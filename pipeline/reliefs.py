"""HMRC January 2026 relief costs. ODS parsed using the standard library.

Pinned publication vintages deliberately prevent silent schema/coverage changes.
Fetcher archives raw sources and retrieval metadata; unavailable costs stay null.
"""
from io import BytesIO, StringIO
from zipfile import ZipFile
from xml.etree import ElementTree as ET
import csv
import hashlib
import re

WORKBOOK='https://assets.publishing.service.gov.uk/media/69a0194e3e672177d0bc76e6/tax_relief_statistics_january_2026.ods'
PUBLICATION='https://www.gov.uk/government/statistics/tax-reliefs/tax-relief-statistics-january-2026'
METHODOLOGY='https://www.gov.uk/government/statistics/tax-reliefs/quality-and-methodology-information-report-january-2026'
PENSION_TABLE='https://assets.publishing.service.gov.uk/media/6a673e0d5e87122783093900/Table_6.csv'
PENSION_DISTRIBUTION='https://assets.publishing.service.gov.uk/media/6a673e0e5e87122783093901/Tables_6_1_and_6_2.csv'
PENSION_SOURCE='https://www.gov.uk/government/statistics/personal-and-stakeholder-pensions-statistics'
VINTAGE='2026-01-22'
T='{urn:oasis:names:tc:opendocument:xmlns:table:1.0}'

def ods_rows(raw):
    root=ET.fromstring(ZipFile(BytesIO(raw)).read('content.xml'))
    sheets={}
    for table in root.iter(T+'table'):
        rows=[]
        for row in table.iter(T+'table-row'):
            values=[]
            for cell in row:
                value=''.join(cell.itertext()).strip()
                repeat=int(cell.get(T+'number-columns-repeated','1'))
                # Ignore enormous ODS empty padding; all known tables have <=14 columns.
                values.extend([value]*min(repeat,max(0,20-len(values))))
            if any(values):rows.append(values)
        sheets[table.get(T+'name')]=rows
    return sheets

def year(raw):
    match=re.fullmatch(r'(\d{4}) to (\d{4})',raw.strip())
    return f'{match[1]}-{match[2][2:]}' if match else None

def number(raw):
    text=raw.strip().replace(',','')
    if re.fullmatch(r'-?\d+(?:\.\d+)?',text):return float(text)
    return None

def estimate(raw,yr,first_forecast=None):
    value=number(raw)
    status=('forecast' if first_forecast and yr>=first_forecast else 'estimate') if value is not None else {'Negligible':'negligible','Disclosive':'withheld','Not available':'unavailable','':'unavailable'}.get(raw)
    if status is None:raise ValueError(f'Unknown HMRC cost status: {raw!r}')
    return {'year':yr,'costMillion':value,'status':status,'rawValue':raw,'claimants':None,'claimantStatus':'unavailable','isForecast':bool(first_forecast and yr>=first_forecast)}

def nullable(raw):return None if raw in ('','Not available','N/A','None.') else raw

def parse_reliefs(raw,retrieval_date=None):
    sheets=ods_rows(raw)
    for key in ('Table_2','Table_3','Table_4','Table_5'):
        if key not in sheets:raise ValueError(f'Missing HMRC sheet {key}')
    rows=[]
    for key,kind in [('Table_2','multi-year'),('Table_3','single-year'),('Table_4','unavailable')]:
        header=sheets[key][1]
        if header[:4]!=['Name','Code','Tax type','Relief type']:raise ValueError('HMRC column schema changed')
        years=[year(h) for h in header[5:11]] if key=='Table_2' else []
        if key=='Table_2' and (len(years)!=6 or not all(years)):raise ValueError('HMRC year columns changed')
        for row in sheets[key][2:]:
            if len(row)<4 or row[3] not in ('Non-structural','Structural'):continue
            name,code,tax,classification=row[:4]
            # HMRC codes are not unique (pensions have component rows), so retain code separately.
            id_=hashlib.sha256(f'{code}|{tax}|{name}|{classification}'.encode()).hexdigest()[:16]
            item={'id':id_,'hmrcCode':nullable(code),'name':name,'taxHead':tax,'classification':classification.lower(),'estimateType':kind,'objective':None,'description':None,'notes':None,'quality':None,'sourceUrl':WORKBOOK,'publicationVintage':VINTAGE,'retrievalDate':retrieval_date,'firstForecastYear':None,'estimates':[]}
            if key=='Table_2':
                first=year(row[4]);item.update(firstForecastYear=first,description=nullable(row[11]),quality=nullable(row[12]),notes=nullable(row[13]))
                item['estimates']=[estimate(v,y,first) for v,y in zip(row[5:11],years)]
            elif key=='Table_3':
                yr=year(row[4])
                if not yr:raise ValueError('Invalid HMRC single-year estimate year')
                item.update(description=nullable(row[7]),quality=nullable(row[6]),notes=nullable(row[8]),estimates=[estimate(row[5],yr)])
            else:item.update(description=nullable(row[5]),notes=nullable(row[4]))
            rows.append(item)
    for item in rows:
        item['aggregationRole']='component' if ('of which' in item['name'].lower() or item['name']=='Pension schemes - member contributions') else 'standalone'
    lookup={(r['hmrcCode'],r['name'],r['taxHead'],r['classification']):r for r in rows}
    if len(lookup)!=len(rows):raise ValueError('Duplicate HMRC relief identity')
    claimant_header=sheets['Table_5'][1]
    if claimant_header[:4]!=['Name','Code','Tax type','Relief type']:raise ValueError('HMRC claimant column schema changed')
    claimant_years=[year(h) for h in claimant_header[5:11]]
    if len(claimant_years)!=6 or not all(claimant_years) or len(set(claimant_years))!=6:raise ValueError('HMRC claimant year schema changed')
    for row in sheets['Table_5'][2:]:
        if len(row)<11 or row[3] not in ('Non-structural','Structural'):continue
        item=lookup.get((nullable(row[1]),row[0],row[2],row[3].lower()))
        if item is None:raise ValueError('Unmatched HMRC claimant row')
        by_year={e['year']:e for e in item['estimates']}
        for yr,raw_value in zip(claimant_years,row[5:11]):
            if yr in by_year:
                val=number(raw_value);first=year(row[4])
                by_year[yr].update(claimants=val,claimantStatus=('forecast' if first and yr>=first else 'estimate') if val is not None else ('withheld' if raw_value=='Disclosive' else 'unavailable'),claimantRawValue=raw_value)
    data={'schemaVersion':1,'asOf':VINTAGE,'publicationDate':VINTAGE,'unit':'GBP million','defaultYear':'2024-25','years':[year(h) for h in sheets['Table_2'][1][5:11]],
      'sources':[{'name':'HMRC estimated cost of tax reliefs, January 2026','url':WORKBOOK},{'name':'HMRC commentary and official aggregate','url':PUBLICATION},{'name':'HMRC quality and methodology','url':METHODOLOGY}],
      'aggregate':{'year':'2024-25','costMillion':218000,'count':103,'label':'Estimated cost of non-structural reliefs with available multi-year estimates','source':PUBLICATION,'rounding':'Official aggregate rounded to £1 billion; independently costed reliefs are not an abolition revenue estimate.'},
      'notes':['Tax relief cost ≠ revenue available. Estimates do not model all behavioural responses, interactions or wider economic effects of abolition.','Do not add relief costs to government expenditure, borrowing or PSNB.','The official headline excludes single-year estimates, withheld estimates and uncosted reliefs. Coverage varies by year.','2025-26 is predominantly forecast. Individual first-forecast years are retained; earlier values are estimates, not necessarily final outturn.','Negligible means less than £3 million; shown as missing numeric values, never zero.','HMRC tax heads and structural/non-structural classifications are retained verbatim apart from letter case. Multiple-tax-head amounts must not be duplicated across tax-head totals.','Description is HMRC’s description of a relief; no inferred policy objective is supplied.'],
      'reliefs':rows}
    validate_reliefs(data)
    return data

def parse_pension(raw):
    reader=csv.DictReader(StringIO(raw.decode('utf-8-sig')))
    result=[]
    for r in reader:
        value_key='value' if 'value' in r else 'value_of_relief'
        raw_value=r.pop(value_key);value=number(raw_value);r['status']='estimate' if value is not None else 'not applicable' if raw_value=='[z]' else 'unavailable';r['rawValue']=raw_value;r['year']=year(r.pop('tax_year').strip());r['costMillion']=value
        if not r['year'] or (value is None and raw_value!='[z]'):raise ValueError('Invalid HMRC pension table value')
        result.append(r)
    return result

def validate_reliefs(data):
    rows=data.get('reliefs',[])
    if len(rows)<500:raise ValueError('Incomplete HMRC relief dataset')
    if len({r['id'] for r in rows})!=len(rows):raise ValueError('Duplicate relief id')
    for r in rows:
        if r['classification'] not in ('non-structural','structural'):raise ValueError('Unknown relief classification')
        for e in r['estimates']:
            if e['status'] in ('negligible','withheld','unavailable') and e['costMillion'] is not None:raise ValueError('Missing relief estimate converted to a value')
    total=sum(e['costMillion'] for r in rows if r['classification']=='non-structural' and r['estimateType']=='multi-year' for e in r['estimates'] if e['year']=='2024-25' and e['costMillion'] is not None)
    if abs(total-218000)>1000:raise ValueError(f'HMRC aggregate consistency check failed: {total}')

def fetch_reliefs(fetcher):
    raw=fetcher(WORKBOOK)
    record=next((r for r in reversed(getattr(fetcher,'records',[])) if r['url']==WORKBOOK),{})
    data=parse_reliefs(raw,record.get('retrievedAt'))
    from .isa import fetch_isa
    data['isa']=fetch_isa(fetcher)
    data['pensions']={'publicationVintage':'2026-07-30','sourceUrl':PENSION_SOURCE,'unit':'GBP million','notes':['July 2026 pension statistics are a later vintage than the January 2026 tax-relief headline. Do not splice the two vintages.','Gross pension relief, net pension relief and tax collected on pensions are different measures; table totals overlap their component rows.'], 'history':parse_pension(fetcher(PENSION_TABLE)),'distribution':parse_pension(fetcher(PENSION_DISTRIBUTION))}
    return data

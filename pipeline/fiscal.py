"""ONS PUSF and Treasury PESA, with explicit series and accounting checks."""
import csv
import io
import re
from datetime import datetime
import openpyxl

ONS_URL = 'https://www.ons.gov.uk/file?uri=/economy/governmentpublicsectorandtaxes/publicsectorfinance/datasets/publicsectorfinances/current/pusf.csv'
ONS_PAGE = 'https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicsectorfinance/datasets/publicsectorfinances'
PESA_PAGE = 'https://www.gov.uk/government/statistics/public-expenditure-statistical-analyses-2026'
PESA_URL = 'https://assets.publishing.service.gov.uk/media/6a5772f59e63154454413701/PESA_2026_CP_Chapter_5_tables.xlsx'
SCOPE = 'UK public sector excluding public sector banks'
SERIES = {
 'borrowing': ('DZLS', 'Net borrowing', '£ million', SCOPE),
 'receipts': ('JW2O', 'Current receipts', '£ million', SCOPE),
 'spending': ('KX5Q', 'Total managed expenditure', '£ million', SCOPE),
 'debtPct': ('HF6X', 'Public sector net debt', '% of GDP', SCOPE),
 'debtBillion': ('HF6W', 'Public sector net debt', '£ billion', SCOPE),
 'incomeTax': ('LIBR', 'Income tax & capital gains tax', '£ million', 'Central government'),
 'nic': ('AIIH', 'Compulsory social contributions', '£ million', 'Central government'),
 'vat': ('NZGF', 'VAT', '£ million', 'Central government'),
 'corporationTax': ('CPRN', 'Corporation tax (gross of tax credits)', '£ million', 'Central government'),
 'goodsServices': ('FV4W', 'Goods & services', '£ million', SCOPE),
 'benefits': ('CWNZ', 'Net social benefits', '£ million', SCOPE),
 'interest': ('JW2P', 'Interest & dividends to private sector / rest of world', '£ million', SCOPE),
 'netInvestment': ('DZLW', 'Net investment', '£ million', SCOPE),
 'depreciation': ('JW2S', 'Consumption of fixed capital', '£ million', SCOPE),
 'currentSpending': ('JW2Q', 'Current expenditure', '£ million', SCOPE),
}

def number(value):
    if value is None or str(value).strip() in ('', '..', '...', 'NA', 'N/A', '-'):
        return None
    result = float(str(value).replace(',', '').strip())
    if not (-1e15 < result < 1e15):
        raise ValueError('Non-finite or implausible number')
    return result

def parse_pusf(raw):
    rows = list(csv.reader(io.StringIO(raw.decode('utf-8-sig'))))
    if len(rows) < 9 or rows[0][0] != 'Title' or rows[1][0] != 'CDID':
        raise ValueError('Expected ONS PUSF CSV headers')
    indices = {code: i for i, code in enumerate(rows[1])}
    missing = [v[0] for v in SERIES.values() if v[0] not in indices]
    if missing:
        raise ValueError(f'Missing required ONS series: {missing}')
    metadata = {r[0]: r for r in rows[2:7]}
    release = datetime.strptime(metadata['Release Date'][indices['DZLS']], '%d-%m-%Y').date().isoformat()
    next_release = metadata['Next release'][indices['DZLS']]
    observations = []
    for row in rows[7:]:
        if not re.fullmatch(r'\d{4} [A-Z]{3}', row[0]):
            continue
        date = datetime.strptime(row[0], '%Y %b').strftime('%Y-%m')
        if date < '2000-04':
            continue
        obs = {'date': date, **{key: number(row[indices[spec[0]]]) for key, spec in SERIES.items()}}
        if any(obs[k] is None for k in ['borrowing','receipts','spending','debtPct','debtBillion']):
            raise ValueError(f'Missing core observation in {date}')
        if abs(obs['spending'] - obs['receipts'] - obs['borrowing']) > 1:
            raise ValueError(f'Borrowing reconciliation failed in {date}')
        # Named source components, not a derived residual disguised as expenditure.
        if all(obs[k] is not None for k in ['currentSpending','depreciation','netInvestment']):
            if abs(obs['currentSpending'] + obs['depreciation'] + obs['netInvestment'] - obs['spending']) > 2:
                raise ValueError(f'Expenditure bridge failed in {date}')
        observations.append(obs)
    if len(observations) < 24 or len({o['date'] for o in observations}) != len(observations):
        raise ValueError('Insufficient or duplicate monthly observations')
    observations.sort(key=lambda r: r['date'])
    for left,right in zip(observations,observations[1:]):
        y,m=map(int,left['date'].split('-')); expected=f'{y+(m==12):04d}-{m%12+1:02d}'
        if right['date'] != expected: raise ValueError(f'Missing month after {left["date"]}')
    return {
      'schemaVersion': 1, 'asOf': observations[-1]['date'], 'releaseDate': release,
      'nextRelease': next_release, 'scope': SCOPE, 'basis': 'Current prices, accruals, not seasonally adjusted',
      'sources': [{'id':'ons-pusf','name':'ONS · Public sector finances','url':ONS_PAGE,'downloadUrl':ONS_URL,
                   'publicationDate':release,'observationDate':observations[-1]['date'],'licence':'Open Government Licence v3.0'}],
      'series': {key:{'code':spec[0],'label':spec[1],'unit':spec[2],'scope':spec[3],
                       'sourceTitle':rows[0][indices[spec[0]]]} for key,spec in SERIES.items()},
      'observations': observations,
      'notes': ['Positive borrowing is a deficit; negative borrowing is a surplus.',
                'Total managed expenditure − current receipts = net borrowing (all excluding public sector banks).',
                'Total managed expenditure = current expenditure + consumption of fixed capital + net investment.',
                'Selected tax details cover central government and do not form an exhaustive public-sector receipts decomposition.',
                'GDP ratios are published ONS ratios using the ONS denominator convention, not ratios calculated by this dashboard.',
                'All historical observations use this release vintage and are subject to revision.'],
    }

def parse_pesa(raw):
    book = openpyxl.load_workbook(io.BytesIO(raw),data_only=True,read_only=True)
    if '5_2' not in book.sheetnames: raise ValueError('Missing PESA table 5.2')
    rows = list(book['5_2'].values)
    if 'Public sector expenditure on services' not in str(rows[0][1]): raise ValueError('Unexpected PESA table')
    year_columns = [(i,str(v)) for i,v in enumerate(rows[4]) if re.fullmatch(r'\d{4}-\d{2}',str(v))]
    names = ['General public services','Defence','Public order and safety','Economic affairs','Environment protection',
             'Housing and community amenities','Health','Recreation, culture and religion','Education','Social protection','EU transactions']
    by_label = {str(r[1]).strip().lower():r for r in rows if r[1] is not None}
    years=[]
    for col,year in year_columns:
        items=[]
        for name in names:
            row=by_label.get('total '+name.lower())
            if row is None: raise ValueError(f'Missing PESA category {name}')
            value=number(row[col])
            if value is None: raise ValueError(f'Missing PESA value {year}/{name}')
            items.append({'name':name,'value':value})
        total=number(by_label['public sector expenditure on services'][col])
        # Eleven independently rounded categories and the rounded total can differ slightly.
        residual=round(total-sum(x['value'] for x in items),6)
        if abs(residual)>6: raise ValueError(f'PESA composition fails reconciliation in {year}')
        if residual: items.append({'name':'Rounding adjustment','value':residual})
        years.append({'year':year,'total':total,'items':items})
    return {'schemaVersion':1,'asOf':years[-1]['year'],'years':years,'unit':'£ million',
       'basis':'Public sector expenditure on services (TES), current prices; includes EU transactions. Different coverage from total managed expenditure.',
       'sources':[{'id':'pesa-2026','name':'HM Treasury · PESA 2026, table 5.2','url':PESA_PAGE,'downloadUrl':PESA_URL,
                   'publicationDate':'2026-07-16','observationDate':years[-1]['year'],'licence':'Open Government Licence v3.0'}],
       'notes':['Five years on a consistent PESA 2026 classification; older vintages are not spliced into this view.',
                'Negative EU transactions are retained, not hidden. Shares use the published TES total.']}

def fetch_fiscal(fetch): return parse_pusf(fetch(ONS_URL))
def fetch_composition(fetch): return parse_pesa(fetch(PESA_URL))

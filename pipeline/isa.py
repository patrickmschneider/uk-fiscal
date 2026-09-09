"""Official ISA holdings/subscriptions, September 2025. No relief-cost model."""
import re
from .reliefs import ods_rows,number,year
WORKBOOK='https://assets.publishing.service.gov.uk/media/68c94808c6df905ce7708427/Individual_Savings_Account_Tables_2025.ods'
SOURCE='https://www.gov.uk/government/statistics/annual-savings-statistics-2025'
COMMENTARY='https://www.gov.uk/government/statistics/tax-reliefs/tax-relief-statistics-january-2026#income-tax-and-capital-gains-tax---individual-savings-accounts'

def table_year(raw):
    match=re.search(r'\d{4} to \d{4}',raw)
    return year(match[0]) if match else None

def clean_number(raw):
    value=number(raw)
    if value is None and raw not in ('[not available]','[too small]',''):
        raise ValueError(f'Unknown ISA value: {raw}')
    return value

def parse_isa(raw,retrieval_date=None):
    sheets=ods_rows(raw);subscriptions=sheets['9_4_ISA_subscriptions'];market=sheets['9_6_ISA_market_values']
    history={}
    # Explicit table sections avoid adding the insurance component twice or mixing Junior ISAs.
    sections=[('Number of accounts subscribed in current year (thousands)','accountsThousand'),('Amounts subscribed (£ million)','subscriptionsMillion'),('Average subscription per account (£)','averageSubscriptionPounds')]
    for title,field in sections:
        start=next(i for i,r in enumerate(subscriptions) if r[0]==title)
        years=subscriptions[start][1:17]
        for r in subscriptions[start+1:start+6]:
            for yr,val in zip(years,r[1:17]):
                y=table_year(yr)
                if not y:raise ValueError('ISA year schema changed')
                key=(y,r[0]);row=history.setdefault(key,{'year':y,'component':r[0],'status':'provisional' if '[provisional]' in yr else 'estimate'})
                row[field]=clean_number(val)
    h=next(r for r in market if len(r)>1 and table_year(r[1]))
    wealth=[]
    labels=['Total ISA and PEP Stocks & Shares Funds','Total ISA Cash Component (including TESSA)','Total ISA Innovative Finance Component','Total Adult ISA and PEP Funds']
    for label in labels:
        row=next(r for r in market if r[0]==label)
        for yr,val in zip(h[1:],row[1:]):
            if not yr:continue
            y=table_year(yr)
            if not y:raise ValueError('ISA market year schema changed')
            wealth.append({'year':y,'component':label,'marketValueMillion':clean_number(val),'status':'provisional' if '[provisional]' in yr else 'estimate'})
    def distribution(name):
        rows=sheets[name];header=next(r for r in rows if 'Average ISA Market Value (£)' in r)
        result=[]
        for row in rows[rows.index(header)+1:]:
            if row[0]=='End of worksheet' or 'Average ISA Market Value (£)' in row:break
            if number(row[9]) is None:continue
            result.append({'group':row[0],'holdersThousand':number(row[9]),'averageMarketValuePounds':number(row[10]),'wealthBands':[{'band':header[i].replace('(thousands)',''),'holdersThousand':clean_number(row[i])} for i in range(1,9)]})
        return result
    income=distribution('9_10_ISA_market_values_income');age=distribution('9_11ISA_market_value_by_age_sex')
    if len(history)!=80 or len(wealth)!=52 or len(income)!=9 or len(age)!=21:raise ValueError('ISA coverage changed: review pinned workbook mapping')
    if next(r for r in history.values() if r['year']=='2023-24' and r['component']=='Total')['subscriptionsMillion']!=102995:raise ValueError('ISA publication control total failed')
    return {'schemaVersion':1,'publicationVintage':'2025-09-18','retrievalDate':retrieval_date,'sourceUrl':WORKBOOK,'publicationUrl':SOURCE,'history':list(history.values()),'marketValues':wealth,'distributionYear':'2022-23','byIncome':income,'byAgeSex':age,'commentary':{'sourceUrl':COMMENTARY,'publicationVintage':'2026-01-22','whyChanged':'HMRC attributes the recent increase in estimated ISA relief to higher interest rates and lower dividend and capital-gains allowances. Accumulation of assets inside ISAs explains the longer-run rise.','distribution':'Holdings are larger on average among older and higher-income ISA holders. These are holdings distributions, not a direct allocation of tax relief by beneficiary.'},'notes':['Subscriptions are annual flows; market values are accumulated stocks, including investment returns. Neither is the fiscal cost of ISA relief.','Accounts subscribed to are not unique individual holders. Individuals may subscribe to more than one type of ISA.','Holder estimates combine a sample of individual returns with provider aggregates; calibration can change reported holder counts.','Distributional information is for 2022-23; aggregate subscriptions and holdings extend to 2023-24. Do not imply that these observations describe the same year.','Lifetime ISA assets are already included in cash and stocks-and-shares market values. Insurance components are of-which rows and are excluded from component totals here.','Income and age distributions describe ISA assets only, not total household wealth or revenue obtainable from reform.','Rounding means component counts may not exactly sum to published totals.']}

def fetch_isa(fetcher):
    raw=fetcher(WORKBOOK)
    record=next((r for r in reversed(getattr(fetcher,'records',[])) if r['url']==WORKBOOK),{})
    return parse_isa(raw,record.get('retrievedAt'))


def compare_relief_releases(previous,current):
    """Audit changes without assuming HMRC's potentially duplicated codes are unique.

    A renamed relief appears as added+removed and needs manual identity review.
    Classification is excluded from the match key so reclassifications are explicit.
    """
    def key(r):return (r.get('hmrcCode'),r['name'],r['taxHead'])
    old={key(r):r for r in previous['reliefs']};new={key(r):r for r in current['reliefs']}
    if len(old)!=len(previous['reliefs']) or len(new)!=len(current['reliefs']):raise ValueError('Ambiguous relief identity requires manual review')
    changed=[]
    for k in old.keys()&new.keys():
        fields=[f for f in ('classification','estimateType','firstForecastYear','description','notes','quality','estimates') if old[k].get(f)!=new[k].get(f)]
        if fields:changed.append({'name':new[k]['name'],'hmrcCode':new[k].get('hmrcCode'),'fields':fields})
    return {'added':[new[k]['name'] for k in sorted(new.keys()-old.keys(),key=str)],'removed':[old[k]['name'] for k in sorted(old.keys()-new.keys(),key=str)],'changed':sorted(changed,key=lambda r:r['name'])}

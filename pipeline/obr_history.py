"""Pinned, user-supplied OBR databank. Read cached source values, never stale sheets.

Historical aggregates travel together: do not subtract structural borrowing from
another vintage's headline borrowing or convert with another vintage's GDP.
"""
import hashlib
import io
import math
import re
from pathlib import Path
import openpyxl

WORKBOOK=Path(__file__).resolve().parents[1]/'data/PSF_aggregates_databank_Aug-4.xlsx'
SOURCE_URL='https://obr.uk/download/public-finances-databank-august-2026/'


def parse_databank(raw):
    book=openpyxl.load_workbook(io.BytesIO(raw),data_only=True,read_only=True)
    cash=list(book['Aggregates (£bn)'].values)
    ratios=list(book['Aggregates (per cent of GDP)'].values)
    notes=' '.join(str(c) for r in cash for c in r if isinstance(c,str))
    if 'released on 21 August 2026' not in notes or 'Forecast years from 2026-27' not in notes:
        raise ValueError('Review the new OBR databank vintage before importing')
    def columns(rows):
        headers=rows[3]
        def index(label):
            if headers.count(label)!=1:raise ValueError(f'Missing or duplicate OBR column: {label}')
            return headers.index(label)
        return {key:index(label) for key,label in {
            'borrowingBn':'Public sector net borrowing',
            'structuralBorrowingBn':'Cyclically-adjusted net borrowing',
            'primaryBalanceBn':'Primary balance',
            'structuralPrimaryBalanceBn':'Cyclically-adjusted primary balance',
            'receiptsBn':'Public sector current receipts',
            'spendingBn':'Total managed expenditure',
        }.items()}
    ci,pi=columns(cash),columns(ratios)
    gdp=cash[3].index('Nominal GDP (£ billion)')
    by_year={r[1]:r for r in ratios if isinstance(r[1],str) and re.fullmatch(r'\d{4}-\d{2}',r[1])}
    rows=[]
    for r in cash:
        year=r[1]
        if not isinstance(year,str) or not re.fullmatch(r'\d{4}-\d{2}',year) or not '1975-76'<=year<'2026-27':continue
        values={k:r[i] for k,i in ci.items()}
        values['gdpBn']=r[gdp]
        if any(not isinstance(v,(float,int)) or not math.isfinite(v) for v in values.values()):
            raise ValueError(f'Missing numeric OBR historical aggregate in {year}')
        if values['gdpBn']<=0:raise ValueError('Nonpositive historical GDP')
        if abs(values['spendingBn']-values['receiptsBn']-values['borrowingBn'])>.002:
            raise ValueError('OBR historical borrowing identity failed')
        for key in ci:
            expected=values[key]/values['gdpBn']*100
            if abs(expected-by_year[year][pi[key]])>.00001:raise ValueError('OBR cash/GDP sheets disagree')
        interest=values['borrowingBn']+values['primaryBalanceBn']
        values.update(year=year,status='outturn',interestBn=interest,deficitInterestBn=interest,
            borrowingPct=100*values['borrowingBn']/values['gdpBn'],
            primaryBalancePct=100*values['primaryBalanceBn']/values['gdpBn'],
            structuralPrimaryBalancePct=100*values['structuralPrimaryBalanceBn']/values['gdpBn'])
        rows.append(values)
    if len(rows)!=51 or rows[0]['year']!='1975-76' or rows[-1]['year']!='2025-26':
        raise ValueError('Incomplete OBR structural history')
    return {'rows':rows,'source':{'id':'obr-databank-history','name':'OBR August 2026 Public Finances Databank','url':SOURCE_URL},
        'outturnAsOf':'2026-08-21','fileSha256':hashlib.sha256(raw).hexdigest(),
        'fileName':WORKBOOK.name,'sheets':['Aggregates (£bn)','Aggregates (per cent of GDP)'],
        'note':'Historical totals, primary and cyclically adjusted balances use one OBR databank vintage and its financial-year GDP. Positive balances denote surpluses. Cyclical borrowing is total minus cyclically adjusted borrowing; these are revised model estimates.'}

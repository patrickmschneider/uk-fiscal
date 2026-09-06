"""DMO gilt stock XML and a deliberately bounded set of official PDF notices.

Pinned notices are reproducible, but are NOT an automatically discovered complete
auction history or current calendar. The output carries this coverage limitation.
"""
from datetime import date, datetime, timezone
from decimal import Decimal
from fractions import Fraction
from io import BytesIO
import json
import math
from pathlib import Path
import re
import xml.etree.ElementTree as ET

CATALOGUE = Path(__file__).resolve().parents[1] / 'catalogue' / 'dmo.json'
FRACTIONS = {'⅛': '1/8', '¼': '1/4', '⅜': '3/8', '½': '1/2', '⅝': '5/8', '¾': '3/4', '⅞': '7/8'}
DAY = r'(?:Monday|Tuesday|Wednesday|Thursday|Friday)'
MONTH = r'(?:January|February|March|April|May|June|July|August|September|October|November|December)'
DATE = r'\d{1,2} ' + MONTH + r' \d{4}'


def number(s):
    n = float(Decimal(s.replace(',', '')))
    if not math.isfinite(n):
        raise ValueError('Non-finite DMO numeric value')
    return n


def match(pattern, text, flags=0):
    found = re.search(pattern, text, flags)
    if not found:
        raise ValueError('DMO document schema changed: ' + pattern)
    return found.group(1)


def iso(s):
    return datetime.strptime(s.strip(), '%d %B %Y').date().isoformat()


def coupon(name):
    prefix = name.split('%')[0].strip()
    for glyph, fraction in FRACTIONS.items():
        prefix = prefix.replace(glyph, ' ' + fraction)
    return float(sum(Fraction(part) for part in prefix.split()))


def parse_stock(raw):
    root = ET.fromstring(raw.strip())
    if root.tag != 'Data':
        raise ValueError('Expected DMO Data XML, not an HTML error page')
    rows = root.findall('View_GILTS_IN_ISSUE')
    if not rows:
        raise ValueError('No gilt stock rows')
    dates = {r.attrib['CLOSE_OF_BUSINESS_DATE'][:10] for r in rows}
    if len(dates) != 1:
        raise ValueError('Mixed DMO stock observation dates')
    as_of = dates.pop()
    date.fromisoformat(as_of)
    securities = []
    seen = set()
    for r in rows:
        a = r.attrib
        isin = a['ISIN_CODE']
        if isin in seen or not re.fullmatch(r'GB[A-Z0-9]{10}', isin):
            raise ValueError('Duplicate or malformed gilt ISIN: ' + isin)
        seen.add(isin)
        kind = a['INSTRUMENT_TYPE'].strip()
        if kind != 'Conventional' and not kind.startswith('Index-linked'):
            raise ValueError('Unrecognised gilt instrument type: ' + kind)
        maturity = a['REDEMPTION_DATE'][:10]
        if date.fromisoformat(maturity) <= date.fromisoformat(as_of):
            raise ValueError('Redeemed instrument in live stock')
        nominal = number(a['TOTAL_AMOUNT_IN_ISSUE'])
        uplifted = number(a['TOTAL_AMOUNT_INCLUDING_IL_UPLIFT'])
        if nominal <= 0 or uplifted <= 0:
            raise ValueError('Non-positive outstanding principal')
        if kind == 'Conventional' and abs(nominal - uplifted) > .000001:
            raise ValueError('Conventional gilt unexpectedly has inflation uplift')
        securities.append({'isin': isin, 'name': a['INSTRUMENT_NAME'],
                           'type': 'conventional' if kind == 'Conventional' else 'index-linked',
                           'indexationLag': None if kind == 'Conventional' else kind.removeprefix('Index-linked ').strip(),
                           'couponPct': coupon(a['INSTRUMENT_NAME']), 'maturityDate': maturity,
                           'nominalMillion': nominal, 'upliftedMillion': uplifted})
    return as_of, sorted(securities, key=lambda r: (r['maturityDate'], r['isin']))


def pdf_text(raw, layout=True):
    from pypdf import PdfReader
    if not raw.startswith(b'%PDF-'):
        raise ValueError('DMO PDF download returned non-PDF content')
    return '\n'.join(p.extract_text(extraction_mode='layout' if layout else 'plain') for p in PdfReader(BytesIO(raw)).pages)


def parse_auction(text, source):
    flat = ' '.join(text.split())
    name = match(r'auction of\s+£[\d,]+ million of (.*?)\s*\(ISIN', flat)
    linked = 'Index-linked' in name
    yield_pattern = r'Striking Price[^\n]*?([\d.]+)%' if linked else r'Non-competitive allotment price[^\n]*?([\d.]+)%'
    # The last million amount preceding total bids is the total allocation.
    before_bids = text.split('Total bids received')[0]
    allotted = re.findall(r'£([\d,.]+)\s+million', before_bids)[-1]
    return {'date': iso(match('(' + DATE + ')', text)),
            'isin': match(r'ISIN [Cc]ode:\s*(GB[A-Z0-9]{10})', flat),
            'name': name, 'type': 'index-linked' if linked else 'conventional',
            'offeredMillion': number(match(r'auction of\s+£([\d,]+) million', flat)),
            'allottedMillion': number(allotted),
            'bidsMillion': number(match(r'Total bids received\s+£([\d,.]+)', flat)),
            'yieldPct': number(match(yield_pattern, text)),
            'yieldBasis': 'real striking yield' if linked else 'nominal average accepted yield',
            'cover': number(match(r'Times covered\**\s+([\d.]+)', flat)),
            'tailBp': None if linked else number(match(r'Tail\*?\s+([\d.]+) bps', flat)),
            'postAuctionMillion': None, 'sourceUrl': source['url'],
            'publicationDate': source['publicationDate']}


def parse_calendar(text, source):
    year = source['calendarYear']
    events = []
    expected = int(match(r'plans to hold (\d+) gilt auctions', text))
    table = text.split('Table 1.')[1].split('2.')[0]
    for line in table.splitlines():
        m = re.match(r'\s*' + DAY + r' (\d{1,2} ' + MONTH + r')\d?\s+\d{1,2}\.\d{2}am\s+(.*?)\s{2,}' + DAY + r' (\d{1,2} ' + MONTH + r')', line)
        if m:
            name = re.sub(r'(20\d{2})\d$', r'\1', m[2])  # trailing footnote marker
            events.append({'date': iso(f'{m[1]} {year}'), 'type': 'auction', 'name': name,
                           'announcementDate': iso(f'{m[3]} {year}'), 'amountMillion': None,
                           'status': 'planned', 'sourceUrl': source['url'],
                           'publicationDate': source['publicationDate'], 'datePrecision': 'day'})
    if len(events) != expected:
        raise ValueError(f'Calendar auction count {len(events)} != published {expected}')
    tender_table = text.split('Table 2.')[-1].split('3.')[0]
    tenders = []
    for line in tender_table.splitlines():
        m = re.match(r'\s*' + DAY + r' (\d{1,2} ' + MONTH + r')\**\s{2,}(.*?)\s{2,}At least', line)
        if m:
            tenders.append({'date': iso(f'{m[1]} {year}'), 'type': 'tender', 'name': m[2],
                            'announcementDate': None, 'amountMillion': None,
                            'status': 'provisional; subject to demand and market conditions',
                            'sourceUrl': source['url'], 'publicationDate': source['publicationDate'], 'datePrecision': 'day'})
    if len(tenders) != 4:
        raise ValueError('Expected four tenders in pinned quarterly calendar')
    return events + tenders


def parse_announcement(text, source):
    flat = ' '.join(text.split())
    return {'date': iso(match(r'Auction Date ' + DAY + r', (' + DATE + ')', flat)),
            'type': 'auction', 'name': match(r'Title (.*?) Amount \(nominal\)', flat),
            'isin': match(r'ISIN Code (GB[A-Z0-9]{10})', flat),
            'announcementDate': source['publicationDate'],
            'settlementDate': iso(match(r'Issue and Settlement Date ' + DAY + r', (' + DATE + ')', flat)),
            'amountMillion': number(match(r'Amount \(nominal\) for auction £([\d,.]+) million', flat)),
            'status': 'announced', 'datePrecision': 'day', 'sourceUrl': source['url'],
            'publicationDate': source['publicationDate']}



def instrument_key(name):
    """Canonical full source name: coupon notation varies across XML/PDFs."""
    suffix = ' '.join(name.split('%', 1)[1].split()).casefold()
    return f'{coupon(name):g}% {suffix}'


def parse_quarterly_auctions(text, source, identities):
    """Only the auction subsection; do not treat syndications/tenders as auctions."""
    section = text.split('Gilt operations review')[1]
    section = re.split(r'Auction(?:\(s\)|s)', section, maxsplit=1)[1].split('Syndication')[0]
    rows = []
    by_name = {}
    for identity in identities:
        key = instrument_key(identity['name'])
        if key in by_name:
            raise ValueError('Ambiguous archived DMO instrument name: ' + key)
        by_name[key] = identity
    for line in section.splitlines():
        if not re.match(r'\d{2}-[A-Za-z]{3}-\d{2}', line):
            continue
        m = re.fullmatch(r'(\d{2}-[A-Za-z]{3}-\d{2})\s+(.*?Gilt \d{4})\s+(.*)', line.strip())
        if not m:
            raise ValueError('Malformed quarterly auction row: ' + line)
        dt, name, rest = m.groups()
        linked = 'Index-linked' in name
        values = rest.split()
        # Green auction PAOF is blank (inapplicable), unlike a reported dash.
        if 'Green' in name and len(values) == 5:
            values.insert(1, '-')
        expected = (5, 6) if linked else (6,)
        if len(values) not in expected:
            raise ValueError('Unexpected quarterly auction columns: ' + line)
        issued, paof, cash, yield_value = values[:4]
        identity = by_name.get(instrument_key(name))
        if identity is None:
            raise ValueError('Quarterly instrument has no archived identity: ' + name)
        rows.append({'date': datetime.strptime(dt, '%d-%b-%y').date().isoformat(),
                     'isin': identity['isin'], 'name': name,
                     'type': 'index-linked' if linked else 'conventional',
                     'offeredMillion': None, 'allottedMillion': number(issued),
                     'bidsMillion': None, 'yieldPct': number(yield_value),
                     'yieldBasis': 'real striking yield' if linked else 'nominal average accepted yield',
                     'cover': number(values[-1]), 'tailBp': None if linked else number(values[-2]),
                     'postAuctionMillion': None if paof == '-' else number(paof),
                     'sourceUrl': source['url'], 'publicationDate': source['publicationDate'],
                     'precisionNote': 'Quarterly review: issuance/PAOF rounded to £0.1m and yields to 0.01 percentage points. A dash/blank PAOF is retained as null; no offered amount or total bids reported.'})
    if len(rows) != source['auctionCount']:
        raise ValueError('Quarterly review auction count changed')
    return rows

def fetch_debt(fetch):
    catalogue = json.loads(CATALOGUE.read_text())
    now = datetime.now(timezone.utc).isoformat()
    stock_source = catalogue['stock']
    as_of, securities = parse_stock(fetch(stock_source['url']))
    auctions, events, options, sources = [], [], {}, []
    sources.append({**stock_source, 'observationDate': as_of, 'publicationDate': None, 'retrievedAt': now})
    for source in catalogue['notices']:
        kind = source['kind']
        text = pdf_text(fetch(source['url']), layout=kind != 'quarterly-review')
        if kind == 'quarterly-review':
            auctions.extend(parse_quarterly_auctions(text, source, catalogue['instrumentIdentities']))
        elif kind == 'auction':
            auctions.append(parse_auction(text, source))
        elif kind == 'calendar':
            events.extend(parse_calendar(text, source))
        elif kind == 'announcement':
            events.append(parse_announcement(text, source))
        elif kind == 'post-auction':
            flat = ' '.join(text.split())
            isin = match(r'ISIN Code:\s*(GB[A-Z0-9]{10})', flat)
            amount = 0.0 if 'There were no additional amounts' in flat else number(match(r'An additional £([\d,.]+) million', flat))
            options[(source['publicationDate'], isin)] = (amount, source['url'])
        elif kind == 'syndication':
            flat = ' '.join(text.split())
            events.append({'date': iso(match(r'week commencing (' + DATE + ')', flat, re.I)),
                           'datePrecision': 'week', 'type': 'syndication',
                           'name': match(r're-opening of (.*?)\. The transaction', flat),
                           'amountMillion': None, 'announcementDate': source['publicationDate'],
                           'status': 'provisional; subject to demand and market conditions',
                           'sourceUrl': source['url'], 'publicationDate': source['publicationDate']})
        sources.append({**source, 'observationDate': source['publicationDate'], 'retrievedAt': now})
    for auction in auctions:
        key = (auction['date'], auction['isin'])
        if key in options:
            auction['postAuctionMillion'], auction['postAuctionSourceUrl'] = options[key]
    # A later announcement supersedes the quarterly plan for the same day/type.
    deduped = {}
    for event in sorted(events, key=lambda e: e['publicationDate']):
        key = (event['date'], event['type'])
        if key in deduped and deduped[key]['publicationDate'] == event['publicationDate']:
            raise ValueError('Duplicate event in a DMO notice')
        deduped[key] = event
    if len({(a['date'], a['isin']) for a in auctions}) != len(auctions):
        raise ValueError('Duplicate auction result')
    return {'schemaVersion': 1, 'asOf': as_of, 'retrievedAt': now, 'sources': sources,
            'securities': securities,
            'totals': {'nominalMillion': round(sum(s['nominalMillion'] for s in securities), 6),
                       'upliftedMillion': round(sum(s['upliftedMillion'] for s in securities), 6)},
            'auctions': sorted(auctions, key=lambda a: a['date'], reverse=True),
            'calendar': sorted(deduped.values(), key=lambda e: (e['date'], e['type'])),
            'availability': catalogue['availability'], 'definitions': catalogue['definitions']}

"""OBR cumulative borrowing profiles as republished in the ONS PSF bulletin.

The OBR workbook is currently inaccessible from this environment. The official
ONS chart download supplies a compatible PSNB ex profile without interpolation.
"""
import csv
import html
import io
import math
import re
from urllib.parse import quote

LATEST_URL = 'https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicsectorfinance/bulletins/publicsectorfinances/latest'
MONTHS = ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar']


def discover_profile(page):
    """Fail closed if the specific cumulative PSNB chart cannot be identified."""
    matches = re.findall(r'<h4[^>]*>\s*Cumulative public sector net borrowing,.*?</h4>\s*<div[^>]*>\s*<div[^>]*data-uri="([^"]+)"', page, re.S)
    if len(matches) != 1:
        raise ValueError('Expected one ONS cumulative public sector net borrowing chart')
    uri = html.unescape(matches[0])
    if not re.fullmatch(r'/economy/governmentpublicsectorandtaxes/publicsectorfinance/bulletins/publicsectorfinances/[a-z]+\d{4}/[a-z0-9]+', uri):
        raise ValueError('Unrecognised ONS profile download URI')
    release = re.search(r'\["releaseDate"\]\s*=\s*"(\d{4}/\d{2}/\d{2})"', page)
    if not release:
        raise ValueError('ONS publication date is missing')
    return 'https://www.ons.gov.uk/generator?format=csv&uri=' + quote(uri, safe=''), release[1].replace('/', '-')


def parse_profile(raw, source_url, publication_date):
    rows = list(csv.reader(io.StringIO(raw.decode('utf-8-sig'))))
    if not any('Cumulative public sector net borrowing' in cell for row in rows for cell in row):
        raise ValueError('Not a cumulative PSNB profile')
    if not any(row == ['Unit', '£ billion'] for row in rows):
        raise ValueError('Profile units must be £ billion')
    notes = '\n'.join(cell for row in rows[:8] for cell in row)
    vintage = re.search(r'Economic and fiscal outlook\s*[-–—]\s*([A-Z][a-z]+ \d{4}) monthly forecast', notes)
    if not vintage:
        raise ValueError('Forecast vintage missing')
    header_index = next((i for i, row in enumerate(rows) if any(cell.startswith('Borrowing - OBR forecast ') for cell in row)), None)
    if header_index is None:
        raise ValueError('OBR forecast column missing')
    columns = [(i, re.fullmatch(r'Borrowing - OBR forecast (\d{4}) to (\d{4})', cell)) for i, cell in enumerate(rows[header_index])]
    columns = [(i, m) for i, m in columns if m]
    if len(columns) != 1:
        raise ValueError('Expected one labelled forecast column')
    column, match = columns[0]
    start, end = map(int, match.groups())
    if end != start + 1:
        raise ValueError('Invalid forecast financial year')
    values = []
    for row in rows[header_index + 1:]:
        if not row or not any(row):
            continue
        index = len(values)
        if index >= 12 or row[0].strip() != MONTHS[index]:
            raise ValueError('Forecast months must be exactly April to March in order')
        value = float(row[column])
        if not math.isfinite(value):
            raise ValueError('Non-finite forecast value')
        month = (index + 3) % 12 + 1
        values.append({'period': f'{start if month >= 4 else end}-{month:02}', 'value': value})
    if len(values) != 12:
        raise ValueError('Incomplete monthly forecast profile')
    return {
        'schemaVersion': 1, 'status': 'available', 'fiscalYear': f'{start}-{str(end)[2:]}',
        'vintage': vintage[1], 'units': '£ billion',
        'basis': 'Cumulative public sector net borrowing excluding public sector banks; positive is borrowing',
        'publicationDate': publication_date,
        'sources': [{'id': 'obr-profile', 'publisher': 'ONS / OBR', 'title': 'OBR monthly borrowing profile, republished by ONS', 'url': source_url, 'publicationDate': publication_date}],
        'cumulative': values,
        'notes': ['Official cumulative profile as published in the ONS PSF bulletin, rounded to £0.1 billion. No interpolation or division of annual forecast. Publication date is the ONS republication; forecast vintage is separate.'],
    }


def fetch_forecast(fetch):
    url, published = discover_profile(fetch(LATEST_URL).decode('utf-8'))
    return parse_profile(fetch(url), url, published)

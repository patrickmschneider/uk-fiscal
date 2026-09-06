"""Official Bank of England nominal gilt spot-curve importer.

Recognises the two whole-curve sheet names inspected in the official archive.
Missing tenor observations remain null; entirely empty non-trading dates are
excluded. No interpolation is performed.
"""
import io
import math
import re
import zipfile
from datetime import date, datetime, timedelta

from openpyxl import load_workbook

PAGE_URL = 'https://www.bankofengland.co.uk/statistics/yield-curves'
LATEST_URL = 'https://www.bankofengland.co.uk/-/media/boe/files/statistics/yield-curves/latest-yield-curve-data.zip'
ARCHIVE_URL = 'https://www.bankofengland.co.uk/-/media/boe/files/statistics/yield-curves/glcnominalddata.zip'


def parse_zip(raw):
    """Read only the whole nominal spot curve; never forward, real or OIS."""
    curves = {}
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        names = [n for n in archive.namelist() if 'glc nominal' in n.lower() and n.lower().endswith('.xlsx')]
        if not names:
            raise ValueError('No recognised nominal gilt workbook in BoE ZIP')
        for name in names:
            if archive.getinfo(name).file_size > 100_000_000:
                raise ValueError('BoE workbook exceeds import size limit')
            workbook = load_workbook(io.BytesIO(archive.read(name)), data_only=True, read_only=True)
            try:
                sheets = [s for s in workbook.sheetnames if re.fullmatch(r'4\.\s*(?:nominal )?spot curve', s.strip(), re.I)]
                if len(sheets) != 1:
                    raise ValueError('Expected exactly one whole spot-curve worksheet')
                rows = list(workbook[sheets[0]].values)
                headers = []
                for index, row in enumerate(rows[:10]):
                    if str(row[0]).strip().lower().rstrip(':') != 'years':
                        continue
                    numbers = [(i, float(v)) for i, v in enumerate(row[1:], 1) if isinstance(v, (int, float)) and not isinstance(v, bool)]
                    if len(numbers) >= 3 and all(0 < v <= 40 for _, v in numbers):
                        headers.append((index, numbers))
                if len(headers) != 1:
                    raise ValueError('Expected unique numeric maturity header in years')
                header_index, tenors = headers[0]
                if any(b[1] <= a[1] for a, b in zip(tenors, tenors[1:])):
                    raise ValueError('Tenors must be strictly increasing')
                for row in rows[header_index + 1:]:
                    if not isinstance(row[0], (date, datetime)):
                        continue
                    observed = row[0].date() if isinstance(row[0], datetime) else row[0]
                    points = []
                    for column, tenor in tenors:
                        value = row[column] if column < len(row) else None
                        if value is None or value == '':
                            points.append({'tenor': tenor, 'rate': None})
                            continue
                        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or abs(value) > 100:
                            raise ValueError('Invalid spot rate in BoE workbook')
                        points.append({'tenor': tenor, 'rate': float(value)})
                    if any(p['rate'] is not None for p in points):
                        key = observed.isoformat()
                        if key in curves and curves[key] != points:
                            raise ValueError('Conflicting dates within BoE archive')
                        curves[key] = points
            finally:
                workbook.close()
    if not curves:
        raise ValueError('No dated nominal spot rates in BoE ZIP')
    return curves


def fetch_curve(fetch):
    # The latest-month file takes precedence over an older archived vintage.
    curves = parse_zip(fetch(ARCHIVE_URL))
    curves.update(parse_zip(fetch(LATEST_URL)))
    latest = date.fromisoformat(max(curves))
    cutoff = (latest - timedelta(days=370)).isoformat()
    return {
        'schemaVersion': 1, 'status': 'available', 'units': '% per annum',
        'basis': 'Bank of England fitted nominal gilt zero-coupon spot curve, continuously compounded; tenor in years',
        'asOf': latest.isoformat(), 'observationDate': latest.isoformat(), 'publicationDate': None,
        'sources': [{'id': 'boe-curve', 'publisher': 'Bank of England', 'title': 'Nominal gilt spot yield curve', 'url': PAGE_URL, 'downloadUrls': [ARCHIVE_URL, LATEST_URL]}],
        'curves': [{'date': d, 'points': curves[d]} for d in sorted(curves) if d >= cutoff],
        'notes': ['Missing tenor values remain null without interpolation. Entirely empty non-trading dates are excluded. Observation date is not the publication or retrieval date.'],
    }

import re, sys
from collections import Counter, defaultdict
from common import load_data, CANONICAL_COUNTS, CANONICAL_ORDER, ROOT

def validate(write_report=True):
    books, chapters = load_data()
    errors=[]; warnings=[]
    if len(books)!=66: errors.append(f"Expected 66 books; found {len(books)}.")
    if len(chapters)!=1189: errors.append(f"Expected 1,189 chapters; found {len(chapters)}.")
    counts=Counter(c['book'] for c in chapters)
    for book, expected in CANONICAL_COUNTS.items():
        if book not in books: errors.append(f"Missing book on Books sheet: {book}.")
        if counts[book]!=expected: errors.append(f"{book}: expected {expected} chapter rows; found {counts[book]}.")
    unknown=sorted(set(counts)-set(CANONICAL_COUNTS))
    if unknown: errors.append("Unknown book names: " + ", ".join(unknown))
    seen=set()
    pattern=re.compile(r"^(?:[1-3] )?[A-Za-z]+(?: of [A-Za-z]+)? \d+:\d+(?:-\d+)?$")
    for c in chapters:
        key=(c['book'],c['chapter'])
        if key in seen: errors.append(f"Duplicate chapter row: {c['book']} {c['chapter']}.")
        seen.add(key)
        for field in ['verse','identifier','why','insight']:
            if not c[field]: errors.append(f"Blank {field}: {c['book']} {c['chapter']}.")
        if c['verse'] and not pattern.match(c['verse']): warnings.append(f"Review verse format: {c['verse']}.")
    status='PASS' if not errors else 'FAIL'
    report=['# Validation Report','',f'**Status:** {status}','',f'- Books: {len(books)} / 66',f'- Chapters: {len(chapters)} / 1,189',f'- Errors: {len(errors)}',f'- Warnings: {len(warnings)}','']
    if errors:
        report += ['## Errors',''] + [f'- {x}' for x in errors] + ['']
    if warnings:
        report += ['## Warnings',''] + [f'- {x}' for x in warnings] + ['']
    if not errors and not warnings: report += ['No validation issues were found.','']
    if write_report:
        (ROOT/'content/indexes/validation-report.qmd').write_text('\n'.join(report),encoding='utf-8')
    return errors,warnings

if __name__=='__main__':
    errors,warnings=validate(True)
    print(f"Validation: {len(errors)} error(s), {len(warnings)} warning(s)")
    sys.exit(1 if errors else 0)

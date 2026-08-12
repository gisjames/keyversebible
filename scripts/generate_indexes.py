from common import load_data, CANONICAL_ORDER, ROOT

def generate():
    books, chapters=load_data()
    grouped={b:[] for b in CANONICAL_ORDER}
    for c in chapters: grouped[c['book']].append(c)
    lines = [
    '---',
    'title: "Scripture Index | Key Verses by Bible Reference"',
    'description: "Browse the Scripture index for representative key verses selected from all 1,189 chapters of the Bible."',
    'lang: en',
    '---',
    '',
    '# Scripture Index {.unnumbered}',
    '',
    ]
    for book in CANONICAL_ORDER:
        lines += [f'## {book}','']
        for c in sorted(grouped[book],key=lambda x:x['chapter']):
            lines.append(f"- **{c['verse']}** | {c['identifier']}")
        lines.append('')
    (ROOT/'content/indexes/scripture-index.qmd').write_text('\n'.join(lines),encoding='utf-8')

if __name__=='__main__': generate(); print('Generated Scripture index.')

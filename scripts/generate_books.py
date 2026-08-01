from collections import defaultdict
from jinja2 import Environment, FileSystemLoader
from common import load_data, CANONICAL_ORDER, ROOT, slug

def generate():
    books, chapters = load_data()
    grouped=defaultdict(list)
    for c in chapters: grouped[c['book']].append(c)
    env=Environment(loader=FileSystemLoader(ROOT/'templates'), trim_blocks=True, lstrip_blocks=True)
    template=env.get_template('book.qmd.j2')
    out=ROOT/'content/books'; out.mkdir(parents=True,exist_ok=True)
    for old in out.glob('*.qmd'): old.unlink()
    for book in CANONICAL_ORDER:
        rows=sorted(grouped[book],key=lambda x:x['chapter'])
        text=template.render(book=book, summary=books[book]['summary'], chapters=rows)
        (out/f'{slug(book)}.qmd').write_text(text,encoding='utf-8')
    return len(CANONICAL_ORDER),sum(len(v) for v in grouped.values())

if __name__=='__main__':
    print('Generated %d books and %d chapters.' % generate())

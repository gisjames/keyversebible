from collections import defaultdict
from jinja2 import Environment, FileSystemLoader

from common import load_data, ROOT, slug


def generate():
    books, chapters = load_data()

    grouped = defaultdict(list)

    for chapter in chapters:
        grouped[chapter["book"]].append(chapter)

    env = Environment(
        loader=FileSystemLoader(ROOT / "templates"),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    template = env.get_template("chapter.qmd.j2")
    book_template = env.get_template("book-index.qmd.j2")

    output_root = ROOT
    output_root.mkdir(parents=True, exist_ok=True)

    generated = 0

    for book, rows in grouped.items():
        rows = sorted(rows, key=lambda x: x["chapter"])
        book_slug = slug(book)
        book_dir = output_root / book_slug
        book_dir.mkdir(parents=True, exist_ok=True)

        book_info = books[book]

        book_text = book_template.render(
            book=book,
            summary=book_info["summary"],
            chapters=rows,
        )

        (book_dir / "index.qmd").write_text(
            book_text,
            encoding="utf-8",
        )

        for index, chapter in enumerate(rows):
            chapter_number = chapter["chapter"]

            previous_chapter = (
                rows[index - 1]["chapter"]
                if index > 0
                else None
            )

            next_chapter = (
                rows[index + 1]["chapter"]
                if index < len(rows) - 1
                else None
            )

            output_dir = (
                output_root
                / book_slug
                / str(chapter_number)
            )

            output_dir.mkdir(
                parents=True,
                exist_ok=True
            )

            text = template.render(
                **chapter,
                previous_chapter=previous_chapter,
                next_chapter=next_chapter,
            )

            output_file = output_dir / "index.qmd"

            output_file.write_text(
                text,
                encoding="utf-8"
            )

            generated += 1

    return generated


if __name__ == "__main__":
    count = generate()
    print(f"Generated {count} chapter pages.")
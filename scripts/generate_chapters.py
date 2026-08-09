from collections import defaultdict
import json
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
        book_url = (
            f"https://gisjames.github.io/keyversebible/"
            f"{book_slug}/"
        )

        book_description = (
            f"Explore the key verse for every chapter of {book}, "
            f"with chapter insights, explanations, and links to each chapter."
        )

        book_structured_data = {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "CollectionPage",
                    "@id": book_url,
                    "url": book_url,
                    "name": f"{book} Key Verses by Chapter",
                    "description": book_description,
                    "inLanguage": "en",
                    "isPartOf": {
                        "@type": "WebSite",
                        "name": "The Key Verse of Every Chapter of the Bible",
                        "url": "https://gisjames.github.io/keyversebible/",
                    },
                },
                {
                    "@type": "BreadcrumbList",
                    "itemListElement": [
                        {
                            "@type": "ListItem",
                            "position": 1,
                            "name": "Home",
                            "item": "https://gisjames.github.io/keyversebible/",
                        },
                        {
                            "@type": "ListItem",
                            "position": 2,
                            "name": book,
                            "item": book_url,
                        },
                    ],
                },
            ],
        }

        book_schema_json = json.dumps(
            book_structured_data,
            ensure_ascii=False,
            indent=2,
        )

        book_text = book_template.render(
            book=book,
            summary=book_info["summary"],
            chapters=rows,
            schema_json=book_schema_json,
        )

        (book_dir / "index.qmd").write_text(
            book_text,
            encoding="utf-8",
        )

        for index, chapter in enumerate(rows):
            chapter_number = chapter["chapter"]
            canonical_url = (
                f"https://gisjames.github.io/keyversebible/"
                f"{book_slug}/{chapter_number}/"
            )

            book_url = (
                f"https://gisjames.github.io/keyversebible/"
                f"{book_slug}/"
            )

            description = (
                f"Discover the key verse for {book} {chapter_number} "
                f"({chapter['verse']}), why it represents the chapter, "
                f"and a concise insight into its meaning and message."
            )

            structured_data = {
                "@context": "https://schema.org",
                "@graph": [
                    {
                        "@type": "WebPage",
                        "@id": canonical_url,
                        "url": canonical_url,
                        "name": f"{book} {chapter_number} Key Verse | {chapter['verse']}",
                        "description": description,
                        "inLanguage": "en",
                        "isPartOf": {
                            "@type": "WebSite",
                            "name": "The Key Verse of Every Chapter of the Bible",
                            "url": "https://gisjames.github.io/keyversebible/",
                        },
                    },
                    {
                        "@type": "BreadcrumbList",
                        "itemListElement": [
                            {
                                "@type": "ListItem",
                                "position": 1,
                                "name": "Home",
                                "item": "https://gisjames.github.io/keyversebible/",
                            },
                            {
                                "@type": "ListItem",
                                "position": 2,
                                "name": book,
                                "item": book_url,
                            },  
                            {
                                "@type": "ListItem",
                                "position": 3,
                                "name": f"{book} {chapter_number}",
                                "item": canonical_url,
                            },
                        ],
                    },
                ],
            }

            schema_json = json.dumps(
                structured_data,
                ensure_ascii=False,
                indent=2,
            )

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
                schema_json=schema_json,
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
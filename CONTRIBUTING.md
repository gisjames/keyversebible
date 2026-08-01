# Contributing

## Workflow

1. Update `data/bible_key_verses.xlsx`.
2. Run `python scripts/build.py --generate-only`.
3. Correct all validation errors.
4. Render the desired Quarto format.
5. Review generated output before publishing.

Do not edit files in `content/books/` manually. They are regenerated from the workbook.

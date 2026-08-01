# Bible Key Verse Quarto Project — Version 3.1

A book-first Quarto publishing project generated from the Excel workbook in `data/bible_key_verses.xlsx`.

## Outputs

The project is configured to produce:

- HTML book/website
- Print-oriented PDF
- EPUB ebook

## First-time setup

From PowerShell in the extracted project directory:

```powershell
python -m pip install -r requirements.txt
```

For PDF output, install TinyTeX once:

```powershell
quarto install tinytex
```

## Build

Generate the 66 book pages and validate all 1,189 chapter records:

```powershell
python scripts/build.py --generate-only
```

Render all configured formats:

```powershell
quarto render
```

Or run generation and rendering together:

```powershell
python scripts/build.py
```

Render a single format:

```powershell
python scripts/build.py --format html
python scripts/build.py --format pdf
python scripts/build.py --format epub
```

Generated output is written to `output/`.

## Editing workflow

1. Edit `data/bible_key_verses.xlsx`.
2. Save the workbook.
3. Run `python scripts/build.py --generate-only`.
4. Review the validation report.
5. Run `quarto render`.

Do not manually edit files under `content/books/`; the generator replaces them during each build.

## Important Quarto convention

The root-level `index.qmd` is required as the book home page and must remain the first item under `book: chapters:` in `_quarto.yml`.

# DocxToHTML (OpenLMS) — Generate LMS-ready HTML from DOCX

Convert university course Word documents (`.docx`) into **LMS-compatible HTML** (e.g., OpenLMS) and generate **PDFs** (rubrics / schedule) linked directly from the HTML.

This project was built to **support degree-program reviews for CONESUP** and to help institutions that must submit/convert full “**Tomos**” (entire degree programs bundled into large documents). It was tested with a document of **1100+ pages** without issues. It’s also useful for instructors or institutions migrating full courses or complete programs into an HTML-based LMS.

## V1 vs V2 (important)

- **V1**: outputs HTML that follows the **official blueprint / format** currently used by the office to import courses into the LMS. **This is not “how I write HTML”**—it matches the institution’s established import format.
- **V2**: **my take** on the same content: improved UX/visuals while keeping compatibility.

## Features

- Automatic `.docx` → HTML conversion, organized by term / class / week.
- PDF generation (rubrics and schedule) with links inside the HTML.
- Handles large documents (tested with 1100+ pages).
- GUI (Tkinter) with **drag & drop**.
- CLI mode for batch processing.
- V1 and V2 templates.

## Project layout

- `main.py`: GUI app.
- `generate_html.py`: CLI entrypoint.
- `generator_refactor/`: core parsing/transformation/templates/writing logic.
- `packaging/pyinstaller/`: build config to create a Windows `.exe`.

## Requirements

- Python **3.8+**
- Dependencies (installed via `requirements.txt`):
  - `python-docx`
  - `jinja2`
  - `reportlab`
  - `tkinterdnd2`

## Installation (recommended: virtual environment)

```bash
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Usage (GUI)

```bash
python main.py
```

- Drag and drop `.docx` files (or select them via the button).
- Choose **V1** or **V2**.
- Output (HTML/PDF) is generated in the **same folder** as the input `.docx` (current generator behavior).

## Usage (CLI)

```bash
python generate_html.py <input_dir> <out_dir>
```

## Build an executable (optional)

```bash
python -m pip install -r requirements-dev.txt
pyinstaller packaging/pyinstaller/GeneradorHTML.spec
```

## License

MIT — see `LICENSE`.

## Author

Marvs04

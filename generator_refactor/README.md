# Generator core (logic + templates)

This folder contains the core logic to convert DOCX into HTML/PDF (parsing, transformation, templates, and output writing). Project entrypoints live at the repository root:

- `main.py` (GUI)
- `generate_html.py` (CLI)

## Goal

- Preserve the current behavior/output.
- Keep the same main entrypoint behavior: read one or more DOCX files from a folder.
- Keep the same output structure: folders per document, term, class, and week.
- Keep the same generated HTML unless changes are explicitly requested later.
- Scale to multiple terms and dozens of classes per document.

## Working principles

- Do not change `generate_html.py` as an entrypoint until parity is validated.
- Move responsibilities in phases; don’t rewrite everything at once.
- Validate each phase against the same reference DOCX.
- Keep parsing, transformation, rendering, and writing separate.

## Proposed structure

- `generator.py`: main orchestration.
- `docx_reader.py`: reads the document and locates blocks/tables.
- `section_parser.py`: extracts semantic sections from paragraphs.
- `schedule_parser.py`: parses the schedule and weeks.
- `transformers.py`: converts raw data into render-ready structures.
- `templates.py`: Jinja templates.
- `writer.py`: safe names, folders, and file writing.

## Current status

Generation happens in `generator_refactor/` and is invoked by `main.py` / `generate_html.py`.
# DocxToHTML (OpenLMS) — Generador de cursos HTML desde DOCX

Convierte documentos Word (`.docx`) de cursos universitarios en **HTML compatible con plataformas LMS** (ej. OpenLMS) y genera **PDFs** (rúbricas / cronograma) enlazados desde el HTML.

Este proyecto se creó para **apoyar procesos de revisión de carreras por parte de CONESUP** y para instituciones que deben enviar/convertir “**Tomos**” completos de carreras universitarias. Fue probado con un documento de **más de 1100 páginas** sin inconvenientes. También sirve para docentes o instituciones que quieran trasladar clases o carreras enteras a un LMS basado en HTML.

## V1 vs V2 (importante)

- **V1**: genera HTML siguiendo el **blueprint / formato oficial** con el que la oficina **importa actualmente** cursos al LMS. **No es “mi forma” de escribir HTML**, es el formato que la institución ya tenía establecido.
- **V2**: es **mi propuesta** (“mi take”) sobre el mismo contenido: mejoras visuales y de experiencia manteniendo la compatibilidad.

## Características

- Conversión automática de `.docx` a HTML estructurado por cuatrimestre / clase / semana.
- Generación de PDFs (rúbricas y cronograma) y enlaces dentro del HTML.
- Soporte para documentos grandes (probado con >1100 páginas).
- Interfaz gráfica (Tkinter) con **arrastrar y soltar**.
- Modo CLI para automatizar por carpeta.
- Plantillas V1 y V2.

## Estructura del proyecto

- `main.py`: aplicación GUI.
- `generate_html.py`: ejecución por línea de comandos (CLI).
- `generator_refactor/`: lógica principal de parsing, transformación, plantillas y escritura.
- `packaging/pyinstaller/`: configuración para compilar `.exe`.

## Requisitos

- Python **3.8+**
- Dependencias (se instalan con `requirements.txt`):
  - `python-docx`
  - `jinja2`
  - `reportlab`
  - `tkinterdnd2`

## Instalación (recomendado con entorno virtual)

```bash
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Uso (GUI)

```bash
python main.py
```

- Arrastra y suelta archivos `.docx` o selecciónalos con el botón.
- Elige **V1** o **V2**.
- La salida (HTML/PDF) se genera en la **misma carpeta** del `.docx` (según la lógica actual del generador).

## Uso (CLI)

```bash
python generate_html.py <input_dir> <out_dir>
```

## Compilar ejecutable (opcional)

```bash
python -m pip install -r requirements-dev.txt
pyinstaller packaging/pyinstaller/GeneradorHTML.spec
```

## Licencia

MIT — ver `LICENSE`.

## Autor

Marvs04

# Núcleo del generador (lógica + plantillas)

Esta carpeta contiene la lógica principal para convertir DOCX a HTML/PDF (parsing, transformación, templates y escritura). Los puntos de entrada del proyecto son:

- `main.py` (GUI)
- `generate_html.py` (CLI)

## Objetivo

- Conservar la funcionalidad actual.
- Mantener la misma entrada principal: leer uno o varios archivos DOCX desde una carpeta.
- Mantener la misma estructura de salida: carpetas por documento, cuatrimestre, clase y semana.
- Mantener el mismo HTML generado, salvo ajustes explícitos solicitados en el futuro.
- Permitir escalar a múltiples cuatrimestres y decenas de clases por documento.

## Principios de trabajo

- No modificar `generate_html.py` como punto de entrada hasta validar paridad.
- Mover responsabilidades por fases, no reescribir todo de una vez.
- Validar cada fase contra el mismo DOCX de referencia.
- Mantener separados parsing, transformación, renderizado y escritura.

## Estructura propuesta

- `generator.py`: orquestación principal.
- `docx_reader.py`: lectura del documento y localización de bloques/tablas.
- `section_parser.py`: extracción semántica de secciones desde párrafos.
- `schedule_parser.py`: parsing del cronograma y semanas.
- `transformers.py`: conversión a estructuras listas para renderizar.
- `templates.py`: plantillas Jinja y cargadores de templates.
- `writer.py`: nombres seguros, carpetas y escritura de archivos.
- `parity_checklist.md`: lista de validación para no perder funcionalidad.
- `migration_map.md`: mapeo de funciones actuales hacia módulos nuevos.

## Estado actual

La generación se realiza desde `generator_refactor/` y es invocada por `main.py` / `generate_html.py`.
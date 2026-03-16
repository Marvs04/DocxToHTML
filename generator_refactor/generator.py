"""Orquestación del flujo modular con paridad respecto a generate_html.py."""

import os
import glob
from urllib.parse import quote
from docx import Document
from jinja2 import Environment, select_autoescape

from generator_refactor.docx_reader import (
	extract_class_blocks,
	find_cronograma_tables,
	find_evaluation_tables,
	parse_course_identity,
)
from generator_refactor.schedule_parser import format_week_range, parse_cronograma
from generator_refactor.section_parser import extract_sections_from_paragraphs
from generator_refactor.templates import BIBLIO_TEMPLATE, MAIN_TEMPLATE, WEEK_TEMPLATE
from generator_refactor.templates_v2 import (
	BIBLIO_TEMPLATE_V2,
	MAIN_TEMPLATE_V2,
	SOCIAL_TEMPLATE_V1,
	SOCIAL_TEMPLATE_V2,
	WEEK_TEMPLATE_V2,
)
from generator_refactor.pdf_generator import generate_pdfs_for_class as _gen_pdfs
from generator_refactor.transformers import (
	build_estrategias_cards,
	build_metodologia_cards,
	extract_rubricas_from_paragraphs,
	normalize_section_lines,
	parse_bibliografia_items,
	parse_competencias_cards,
	parse_contenidos_from_weeks_map,
	parse_evaluation_rows,
	parse_evaluation_table,
	parse_general_bibliografia,
	parse_info_general_cards,
)
from generator_refactor.writer import (
	build_class_html_name,
	build_class_output_dir,
	build_document_output_dir,
	build_week_output_dir,
	write_text_file,
)


def _rubrica_pdf_filename(title):
	"""Build the exact rubric PDF filename used by pdf_generator."""
	safe_title = title[:80].replace("/", "-").replace("\\", "-")
	return f"{safe_title}.pdf"


def _process_docx(docx_file, doc_out_dir, env, tmpl, week_tmpl, biblio_tmpl,
                  on_progress=None, social_html='', cancel_check=None):
	doc = Document(docx_file)
	class_blocks = extract_class_blocks(doc)
	if not class_blocks:
		doc_name = os.path.splitext(os.path.basename(docx_file))[0]
		class_blocks = [{'title': doc_name, 'term': 'Sin cuatrimestre', 'paragraphs': doc.paragraphs}]

	cron_tables = find_cronograma_tables(doc)
	evaluation_tables = find_evaluation_tables(doc)

	n_terms = len(set(b['term'] for b in class_blocks))
	n_classes = len(class_blocks)
	if on_progress:
		on_progress('stats', n_terms, n_classes)

	pdf_jobs = []
	for idx, class_block in enumerate(class_blocks):
		if cancel_check and cancel_check():
			return pdf_jobs
		class_name = class_block['title']
		term_name = class_block['term']
		if on_progress:
			on_progress('class', idx + 1, n_classes, class_name)
		class_code, class_name_clean = parse_course_identity(class_name)
		_, class_dir = build_class_output_dir(doc_out_dir, term_name, class_name)

		sections = extract_sections_from_paragraphs(class_block['paragraphs'])
		weeks_map = parse_cronograma(cron_tables[idx]) if idx < len(cron_tables) else {}

		weeks_map_copy = dict(weeks_map)
		for weeks, units in weeks_map_copy.items():
			if len(weeks) > 1:
				for week in weeks:
					if tuple([week]) in weeks_map:
						del weeks_map[tuple([week])]

		week_folders = [{'label': format_week_range(weeks), 'folder': format_week_range(weeks)} for weeks in weeks_map.keys()]

		info_cards = parse_info_general_cards(sections.get('info_general', ''), class_code, class_name_clean, term_name)
		descripcion_paragraphs = normalize_section_lines(sections.get('descripcion', '')) or ['[Agregar descripción del curso]']
		competencias_text = sections.get('competencias', '').strip() or '[Agregar competencias del curso]'
		competencias_cards = parse_competencias_cards(competencias_text)
		contenidos_units = parse_contenidos_from_weeks_map(weeks_map)
		bibliografia_general = parse_general_bibliografia(sections.get('bibliografia', '').strip())
		metodologia_cards = build_metodologia_cards(sections)
		estrategias_intro, estrategias_cards = build_estrategias_cards(sections)
		recursos_fixed_cards = [
			{'title': 'Biblioteca Virtual', 'body': ['Acceso a bases de datos académicas, libros y revistas especializadas para fortalecer la investigación y el aprendizaje.']},
			{'title': 'Office 365', 'body': ['Uso de herramientas colaborativas (Word, Excel, PowerPoint, OneDrive y Teams) para actividades, entregas y trabajo en equipo.']},
			{'title': 'Recursos visuales y simulaciones', 'body': ['Material audiovisual, simuladores y recursos interactivos para aplicar conceptos en contextos prácticos.']},
		]
		rubricas_titles = extract_rubricas_from_paragraphs(class_block['paragraphs'])
		rubricas_items = [
			{
				'title': r,
				'href': f"Rubricas y Cronograma/{quote(_rubrica_pdf_filename(r))}",
			}
			for r in rubricas_titles
		] or [{'title': 'Rúbricas evaluativas del curso', 'href': '#'}]
		cronograma_pdf_href = 'Rubricas y Cronograma/Cronograma.pdf'
		evaluacion_rows = []
		if idx < len(evaluation_tables):
			evaluacion_rows = parse_evaluation_table(evaluation_tables[idx])
		if not evaluacion_rows:
			evaluacion_rows = parse_evaluation_rows(sections.get('evaluacion', '').strip() or '')

		main_html = tmpl.render(
			course_name=class_name,
			course_code=class_code or 'CURSO',
			info_cards=info_cards,
			descripcion_paragraphs=descripcion_paragraphs,
			competencias_text=competencias_text,
			competencias_cards=competencias_cards,
			contenidos_units=contenidos_units,
			metodologia_cards=metodologia_cards,
			estrategias_intro=estrategias_intro,
			estrategias_cards=estrategias_cards,
			recursos_fixed_cards=recursos_fixed_cards,
			evaluacion_rows=evaluacion_rows,
			rubricas_items=rubricas_items,
			bibliografia_general=bibliografia_general,
			week_folders=week_folders,
			cronograma_pdf_href=cronograma_pdf_href,
		)
		write_text_file(os.path.join(class_dir, build_class_html_name(class_name)), main_html)

		for weeks, units in weeks_map.items():
			week_range = format_week_range(weeks)
			week_dir = build_week_output_dir(class_dir, week_range)
			for unit in units:
				html = week_tmpl.render(
					week_range=unit['unit'],
					unit_title=unit['unit'],
					resultado=unit['resultado'],
					contenidos=[c for c in unit['contenidos'].split('\n') if c != unit['unit']],
				)
				write_text_file(os.path.join(week_dir, 'index.html'), html)
				biblio_html = biblio_tmpl.render(week_range=week_range, bibliografia=parse_bibliografia_items(unit['bibliografia']))
				write_text_file(os.path.join(week_dir, 'bibliografia.html'), biblio_html)

		# Espacio social
		if social_html:
			write_text_file(os.path.join(class_dir, 'espacio_social.html'), social_html)

		pdf_jobs.append({
			'class_name': class_name,
			'doc': doc,
			'paragraphs': class_block['paragraphs'],
			'weeks_map': weeks_map,
			'class_dir': class_dir,
		})

	return pdf_jobs


def generate_file(docx_path, out_dir, on_progress=None, style='v1', cancel_check=None):
	"""Procesa un único archivo DOCX y escribe la salida en out_dir."""
	if not os.path.isfile(docx_path) or os.path.basename(docx_path).startswith("~$"):
		print(f"Archivo no válido: {docx_path}")
		return
	doc_name = os.path.splitext(os.path.basename(docx_path))[0]
	doc_out_dir = build_document_output_dir(out_dir, doc_name)
	env = Environment(autoescape=select_autoescape(['html', 'xml']))
	if style == 'v2':
		tmpl        = env.from_string(MAIN_TEMPLATE_V2)
		week_tmpl   = env.from_string(WEEK_TEMPLATE_V2)
		biblio_tmpl = env.from_string(BIBLIO_TEMPLATE_V2)
		social_html = SOCIAL_TEMPLATE_V2
	else:
		tmpl        = env.from_string(MAIN_TEMPLATE)
		week_tmpl   = env.from_string(WEEK_TEMPLATE)
		biblio_tmpl = env.from_string(BIBLIO_TEMPLATE)
		social_html = SOCIAL_TEMPLATE_V1
	# Fase 1: HTMLs
	pdf_jobs = _process_docx(docx_path, doc_out_dir, env, tmpl, week_tmpl, biblio_tmpl,
	                         on_progress=on_progress, social_html=social_html,
	                         cancel_check=cancel_check)
	# Fase 2: PDFs (al final, para que la GUI no se bloquee durante la generación HTML)
	if on_progress:
		on_progress('pdf_start', len(pdf_jobs))
	for i, job in enumerate(pdf_jobs):
		if cancel_check and cancel_check():
			break
		if on_progress:
			on_progress('pdf_item', i + 1, len(pdf_jobs), job['class_name'])
		try:
			_gen_pdfs(job['class_name'], job['doc'], job['paragraphs'],
			          job['weeks_map'], job['class_dir'])
		except Exception as _e:
			print(f"    [PDF] Error en '{job['class_name']}': {_e}")
	print(f"✓ {doc_name}  →  {doc_out_dir}")


def generate(input_dir, out_dir, style='v1'):
	docx_files = [
		path for path in glob.glob(os.path.join(input_dir, "*.docx"))
		if not os.path.basename(path).startswith("~$")
	]
	if not docx_files:
		print("Error: No se encontró ningún archivo .docx en la carpeta especificada.")
		return

	env = Environment(autoescape=select_autoescape(['html', 'xml']))
	if style == 'v2':
		tmpl        = env.from_string(MAIN_TEMPLATE_V2)
		week_tmpl   = env.from_string(WEEK_TEMPLATE_V2)
		biblio_tmpl = env.from_string(BIBLIO_TEMPLATE_V2)
		social_html = SOCIAL_TEMPLATE_V2
	else:
		tmpl        = env.from_string(MAIN_TEMPLATE)
		week_tmpl   = env.from_string(WEEK_TEMPLATE)
		biblio_tmpl = env.from_string(BIBLIO_TEMPLATE)
		social_html = SOCIAL_TEMPLATE_V1

	for docx_file in docx_files:
		doc_name = os.path.splitext(os.path.basename(docx_file))[0]
		doc_out_dir = build_document_output_dir(out_dir, doc_name)
		pdf_jobs = _process_docx(docx_file, doc_out_dir, env, tmpl, week_tmpl, biblio_tmpl,
		                         social_html=social_html)
		for job in pdf_jobs:
			try:
				_gen_pdfs(job['class_name'], job['doc'], job['paragraphs'],
				          job['weeks_map'], job['class_dir'])
			except Exception as _e:
				print(f"  [PDF] Error en '{job['class_name']}': {_e}")
		print(f"✓ {doc_name}  →  {doc_out_dir}")

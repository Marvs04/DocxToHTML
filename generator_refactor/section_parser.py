"""Extracción semántica de secciones desde párrafos del DOCX.

Migrado literalmente desde generate_html.py para mantener paridad en la fase 3.
"""

import re
import unicodedata
from collections import defaultdict


def normalize_heading(value):
	normalized = unicodedata.normalize('NFKD', value or '')
	return ''.join(ch for ch in normalized if not unicodedata.combining(ch)).strip().lower()


SECTION_KEYS = {
	'info_general': ['información general', 'informacion general', 'generalidades', 'datos del curso'],
	'descripcion': ['descripción', 'descripcion'],
	'competencias': ['competencias'],
	'contenidos': ['contenidos', 'unidad'],
	'metodologia': ['metodología', 'metodologia'],
	'estrategias': ['estrategias'],
	'recursos': ['recursos'],
	'evaluacion': ['evaluación', 'evaluacion'],
	'cronograma': ['cronograma'],
	'bibliografia': ['bibliografía', 'bibliografia'],
	'observaciones': ['observaciones generales', 'observaciones']
}


def find_section_name(par_text):
	low = par_text.lower().strip()
	for key, opts in SECTION_KEYS.items():
		for o in opts:
			pattern = rf'^{re.escape(o)}(?:\b|\s|:|,|\-|\()'
			if low == o or re.match(pattern, low):
				return key
	return None


def is_heading_like(text, style_name=''):
	t = (text or '').strip()
	if not t:
		return False
	low = t.lower()
	if style_name.startswith('heading'):
		return True
	if len(t) <= 80 and not t.endswith(('.', ';', '?', '!')):
		if any(word in low for word in ['información general', 'descripcion del curso', 'descripción del curso', 'competencias', 'contenidos temáticos', 'metodología', 'estrategias de aprendizaje', 'evaluación de los aprendizajes', 'recursos didácticos', 'cronograma', 'rúbricas evaluativas', 'bibliografía', 'observaciones generales']):
			return True
	if t.isupper() and len(t) <= 100:
		return True
	return False


def extract_sections_from_paragraphs(paragraphs):
	sections = defaultdict(list)
	last_key = None

	def is_section_subheading(text, key):
		normalized = normalize_heading(text)
		return key == 'bibliografia' and normalized in {'bibliografia obligatoria', 'bibliografia complementaria'}

	for p in paragraphs:
		t = p.text.strip()
		if not t:
			continue
		style = getattr(p, 'style', None)
		style_name = getattr(style, 'name', '').lower() if style else ''
		key = find_section_name(t)
		low = t.lower().strip()
		explicit_heading_start = re.match(r'^(informaci[oó]n|descripci[oó]n|competencias|contenidos tem[aá]ticos|metodolog[ií]a|estrategias|recursos|evaluaci[oó]n|cronograma|r[uú]bricas|bibliograf[ií]a|observaciones)', low)

		if key and not is_section_subheading(t, key) and (is_heading_like(t, style_name) or explicit_heading_start):
			last_key = key
			continue

		if is_heading_like(t, style_name):
			key = find_section_name(t)
			if key and not is_section_subheading(t, key):
				last_key = key
				continue

		if last_key:
			sections[last_key].append(t)
	return {k: '\n'.join(v) for k, v in sections.items()}


def extract_sections(doc):
	return extract_sections_from_paragraphs(doc.paragraphs)

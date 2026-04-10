"""Parsing del cronograma y de la estructura semanal.

Migrado literalmente desde generate_html.py para mantener paridad en la fase 2.
"""

import re
from collections import defaultdict


def parse_week_cell(s):
	s = s.strip().lower()
	s = s.replace('y', ',').replace('-', ',').replace('a', ',')
	nums = re.findall(r'\d+', s)
	return sorted({int(n) for n in nums}) if nums else []


def is_week_marker(value):
	low = (value or '').strip().lower()
	if not low or 'semana' in low:
		return False
	# Allow newlines/multiline format (e.g., "12\n11" or "12 y 13")
	low = low.replace('\n', ',').replace('\r', ',')
	return bool(re.fullmatch(r'\d+(?:\s*(?:y|a|-|,)\s*\d+)*', low))


def clean_intro_text(value):
	cleaned = (value or '').strip()
	cleaned = re.sub(r"^\s*introducci[oó]n(?:\s+unidad\s*\d+)?\s*:?\s*", "", cleaned, flags=re.IGNORECASE)
	return cleaned.strip()


def is_table_header_row(cells):
	normalized = [(c or '').strip().lower() for c in cells]
	joined = ' '.join(normalized)
	first = normalized[0] if normalized else ''
	second = normalized[1] if len(normalized) > 1 else ''

	if 'distribución de horas asignadas al trabajo por semana' in joined:
		return True
	if first == 'semana' and ('contenido' in second or 'contenidos' in second):
		return True
	if 'hrs sincrónicas' in joined or 'hrs asincrónicas' in joined:
		return True
	return False


def find_cronograma_table(doc):
	candidates = []
	for tbl in doc.tables:
		text_cells = [[cell.text.strip().lower() for cell in row.cells] for row in tbl.rows]
		header_line = ' '.join(text_cells[0]) if text_cells else ''
		if 'cronograma' in header_line or any('sem' in c for c in text_cells[0]):
			return tbl
		candidates.append(tbl)
	if candidates:
		return max(candidates, key=lambda t: len(t.rows))
	return None


def parse_cronograma(tbl):
	rows = tbl.rows
	weeks_map = defaultdict(list)
	current_unit_title = ''
	current_intro = ''

	start_idx = 2 if len(rows) > 2 else 0
	for idx in range(start_idx, len(rows)):
		r = rows[idx]
		cells = [c.text.strip() for c in r.cells]
		if not any(cells):
			continue

		if is_table_header_row(cells):
			continue

		first = cells[0]
		if is_week_marker(first):
			weeks = parse_week_cell(first)
			if not weeks:
				continue
			contents = cells[1] if len(cells) > 1 else ''
			bibli = cells[6] if len(cells) > 6 else ''

			unit_title = current_unit_title
			rest_contents = contents
			m = re.match(r'^(Unidad\s*\d+[:.].*?)(?:\n|$)', contents, re.IGNORECASE)
			if m:
				unit_title = m.group(1).strip()
				rest_contents = contents[m.end():].strip()

			resultado = current_intro

			entry = {
				'unit': unit_title,
				'resultado': resultado,
				'contenidos': rest_contents,
				'bibliografia': bibli,
			}
			weeks_map[tuple(weeks)].append(entry)
		else:
			for cell_value in cells:
				m_title = re.search(r'(Unidad\s*\d+\.[^\n\r]*)', cell_value, re.IGNORECASE)
				if m_title:
					current_unit_title = m_title.group(1).strip()
					break

			intro_candidate = ''
			for cell_value in cells:
				if re.search(r'introducci[oó]n', cell_value, re.IGNORECASE):
					intro_candidate = clean_intro_text(cell_value)
					break

			if not intro_candidate and len(cells) > 1:
				fallback = clean_intro_text(cells[1])
				if fallback and fallback.lower() not in {'contenidos', 'contenido', 'semana', 'bibliografía', 'bibliografia'}:
					intro_candidate = fallback

			if intro_candidate and intro_candidate.lower() not in {'introducción', 'introduccion', 'contenidos', 'contenido'}:
				current_intro = intro_candidate

	return weeks_map


def format_week_range(weeks):
	if len(weeks) == 1:
		return f"Semana {weeks[0]}"
	return f"Semana {' y '.join(map(str, weeks))}"

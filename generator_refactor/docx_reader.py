"""Lectura de documentos DOCX y localización de bloques del curso.

Migrado literalmente desde generate_html.py para mantener paridad en la fase 1.
"""

import re


def parse_term_heading(text):
	low = (text or '').strip().lower()
	m = re.search(r'(primer|segundo|tercer|cuarto|quinto|sexto|s[eé]ptimo|octavo|noveno|d[eé]cimo)\s+cuatrimestre', low)
	if not m:
		return None
	word = m.group(1)
	norm = {
		'primer': 'Primer',
		'segundo': 'Segundo',
		'tercer': 'Tercer',
		'cuarto': 'Cuarto',
		'quinto': 'Quinto',
		'sexto': 'Sexto',
		'séptimo': 'Séptimo',
		'septimo': 'Séptimo',
		'octavo': 'Octavo',
		'noveno': 'Noveno',
		'décimo': 'Décimo',
		'decimo': 'Décimo',
	}.get(word, word.capitalize())
	return f"{norm} Cuatrimestre"


def is_class_title(text):
	t = (text or '').strip()
	return bool(re.match(r'^[A-ZÁÉÍÓÚÑ]{2,}\d{3,}[a-zA-Z]?\s+.+', t))


def extract_class_blocks(doc):
	blocks = []
	current_term = 'Sin cuatrimestre'
	class_starts = []

	for idx, p in enumerate(doc.paragraphs):
		t = p.text.strip()
		if not t:
			continue
		term = parse_term_heading(t)
		if term:
			current_term = term
			continue
		if is_class_title(t):
			class_starts.append((idx, t, current_term))

	for i, (start_idx, title, term) in enumerate(class_starts):
		end_idx = class_starts[i + 1][0] if i + 1 < len(class_starts) else len(doc.paragraphs)
		blocks.append({
			'title': title,
			'term': term,
			'paragraphs': doc.paragraphs[start_idx:end_idx],
		})

	return blocks


def is_cronograma_table(tbl):
	for row in tbl.rows[:3]:
		joined = ' '.join(cell.text.strip().lower() for cell in row.cells)
		if 'semana' in joined and ('contenido' in joined or 'materiales' in joined):
			return True
	return False


def find_cronograma_tables(doc):
	return [tbl for tbl in doc.tables if is_cronograma_table(tbl)]


def parse_course_identity(class_title):
	t = (class_title or '').strip()
	m = re.match(r'^([A-ZÁÉÍÓÚÑ]{2,}\d{3,}[a-zA-Z]?)\s+(.+)$', t)
	if m:
		return m.group(1).strip(), m.group(2).strip()
	return '', t


def is_evaluation_table(tbl):
	if not tbl.rows:
		return False
	first_row = ' '.join(c.text.strip().lower() for c in tbl.rows[0].cells)
	return 'rubros' in first_row and 'porcentaje' in first_row


def find_evaluation_tables(doc):
	return [tbl for tbl in doc.tables if is_evaluation_table(tbl)]


def extract_rubricas_with_tables(doc, paragraphs):
	"""Devuelve lista de {'title': str, 'table': Table|None} para cada rúbrica detectada."""
	body = doc.element.body
	elements = list(body)

	# Índices por identidad de elemento XML — estable entre múltiples llamadas a doc.paragraphs
	para_elem_to_idx = {el: i for i, el in enumerate(elements) if el.tag.endswith('}p')}
	tbl_elem_to_obj  = {t._element: t for t in doc.tables}

	results = []
	in_rubricas = False

	for p in paragraphs:
		t = p.text.strip()
		low = t.lower()
		if 'rúbricas evaluativas' in low or 'rubricas evaluativas' in low:
			in_rubricas = True
			continue
		if in_rubricas and ('bibliograf' in low or 'observaciones generales' in low):
			break
		if in_rubricas and ('rúbrica para evaluar' in low or 'rubrica para evaluar' in low):
			elem_idx = para_elem_to_idx.get(p._element)
			rubrica_table = None
			if elem_idx is not None:
				for el in elements[elem_idx + 1:]:
					tag = el.tag.split('}')[-1] if '}' in el.tag else el.tag
					if tag == 'tbl':
						rubrica_table = tbl_elem_to_obj.get(el)
						break
					elif tag == 'p':
						# Saltar párrafos vacíos; parar ante texto antes de la tabla
						inner = ''.join(r.text or '' for r in el.iter() if r.tag.endswith('}t')).strip()
						if inner:
							break
			results.append({'title': t, 'table': rubrica_table})

	return results

"""Transformación de texto y tablas a estructuras listas para renderizar.

Migrado literalmente desde generate_html.py para mantener paridad en la fase 4.
"""

import re

from generator_refactor.section_parser import normalize_heading


def normalize_section_lines(value):
	if not value:
		return []
	return [line.strip() for line in value.split('\n') if line.strip()]


def parse_info_general_cards(info_text, class_code, class_name, term_name):
	lines = normalize_section_lines(info_text)
	parsed = {}
	for line in lines:
		m = re.match(r'^([^:]{2,60}):\s*(.+)$', line)
		if m:
			parsed[m.group(1).strip().lower()] = m.group(2).strip()

	def get_field(*keys, default=''):
		for k in keys:
			if k in parsed and parsed[k]:
				return parsed[k]
		return default

	cards = [
		{'label': 'Código del curso', 'value': get_field('código del curso', 'codigo del curso', default=class_code), 'wide': False},
		{'label': 'Nombre del curso', 'value': get_field('nombre del curso', default=class_name), 'wide': False},
		{'label': 'Créditos', 'value': get_field('créditos', 'creditos', default='3'), 'wide': False},
		{'label': 'Duración', 'value': get_field('duración', 'duracion', default='15 semanas – cuatrimestral'), 'wide': False},
		{'label': 'Distribución de horas virtuales por semana', 'value': get_field('distribución de horas virtuales por semana', 'distribucion de horas virtuales por semana', default='9 horas distribuidas en: 2 horas sincrónicas, 1 hora de práctica virtual y 6 horas de trabajo independiente virtual.'), 'wide': True},
		{'label': 'Modalidad', 'value': get_field('modalidad', default='Virtual'), 'wide': False},
		{'label': 'Naturaleza', 'value': get_field('naturaleza', default='Teórico-práctico'), 'wide': False},
		{'label': 'Ubicación', 'value': get_field('ubicación', 'ubicacion', default=term_name), 'wide': False},
		{'label': 'Requisitos', 'value': get_field('requisitos', default='No tiene'), 'wide': False},
		{'label': 'Correquisitos', 'value': get_field('correquisitos', default='No tiene'), 'wide': False},
		{'label': 'Nivel', 'value': get_field('nivel', default='Maestría profesional'), 'wide': False},
		{'label': 'Profesor', 'value': get_field('profesor', default='[Nombre del profesor]'), 'wide': False},
	]
	return cards


def parse_contenidos_from_weeks_map(weeks_map):
	units = []
	seen = set()
	for _, entries in weeks_map.items():
		for entry in entries:
			title = (entry.get('unit') or '').strip()
			if not title or title in seen:
				continue
			seen.add(title)
			items = [x.strip() for x in (entry.get('contenidos') or '').split('\n') if x.strip()]
			units.append({'title': title, 'items': items})
	return units


def split_clean_lines(value):
	if not value:
		return []
	lines = [line.strip() for line in value.replace('\r', '\n').split('\n') if line.strip()]
	return lines


def build_text_cards(value):
	lines = split_clean_lines(value)
	cards = []
	current_title = ''
	current_body = []

	for line in lines:
		if line.endswith(':') and len(line) < 90:
			if current_title or current_body:
				cards.append({'title': current_title or 'Punto clave', 'body': current_body[:]})
			current_title = line[:-1].strip()
			current_body = []
		else:
			if not current_title and not current_body:
				current_title = 'Punto clave'
			current_body.append(line)

	if current_title or current_body:
		cards.append({'title': current_title or 'Punto clave', 'body': current_body[:]})

	if not cards:
		cards = [{'title': 'Punto clave', 'body': ['[Sin información disponible]']}]
	return cards


def parse_evaluation_rows(evaluacion_text):
	lines = split_clean_lines(evaluacion_text)
	rows = []
	seen = set()

	for line in lines:
		low = line.lower()
		if any(k in low for k in ['criterios de desempeño', 'resultados de aprendizaje', 'nivel de logro y evidencias']):
			continue

		actividad = ''
		criterio = ''
		if re.search(r'evidencia\s*:', line, re.IGNORECASE):
			parts = re.split(r'evidencia\s*:\s*', line, flags=re.IGNORECASE, maxsplit=1)
			actividad = parts[0].strip(' .;-')
			criterio = parts[1].strip() if len(parts) > 1 else 'Ver detalle en la guía de evaluación.'
		elif any(k in low for k in ['taller', 'portafolio', 'prueba', 'proyecto', 'foro', 'examen', 'presentación', 'presentacion']):
			actividad = line.strip(' .;-')
			criterio = 'Ver rúbrica del curso.'

		if actividad:
			key = actividad.lower()
			if key not in seen:
				seen.add(key)
				rows.append({'actividad': actividad, 'criterio': criterio, 'porcentaje': '-'})

	if not rows:
		rows.append({'actividad': 'Seguimiento de actividades del curso', 'criterio': 'Evaluación continua según rúbricas publicadas.', 'porcentaje': '-'})

	return rows


def gather_bibliografia_items(weeks_map):
	items = []
	seen = set()
	for _, entries in weeks_map.items():
		for entry in entries:
			parsed = parse_bibliografia_items(entry.get('bibliografia', ''))
			for item in parsed:
				key = (item.get('text', '').strip().lower(), (item.get('url') or '').strip().lower())
				if key in seen:
					continue
				seen.add(key)
				items.append({'text': item.get('text', ''), 'url': item.get('url')})
	return items


def parse_evaluation_table(tbl):
	rows = []
	for r in tbl.rows[1:]:
		cells = [c.text.strip() for c in r.cells]
		if not any(cells):
			continue
		rubro = cells[0] if len(cells) > 0 else ''
		pct = cells[1] if len(cells) > 1 else ''
		if not rubro:
			continue
		if rubro.lower() == 'total':
			continue
		rows.append({'actividad': rubro, 'criterio': 'Ver rúbrica del curso.', 'porcentaje': pct or '-'})
	return rows


def build_labeled_cards(text, default_title='Punto clave'):
	lines = split_clean_lines(text)
	if not lines:
		return [{'title': default_title, 'body': ['[Sin información disponible]']}]

	heading_markers = {
		'competencia general',
		'competencias específicas',
		'competencias especificas',
		'criterios de desempeño',
		'resultados de aprendizaje',
		'resultados de aprendizaje, nivel de logro y evidencias',
		'instrucciones',
		'metodología',
		'metodologia',
		'estrategias',
		'recursos',
	}

	cards = []
	current_title = default_title
	current_body = []

	for line in lines:
		low = line.lower().strip(' :')
		is_heading = (
			low in heading_markers
			or line.endswith(':')
			or (len(line) < 80 and not any(ch in line for ch in '.;!?') and low.startswith(('competencia', 'criterios', 'resultados', 'instrucciones', 'metod', 'estrateg', 'recurso')))
		)

		if is_heading:
			if current_body:
				cards.append({'title': current_title, 'body': current_body[:]})
				current_body = []
			current_title = line.rstrip(':')
			continue

		current_body.append(line)

	if current_body:
		cards.append({'title': current_title, 'body': current_body[:]})

	if not cards:
		cards = [{'title': default_title, 'body': lines}]

	return cards


def parse_competencias_cards(text):
	lines = split_clean_lines(text)
	if not lines:
		return [{'title': 'Competencias', 'body': ['[Agregar competencias del curso]']}]

	cards = []
	current_title = 'Competencias'
	current_body = []

	markers = [
		'competencia general',
		'competencias específicas',
		'competencias especificas',
		'criterios de desempeño',
		'resultados de aprendizaje, nivel de logro y evidencias',
		'resultados de aprendizaje',
	]

	for line in lines:
		low = line.lower().strip(' :')
		if low in markers:
			if current_body:
				cards.append({'title': current_title, 'body': current_body[:]})
				current_body = []
			current_title = line.rstrip(':')
			continue
		current_body.append(line)

	if current_body:
		cards.append({'title': current_title, 'body': current_body[:]})

	return cards or [{'title': 'Competencias', 'body': lines}]


def extract_rubricas_from_paragraphs(paragraphs):
	lines = [p.text.strip() for p in paragraphs if p.text.strip()]
	rubricas = []
	rubrica_re = re.compile(r"^r[úu]bricas?\b", re.IGNORECASE)
	for line in lines:
		low = line.lower()
		is_short = len(line) < 80
		if is_short and (low.startswith('bibliograf') or low.startswith('observaciones')):
			break
		if is_short and (low.startswith('rúbricas evaluativas') or low.startswith('rubricas evaluativas')):
			continue
		if rubrica_re.match(line):
			rubricas.append(line)
	return rubricas


def build_metodologia_cards(sections):
	metodologia = sections.get('metodologia', '').strip()
	estrategias = sections.get('estrategias', '').strip()

	if metodologia:
		return build_labeled_cards(metodologia, default_title='Enfoque metodológico')

	estr_lines = split_clean_lines(estrategias)
	if estr_lines:
		seed = '\n'.join(estr_lines[:2])
		return build_labeled_cards(seed, default_title='Enfoque metodológico')

	return [{'title': 'Enfoque metodológico', 'body': ['[Agregar metodología del curso]']}]


def build_estrategias_cards(sections):
	estrategias = sections.get('estrategias', '').strip()
	if not estrategias:
		return '', [{'title': 'Estrategia de aprendizaje', 'body': ['[Agregar estrategias de aprendizaje]'], 'instructions': []}]

	lines = split_clean_lines(estrategias)
	intro = []
	cards = []
	current_card = None
	current_target = 'body'

	def is_strategy_title_candidate(line, next_line=''):
		normalized = normalize_heading(line).strip(' :')
		if not normalized or normalized in {'estrategias', 'estrategias de aprendizaje', 'instrucciones'}:
			return False
		if len(line) > 120 or line.endswith(('.', ';', ':', '?', '!')):
			return False
		if normalized.startswith(('las estrategias', 'la estrategia', 'estas estrategias', 'el curso', 'los estudiantes', 'permite', 'permite a')):
			return False
		if re.match(r'^\d+[.)-]\s+', line):
			return True

		words = [word for word in re.split(r'\s+', line) if word]
		if len(words) > 10:
			return False

		title_like_words = sum(
			1 for word in words
			if word[:1].isupper() or normalize_heading(word) in {'de', 'del', 'la', 'el', 'y', 'con', 'para', 'en', 'ia'}
		)
		next_normalized = normalize_heading(next_line)
		next_is_body = bool(next_line) and (
			next_line.endswith(('.', ';', '?', '!'))
			or len(next_line) > 80
			or next_normalized.startswith('instrucciones')
		)
		return next_is_body and title_like_words >= max(1, len(words) - 2)

	def flush_current_card():
		nonlocal current_card
		if not current_card:
			return
		if not current_card['body']:
			current_card['body'] = ['[Agregar descripción de la estrategia]']
		cards.append(current_card)
		current_card = None

	for index, line in enumerate(lines):
		normalized = normalize_heading(line).strip(' :')
		next_line = lines[index + 1] if index + 1 < len(lines) else ''

		if normalized.startswith('instrucciones'):
			if current_card is None:
				current_card = {'title': 'Estrategia de aprendizaje', 'body': [], 'instructions': []}
			current_target = 'instructions'
			continue

		if is_strategy_title_candidate(line, next_line):
			flush_current_card()
			current_card = {'title': line, 'body': [], 'instructions': []}
			current_target = 'body'
			continue

		if current_card is None:
			intro.append(line)
			continue

		current_card[current_target].append(line)

	flush_current_card()

	if not cards:
		cards = build_labeled_cards(estrategias, default_title='Estrategia de aprendizaje')
		cards = [{'title': card['title'], 'body': card['body'], 'instructions': []} for card in cards]

	return '\n'.join(intro).strip(), cards


def build_recursos_cards(sections, bibliografia_general):
	recursos = sections.get('recursos', '').strip()
	if recursos:
		return build_labeled_cards(recursos, default_title='Recurso didáctico')

	refs = []
	if isinstance(bibliografia_general, dict):
		refs = bibliografia_general.get('obligatoria', []) + bibliografia_general.get('complementaria', [])
	elif bibliografia_general:
		refs = bibliografia_general

	if refs:
		return [
			{'title': 'Bibliografía base', 'body': [item['text'] for item in refs[:4]]},
			{'title': 'Biblioteca virtual', 'body': ['Utilice los botones de acceso directo en la sección Bibliografía y Biblioteca Virtual.']},
		]

	return [{'title': 'Recurso didáctico', 'body': ['[Agregar recursos didácticos]']}]


def parse_bibliografia_items(raw_text):
	if not raw_text:
		return []

	lines = [line.strip() for line in re.split(r'\n+', raw_text) if line.strip()]
	items = []
	pending_text = None

	for line in lines:
		low = line.lower()
		if 'material de consulta y aprendizaje' in low or 'disponible en la sección semanal' in low:
			continue

		urls = re.findall(r'https?://\S+', line)
		text_without_urls = re.sub(r'https?://\S+', '', line).strip(' .;')

		if urls and not text_without_urls:
			if items and not items[-1].get('url'):
				items[-1]['url'] = urls[0]
			elif pending_text:
				items.append({'text': pending_text, 'url': urls[0]})
				pending_text = None
			continue

		if urls and text_without_urls:
			items.append({'text': text_without_urls, 'url': urls[0]})
			pending_text = None
			continue

		if pending_text:
			pending_text = f"{pending_text} {line}".strip()
		else:
			pending_text = line

	if pending_text:
		items.append({'text': pending_text, 'url': None})

	return [it for it in items if it.get('text')]


def parse_general_bibliografia(raw_text):
	lines = split_clean_lines(raw_text)
	obligatoria_lines = []
	complementaria_lines = []
	current_section = None
	saw_explicit_section = False

	for line in lines:
		normalized = normalize_heading(line)
		if normalized == 'bibliografia':
			continue
		if normalized.startswith('bibliografia obligatoria'):
			current_section = 'obligatoria'
			saw_explicit_section = True
			continue
		if normalized.startswith('bibliografia complementaria'):
			current_section = 'complementaria'
			saw_explicit_section = True
			continue
		if normalized.startswith('observaciones generales'):
			break

		if current_section == 'complementaria':
			complementaria_lines.append(line)
		else:
			obligatoria_lines.append(line)

	if not saw_explicit_section and not obligatoria_lines and lines:
		obligatoria_lines = lines[:]

	obligatoria = parse_bibliografia_items('\n'.join(obligatoria_lines))
	complementaria = parse_bibliografia_items('\n'.join(complementaria_lines))

	if not obligatoria:
		obligatoria = [{'text': 'Sin referencias bibliográficas obligatorias disponibles.', 'url': None}]
	if not complementaria:
		complementaria = [{'text': 'Sin referencias bibliográficas complementarias disponibles.', 'url': None}]

	return {
		'obligatoria': obligatoria,
		'complementaria': complementaria,
	}

"""Escritura de archivos y organización de salida.

Migrado incrementalmente desde generate_html.py para mantener paridad en la fase 6.
"""

import os
import re
import sys


def safe_name(value):
	return re.sub(r'[<>:"/\\|?*]', '_', (value or '').strip())


def _win_long(path):
	# Prefijo extendido de Windows para rutas > 260 caracteres
	if sys.platform != "win32":
		return path
	path = os.path.abspath(path)
	if not path.startswith("\\\\?\\"):
		path = "\\\\?\\" + path
	return path


def ensure_directory(path):
	os.makedirs(_win_long(path), exist_ok=True)
	return path


def build_document_output_dir(out_dir, doc_name):
	return ensure_directory(os.path.join(out_dir, safe_name(doc_name)))


def build_class_output_dir(doc_out_dir, term_name, class_name):
	term_dir = os.path.join(doc_out_dir, safe_name(term_name))
	class_dir = os.path.join(term_dir, safe_name(class_name))
	ensure_directory(class_dir)
	return term_dir, class_dir


def build_week_output_dir(class_dir, week_range):
	return ensure_directory(os.path.join(class_dir, week_range))


def build_class_html_name(class_name):
	return f"{safe_name(class_name)}.html"


def write_text_file(path, content):
	with open(_win_long(path), 'w', encoding='utf-8') as file_handle:
		file_handle.write(content)

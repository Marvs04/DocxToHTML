"""Templates Jinja del generador.

Migrados literalmente desde generate_html.py para mantener paridad en la fase 5.
"""

MAIN_TEMPLATE = """

<!-- Acordeón maestro | Generalidades -->
<div class="card shadow-sm border-0 mb-3" style="border-left: 8px solid #002E62; border-radius: 14px;">
	<div class="card-body" style="padding: 1rem 1.1rem;">
		<div style="display: flex; align-items: center; justify-content: space-between; gap: .75rem; flex-wrap: wrap;">
			<div style="display: flex; align-items: center; gap: .6rem;"><span style="font-size: 1.25rem; line-height: 1;">🧭</span>
				<h3 class="h5 m-0" style="color: #002e62;">Generalidades del curso</h3>
			</div>
			<span class="badge badge-pill" style="background: #FDC82C; color: #002e62; font-weight: bold;"> Sección General </span>
		</div>
		<div style="margin-top: .6rem; background: #e9f5ee; border-left: 6px solid #6fbf73; padding: .7rem .9rem; border-radius: 10px;">Aquí encontrarás la información esencial para iniciar el curso con claridad.</div>

		<details style="margin-top: .9rem; border: 1px solid rgba(0,46,98,.12); border-radius: 12px; overflow: hidden;">
			<summary style="cursor: pointer; list-style: none; padding: .9rem 1rem; background: #f7f9fc; display: flex; align-items: center; justify-content: space-between; gap: 1rem;">
				<span style="width: 34px; height: 34px; display: inline-flex; align-items: center; justify-content: center; border-radius: 10px; background: rgba(0,46,98,.08);">📌</span>
				<strong style="color: #002e62; font-size: 1rem;">Información general del curso</strong><span style="color: #002e62; font-weight: bold; opacity: .75;">Abrir / Cerrar</span>
			</summary>
			<div style="padding: 1rem 1rem .9rem 1rem; background: #ffffff;">
				<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: .75rem; margin-bottom: .85rem;">
					{% for card in info_cards %}
					<div style="background: #ffffff; border: 1px solid rgba(0,46,98,.10); border-radius: 12px; padding: .8rem .9rem;{% if card.wide %} grid-column: 1 / -1; border-left: 6px solid #002E62; background: #f7f9fc;{% endif %}">
						<div style="font-size: .85rem; color: #64748b;">{{ card.label }}</div>
						<div style="font-weight: bold; color: #0f172a;">{{ card.value }}</div>
					</div>
					{% endfor %}
				</div>
				<div style="border-top: 1px dashed rgba(0,46,98,.18); padding-top: .85rem;">
					<div style="font-weight: bold; color: #002e62; margin-bottom: .35rem;">Horario de atención</div>
					<div style="color: #334155;">[Ej.: Lunes y miércoles 6:00 p.m. – 7:00 p.m. | Modalidad: virtual]</div>
					<div style="margin-top: .75rem; font-weight: bold; color: #002e62; margin-bottom: .35rem;">Canales oficiales</div>
					<ul style="margin: .2rem 0 0 1.1rem; color: #334155;">
						<li>Avisos del curso (foros/comunicados)</li>
						<li>Mensajería interna de la plataforma</li>
						<li>Sesiones sincrónicas (si aplica)</li>
					</ul>
				</div>
			</div>
		</details>

		<details style="margin-top: .75rem; border: 1px solid rgba(0,46,98,.12); border-radius: 12px; overflow: hidden;">
			<summary style="cursor: pointer; list-style: none; padding: .9rem 1rem; background: #f7f9fc; display: flex; align-items: center; justify-content: space-between; gap: 1rem;">
				<span style="width: 34px; height: 34px; display: inline-flex; align-items: center; justify-content: center; border-radius: 10px; background: rgba(0,46,98,.08);">📝</span>
				<strong style="color: #002e62; font-size: 1rem;">Descripción del curso</strong><span style="color: #002e62; font-weight: bold; opacity: .75;">Abrir / Cerrar</span>
			</summary>
			<div style="padding: 1rem 1rem .95rem 1rem; background: #ffffff;">
				<div style="background: #ffffff; border: 1px solid rgba(0,46,98,.10); border-radius: 12px; padding: .95rem 1rem; color: #334155; line-height: 1.55;">
					{% for p in descripcion_paragraphs %}<p style="margin-bottom: .8rem;">{{ p }}</p>{% endfor %}
				</div>
			</div>
		</details>
	</div>
</div>

<div class="card shadow-sm border-0 mb-3" style="border-left: 8px solid #002E62;">
	<div class="card-body py-3">
		<div class="d-flex align-items-center justify-content-between flex-wrap gap-2">
			<h3 class="h5 m-0" style="color: #002e62;">🎯 Competencias, elementos y resultados de aprendizaje</h3>
			<span class="badge badge-pill" style="background: #FDC82C; color: #002e62;">{{ course_code }}</span>
		</div>
		<div style="margin-top: .35rem; color: #475569; font-size: 14.5px;">En esta sección se presentan las competencias del curso con un diseño de lectura fácil.</div>
		<hr class="my-3" style="border-top: 2px solid #002E62; opacity: .15;">
		<details style="background: #ffffff; border: 1px solid rgba(0,46,98,.12); border-radius: 12px; overflow: hidden;">
			<summary style="cursor: pointer; list-style: none; padding: .9rem 1rem; background: #f7f9fc; display: flex; align-items: center; justify-content: space-between; gap: 1rem; border-left: 6px solid #002E62;">
				<span style="font-size: 1.05rem; color: #0f172a;">▸</span> <strong style="color: #002e62; font-size: 1rem;">Ver competencias</strong> <span style="color: #64748b; font-weight: bold; font-size: 0.9rem;">Abrir / Cerrar</span>
			</summary>
			<div style="padding: 1rem; display:flex; flex-wrap:wrap; gap:.85rem;">
				{% for card in competencias_cards %}
				<div style="flex:1 1 320px; background:#ffffff; border:1px solid rgba(0,46,98,.10); border-left:6px solid #002E62; border-radius:12px; padding:.95rem 1rem; box-shadow:0 2px 8px rgba(0,0,0,.03);">
					<div style="font-weight:800; color:#002e62; margin-bottom:.35rem;">{{ card.title }}</div>
					<ul style="margin:0; padding-left:1.1rem; color:#334155; line-height:1.5;">{% for line in card.body %}<li style="margin-bottom:.35rem;">{{ line }}</li>{% endfor %}</ul>
				</div>
				{% endfor %}
			</div>
		</details>
	</div>
</div>

<div class="card shadow-sm border-0 mb-3" style="border-left: 8px solid #002E62;">
	<div class="card-body py-3">
		<div class="d-flex align-items-center justify-content-between flex-wrap gap-2">
			<h3 class="h5 m-0" style="color: #002e62;">🧾 Contenidos del curso (resumen)</h3>
			<span class="badge badge-pill" style="background: #FDC82C; color: #002e62;">{{ course_code }}</span>
		</div>
		<div style="margin-top: .35rem; color: #475569; font-size: 14.5px;">Se presenta un panorama de las unidades y temas del curso.</div>
		<hr class="my-3" style="border-top: 2px solid #002E62; opacity: .15;">
		<details style="background: #f7f9fc; border: 1px solid rgba(0,46,98,.10); border-radius: 12px; overflow: hidden;">
			<summary style="cursor: pointer; list-style: none; padding: .85rem 1rem; background: #ffffff; display: flex; align-items: center; justify-content: space-between; gap: 1rem; border-left: 6px solid #002E62;">
				<span style="font-size: 1.15rem;">▸</span> <strong style="color: #002e62;">Ver contenidos por unidades</strong><span style="color: #64748b; font-weight: 600;">Abrir / Cerrar</span>
			</summary>
			<div style="padding: 1rem;">
				<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: .85rem;">
					{% for unit in contenidos_units %}
					<div style="background: #ffffff; border: 1px solid rgba(0,46,98,.10); border-radius: 12px; padding: .9rem 1rem;">
						<div style="font-weight: 800; color: #002e62; margin-bottom:.5rem;">{{ unit['title'] }}</div>
						<ul style="margin: 0; padding-left: 1.1rem; color: #0f172a; line-height: 1.5;">{% for item in unit['items'] %}<li>{{ item }}</li>{% endfor %}</ul>
					</div>
					{% endfor %}
				</div>
			</div>
		</details>
	</div>
</div>

<div class="card shadow-sm border-0 mb-3" style="border-left: 8px solid #002E62;">
	<div class="card-body py-3">
		<div class="d-flex align-items-center justify-content-between flex-wrap gap-2">
			<h3 class="h5 m-0" style="color: #002e62;">🧭 Metodología</h3>
			<span class="badge badge-pill" style="background: #FDC82C; color: #002e62;">{{ course_code }}</span>
		</div>
		<div style="margin-top: .35rem; color: #475569; font-size: 14.5px;">En esta sección se describe el enfoque metodológico que guiará el desarrollo del curso.</div>
		<hr class="my-3" style="border-top: 2px solid #002E62; opacity: .12;">
		<details style="background: #f7f9fc; border: 1px solid rgba(0,46,98,.10); border-radius: 12px; overflow: hidden;">
			<summary style="cursor: pointer; list-style: none; padding: .9rem 1rem; background: #ffffff; display: flex; align-items: center; justify-content: space-between; gap: 1rem; border-left: 6px solid #002E62;">
				<span style="font-size: 1.05rem; color: #0f172a;">▸</span> <strong style="color: #002e62; font-size: 1rem;">Ver metodología del curso</strong><span style="color: #64748b; font-weight: bold;">Abrir / Cerrar</span>
			</summary>
			<div style="padding: 1rem; display:flex; flex-wrap:wrap; gap:.85rem;">
				{% for card in metodologia_cards %}
				<div style="flex: 1 1 280px; background:#ffffff; border:1px solid rgba(0,46,98,.10); border-left:6px solid #6fbf73; border-radius:12px; padding:.95rem 1rem;">
					<div style="font-weight:800; color:#0f172a; margin-bottom:.35rem;">{{ card.title }}</div>
					{% for line in card.body %}<div style="color:#334155; line-height:1.5; margin-bottom:.25rem;">{{ line }}</div>{% endfor %}
				</div>
				{% endfor %}
			</div>
		</details>
	</div>
</div>

<div class="card shadow-sm border-0 mb-3" style="border-left: 8px solid #002E62;">
	<div class="card-body py-3">
		<div class="d-flex align-items-center justify-content-between flex-wrap gap-2">
			<h3 class="h5 m-0" style="color: #002e62;">🧠 Estrategias de aprendizaje</h3>
			<span class="badge badge-pill" style="background: #FDC82C; color: #002e62;">{{ course_code }}</span>
		</div>
		<div style="margin-top: .35rem; color: #475569; font-size: 14.5px;">En esta sección se describen las estrategias de aprendizaje que guían el desarrollo del curso.</div>
		<hr class="my-3" style="border-top: 2px solid #002E62; opacity: .12;">
		<details style="background: #f7f9fc; border: 1px solid rgba(0,46,98,.10); border-radius: 12px; overflow: hidden;">
			<summary style="cursor: pointer; list-style: none; padding: .9rem 1rem; background: #ffffff; display: flex; align-items: center; justify-content: space-between; gap: 1rem; border-left: 6px solid #002E62;">
				<span style="font-size: 1.05rem; color: #0f172a;">▸</span> <strong style="color: #002e62; font-size: 1rem;">Ver estrategias de aprendizaje</strong><span style="color: #64748b; font-weight: bold;">Abrir / Cerrar</span>
			</summary>
			<div style="padding: 1rem;">
				{% if estrategias_intro %}
				<div style="margin-bottom: .95rem; background: #fff8e1; border: 1px solid rgba(253,200,44,.55); border-left: 6px solid #FDC82C; border-radius: 12px; padding: .95rem 1rem; color: #6b4f00; line-height: 1.55;">{{ estrategias_intro }}</div>
				{% endif %}
				<div style="display:flex; flex-wrap:wrap; gap:.85rem;">
					{% for card in estrategias_cards %}
					<div style="flex: 1 1 320px; background:#ffffff; border:1px solid rgba(0,46,98,.10); border-left:6px solid #FDC82C; border-radius:12px; padding:.95rem 1rem; box-shadow:0 2px 8px rgba(0,0,0,.03);">
						<div style="font-weight:800; color:#0f172a; margin-bottom:.45rem;">{{ card.title }}</div>
						{% for line in card.body %}<div style="color:#334155; line-height:1.5; margin-bottom:.35rem;">{{ line }}</div>{% endfor %}
						{% if card.instructions %}
						<div style="margin-top:.85rem; font-weight:800; color:#002e62;">Instrucciones</div>
						<ol style="margin:.45rem 0 0 1.1rem; padding-left:.65rem; color:#334155; line-height:1.55;">
							{% for line in card.instructions %}<li style="margin-bottom:.35rem;">{{ line }}</li>{% endfor %}
						</ol>
						{% endif %}
					</div>
					{% endfor %}
				</div>
			</div>
		</details>
	</div>
</div>

<div class="card shadow-sm border-0 mb-3" style="border-left: 8px solid #002E62;">
	<div class="card-body py-3">
		<div class="d-flex align-items-center justify-content-between flex-wrap gap-2">
			<h3 class="h5 m-0" style="color: #002e62;">🧰 Recursos didácticos</h3>
			<span class="badge badge-pill" style="background: #FDC82C; color: #002e62;">{{ course_code }}</span>
		</div>
		<div style="margin-top: .35rem; color: #475569; font-size: 14.5px;">Recursos y herramientas que se utilizarán para desarrollar las actividades del curso.</div>
		<hr class="my-3" style="border-top: 2px solid #002E62; opacity: .12;">
		<details style="background: #f7f9fc; border: 1px solid rgba(0,46,98,.10); border-radius: 12px; overflow: hidden;">
			<summary style="cursor: pointer; list-style: none; padding: .9rem 1rem; background: #ffffff; display: flex; align-items: center; justify-content: space-between; gap: 1rem; border-left: 6px solid #002E62;">
				<span style="font-size: 1.05rem; color: #0f172a;">▸</span> <strong style="color: #002e62; font-size: 1rem;">Ver recursos didácticos del curso</strong><span style="color: #64748b; font-weight: bold;">Abrir / Cerrar</span>
			</summary>
			<div style="padding: 1rem; display:flex; flex-wrap:wrap; gap:.85rem;">
				{% for card in recursos_fixed_cards %}
				<div style="flex: 1 1 280px; background:#ffffff; border:1px solid rgba(0,46,98,.10); border-left:6px solid #0ea5e9; border-radius:12px; padding:.95rem 1rem;">
					<div style="font-weight:800; color:#0f172a; margin-bottom:.35rem;">{{ card.title }}</div>
					{% for line in card.body %}<div style="color:#334155; line-height:1.5; margin-bottom:.25rem;">{{ line }}</div>{% endfor %}
				</div>
				{% endfor %}
			</div>
		</details>
	</div>
</div>

<div class="card shadow-sm border-0 mb-3" style="border-left: 8px solid #002E62;">
	<div class="card-body py-3">
		<div class="d-flex align-items-center justify-content-between flex-wrap gap-2">
			<h3 class="h5 m-0" style="color: #002e62;">✅ Evaluación de los aprendizajes</h3>
			<span class="badge badge-pill" style="background: #FDC82C; color: #002e62;">{{ course_code }}</span>
		</div>
		<div style="margin-top: .35rem; color: #475569; font-size: 14.5px;">Tabla resumen de actividades y criterios de evaluación del curso.</div>
		<hr class="my-3" style="border-top: 2px solid #002E62; opacity: .12;">
		<details style="background: #f7f9fc; border: 1px solid rgba(0,46,98,.10); border-radius: 12px; overflow: hidden;">
			<summary style="cursor: pointer; list-style: none; padding: .9rem 1rem; background: #ffffff; display: flex; align-items: center; justify-content: space-between; gap: 1rem; border-left: 6px solid #002E62;">
				<span style="font-size: 1.05rem; color: #0f172a;">▸</span> <strong style="color: #002e62; font-size: 1rem;">Ver evaluación del curso</strong><span style="color: #64748b; font-weight: bold;">Abrir / Cerrar</span>
			</summary>
			<div style="padding: 1rem;">
				<div style="overflow:auto; border:1px solid rgba(0,46,98,.12); border-radius:12px;">
					<table style="width:100%; border-collapse: collapse; min-width: 680px;">
						<thead>
							<tr style="background:#002E62; color:#fff;">
								<th style="padding:.65rem .75rem; text-align:left; border-right:1px solid rgba(255,255,255,.25);">Actividad de evaluación</th>
								<th style="padding:.65rem .75rem; text-align:left;">Porcentaje</th>
							</tr>
						</thead>
						<tbody>
							{% for row in evaluacion_rows %}
							<tr style="background:{% if loop.index % 2 == 0 %}#ffffff{% else %}#f8fafc{% endif %};">
								<td style="padding:.6rem .75rem; border-top:1px solid rgba(0,46,98,.08);">{{ row.actividad }}</td>
								<td style="padding:.6rem .75rem; border-top:1px solid rgba(0,46,98,.08);">{{ row.porcentaje }}</td>
							</tr>
							{% endfor %}
						</tbody>
					</table>
				</div>
			</div>
		</details>
	</div>
</div>

<div class="card shadow-sm border-0 mb-3" style="border-left: 8px solid #002E62;">
	<div class="card-body py-3">
		<div class="d-flex align-items-center justify-content-between flex-wrap gap-2">
			<h3 class="h5 m-0" style="color: #002e62;">📄 Rúbricas y guías</h3>
			<span class="badge badge-pill" style="background: #FDC82C; color: #002e62;">{{ course_code }}</span>
		</div>
		<div style="margin-top: .35rem; color: #475569; font-size: 14.5px;">Descargue las rúbricas evaluativas y la guía oficial de evaluación del curso.</div>
		<hr class="my-3" style="border-top: 2px solid #002E62; opacity: .12;">
		<details style="background: #f7f9fc; border: 1px solid rgba(0,46,98,.10); border-radius: 12px; overflow: hidden;">
			<summary style="cursor: pointer; list-style: none; padding: .9rem 1rem; background: #ffffff; display: flex; align-items: center; justify-content: space-between; gap: 1rem; border-left: 6px solid #002E62;">
				<span style="font-size: 1.05rem; color: #0f172a;">▸</span> <strong style="color: #002e62; font-size: 1rem;">Ver rúbricas y guías</strong><span style="color: #64748b; font-weight: bold;">Abrir / Cerrar</span>
			</summary>
			<div style="padding: 1rem;">
				<div style="overflow:auto; border:1px solid rgba(0,46,98,.12); border-radius:12px;">
					<table style="width:100%; border-collapse: collapse; min-width: 680px;">
						<thead>
							<tr style="background:#002E62; color:#fff;">
								<th style="padding:.65rem .75rem; text-align:left; border-right:1px solid rgba(255,255,255,.25);">Documento</th>
								<th style="padding:.65rem .75rem; text-align:left;">Acción</th>
							</tr>
						</thead>
						<tbody>
							{% for rb in rubricas_items %}
							<tr style="background:{% if loop.index % 2 == 0 %}#ffffff{% else %}#f8fafc{% endif %};">
								<td style="padding:.6rem .75rem; border-top:1px solid rgba(0,46,98,.08);">{{ rb.title }}</td>
								<td style="padding:.6rem .75rem; border-top:1px solid rgba(0,46,98,.08);"><a style="display: inline-flex; align-items: center; gap: .5rem; background: #002E62; color: #ffffff; text-decoration: none; padding: .55rem .85rem; border-radius: 10px; font-weight: 800;" href="{{ rb.href }}" target="_blank" rel="noopener">📥 Abrir rúbrica</a></td>
							</tr>
							{% endfor %}
						</tbody>
					</table>
				</div>
			</div>
		</details>
	</div>
</div>

<div class="card shadow-sm border-0 mb-3" style="border-left: 8px solid #002E62;">
	<div class="card-body py-3">
		<div class="d-flex align-items-center justify-content-between flex-wrap gap-2">
			<h3 class="h5 m-0" style="color: #002e62;">🗓️ Cronograma del curso</h3>
			<span class="badge badge-pill" style="background: #FDC82C; color: #002e62;">{{ course_code }}</span>
		</div>
		<div style="margin-top: .35rem; color: #475569; font-size: 14.5px;">Semanas habilitadas para consultar contenido y bibliografía.</div>
		<hr class="my-3" style="border-top: 2px solid #002E62; opacity: .12;">
		<details style="background: #f7f9fc; border: 1px solid rgba(0,46,98,.10); border-radius: 12px; overflow: hidden;">
			<summary style="cursor: pointer; list-style: none; padding: .9rem 1rem; background: #ffffff; display: flex; align-items: center; justify-content: space-between; gap: 1rem; border-left: 6px solid #002E62;">
				<span style="font-size: 1.05rem; color: #0f172a;">▸</span> <strong style="color: #002e62; font-size: 1rem;">Ver cronograma disponible</strong><span style="color: #64748b; font-weight: bold;">Abrir / Cerrar</span>
			</summary>
			<div style="padding: 1rem;">
				<div style="margin-bottom:.8rem;"><a style="display: inline-flex; align-items: center; gap: .5rem; background: #002E62; color: #ffffff; text-decoration: none; padding: .55rem .85rem; border-radius: 10px; font-weight: 800;" href="{{ cronograma_pdf_href }}" target="_blank" rel="noopener">📅 Abrir cronograma</a></div>
			</div>
		</details>
	</div>
</div>

<div class="card shadow-sm border-0 mb-3" style="border-left: 8px solid #002E62;">
	<div class="card-body py-3">
		<div class="d-flex align-items-center justify-content-between flex-wrap gap-2">
			<h3 class="h5 m-0" style="color: #002e62;">📚 Bibliografía y Biblioteca Virtual</h3>
			<span class="badge badge-pill" style="background: #FDC82C; color: #002e62;">{{ course_code }}</span>
		</div>
		<div style="margin-top: .35rem; color: #475569; font-size: 14.5px;">Fuentes de consulta del curso y acceso a biblioteca virtual.</div>
		<hr class="my-3" style="border-top: 2px solid #002E62; opacity: .12;">
		<div style="background: linear-gradient(180deg, #fff8d6 0%, #fffdf3 100%); border: 1px solid rgba(253,200,44,.55); border-left: 8px solid #FDC82C; border-radius: 14px; padding: 1rem;">
			<div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: .95rem;">
				<div style="background:#ffffff; border:1px solid rgba(0,46,98,.10); border-radius:12px; padding:.95rem 1rem;">
					<div style="font-weight:900; color:#002e62; margin-bottom:.55rem;">Bibliografía obligatoria</div>
					<ul style="margin:.2rem 0 0 1.1rem; color:#334155; line-height:1.55;">
						{% for ref in bibliografia_general.obligatoria %}
						<li style="margin-bottom:.8rem;">{{ ref.text }}
							{% if ref.url %}
							<div style='margin-top: .35rem;'><a style='display: inline-flex; align-items: center; gap: .45rem; background: #002E62; color: #ffffff; text-decoration: none; padding: .45rem .75rem; border-radius: 10px; font-weight: 800; font-size: 13.5px;' href='{{ ref.url }}' target='_blank' rel='noopener'> 🔗 Abrir en biblioteca </a></div>
							{% endif %}
						</li>
						{% endfor %}
					</ul>
				</div>
				<div style="background:#ffffff; border:1px solid rgba(0,46,98,.10); border-radius:12px; padding:.95rem 1rem;">
					<div style="font-weight:900; color:#002e62; margin-bottom:.55rem;">Bibliografía complementaria</div>
					<ul style="margin:.2rem 0 0 1.1rem; color:#334155; line-height:1.55;">
						{% for ref in bibliografia_general.complementaria %}
						<li style="margin-bottom:.8rem;">{{ ref.text }}
							{% if ref.url %}
							<div style='margin-top: .35rem;'><a style='display: inline-flex; align-items: center; gap: .45rem; background: #002E62; color: #ffffff; text-decoration: none; padding: .45rem .75rem; border-radius: 10px; font-weight: 800; font-size: 13.5px;' href='{{ ref.url }}' target='_blank' rel='noopener'> 🔗 Abrir en biblioteca </a></div>
							{% endif %}
						</li>
						{% endfor %}
					</ul>
				</div>
			</div>
			<div style="margin-top: 1rem; background:#fffdf5; border:1px solid rgba(253,200,44,.45); border-left:6px solid #FDC82C; border-radius:12px; padding:.9rem 1rem; color:#334155; box-shadow:0 2px 8px rgba(0,0,0,.03);">
				<div style="font-weight:900; color:#002e62; margin-bottom:.55rem;">Biblioteca Virtual</div>
				<div style="display:flex; align-items:center; gap:.5rem; margin-bottom:.35rem;">🔗 <strong>Link:</strong> <span>Abrir Biblioteca Virtual</span></div>
				<div style="display:flex; align-items:center; gap:.5rem; margin-bottom:.35rem;">👤 <strong>Usuario:</strong> <span>BVAUNADECA</span></div>
				<div style="display:flex; align-items:center; gap:.5rem; margin-bottom:.35rem;">🔒 <strong>Contraseña:</strong> <span>lucas2-11</span></div>
				<div style="margin-top:.4rem; color:#b45309; font-weight:700;">📌 Mantén estas credenciales en privado y no las compartas públicamente.</div>
			</div>
		</div>
	</div>
</div>
"""

WEEK_TEMPLATE = """<!doctype html>
<html>
<head>
	<meta charset='utf-8'>
	<title>{{ unit_title }}</title>
</head>
<body>
	<div class="card shadow-sm border-0 mb-3" style="border-left: 8px solid #002E62;">
		<div class="card-body" style="padding: 1.1rem 1.15rem;">
			<div style="text-align: center; margin-top: .25rem;">
				<div style="font-size: 1.6rem; font-weight: 900; color: #0f172a;">{{ unit_title }}</div>
				<div style="margin: .6rem auto 0 auto; width: 90px; height: 4px; background: #002E62; border-radius: 99px;"> </div>
			</div>
			<div style="margin-top: 1rem; background: #e9f5ee; border: 1px solid rgba(111,191,115,.35); border-left: 6px solid #6fbf73; padding: .85rem 1rem; border-radius: 12px;">
				<div style="font-weight: 900; color: #166534; margin-bottom: .25rem;">Resultado de aprendizaje</div>
				<div style="color: #14532d; line-height: 1.45;">{{ resultado }}</div>
			</div>
			<div style="margin-top: 1.1rem;">
				<div style="background: #002E62; color: #ffffff; border-radius: 12px; padding: .7rem .95rem; font-weight: 900; letter-spacing: .25rem; display: flex; align-items: center; justify-content: space-between;">CONTENIDOS <span style="opacity: .9;">📂</span></div>
				<ul style="margin: .75rem 0 0 1.1rem; color: #334155; line-height: 1.6;">
					{% for content in contenidos %}
					<li>{{ content }}</li>
					{% endfor %}
				</ul>
			</div>
		</div>
	</div>
</body>
</html>
"""

BIBLIO_TEMPLATE = """
<!doctype html>
<html>
<head>
	<meta charset='utf-8'>
	<title>Bibliografía {{ week_range }}</title>
</head>
<body>
	<!-- BLOQUE | Bibliografía ({{ week_range }}) -->
	<div style='background: #f7f9fc; border: 1px solid rgba(0,46,98,.10); border-left: 6px solid #6b7280; border-radius: 12px; padding: 1rem 1.1rem; margin: 0 0 1rem 0;'>
		<div style='font-weight: 900; color: #0f172a; font-size: 1.05rem; margin-bottom: .35rem;'>Bibliografía de consulta y aprendizaje</div>
		<div style='color: #64748b; font-size: 13.5px; margin-bottom: .75rem;'>Disponible en Campus Virtual.</div>
		<ul style='margin: .2rem 0 0 1.1rem; color: #334155; line-height: 1.55;'>
			{% for item in bibliografia %}
			<li{% if loop.first %} style='margin-bottom: .8rem;'{% endif %}>{{ item.text }}
				{% if item.url %}
				<div style='margin-top: .35rem;'><a
					style='display: inline-flex; align-items: center; gap: .45rem; background: #002E62; color: #ffffff; text-decoration: none; padding: .45rem .75rem; border-radius: 10px; font-weight: 800; font-size: 13.5px;'
					href='{{ item.url }}'
					target='_blank' rel='noopener'> 🔗 Abrir en biblioteca </a></div>
				{% endif %}
			</li>
			{% endfor %}
		</ul>
	</div>
</body>
</html>
"""

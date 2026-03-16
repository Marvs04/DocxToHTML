"""Interfaz gráfica del Generador de Cursos HTML."""

import os
import re
import threading
import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk

from tkinterdnd2 import DND_FILES, TkinterDnD

from generator_refactor.generator import generate_file

AZUL    = "#002E62"
AMARILLO= "#FDC82C"
FONDO   = "#f0f4f8"
BLANCO  = "#ffffff"


def _parse_paths(raw):
    raw = raw.strip()
    paths = re.findall(r'\{([^}]+)\}', raw)
    resto = re.sub(r'\{[^}]+\}', '', raw).split()
    return [p for p in paths + resto if p]


class App(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("Generador de Cursos HTML")
        self.resizable(False, False)
        self.configure(bg=FONDO)
        self.style_var = tk.StringVar(value='v1')
        self.cancel_event = threading.Event()
        self._build_ui()
        self._center()

    def _center(self):
        self.update_idletasks()
        w, h = 560, 730
        x = (self.winfo_screenwidth()  - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _build_ui(self):
        # ── Encabezado ──────────────────────────────────────────────────
        hdr = tk.Frame(self, bg=AZUL, pady=14)
        hdr.pack(fill="x")
        tk.Label(hdr, text="Generador de Cursos HTML",
                 font=("Segoe UI", 15, "bold"), fg=BLANCO, bg=AZUL).pack()
        tk.Label(hdr, text="Arrastra tus archivos .docx o usa el botón",
                 font=("Segoe UI", 9), fg=AMARILLO, bg=AZUL).pack()

        # ── Zona de drop ────────────────────────────────────────────────
        self.drop_frame = tk.Frame(self, bg=BLANCO, highlightthickness=2,
                                   highlightbackground="#cbd5e1")
        self.drop_frame.pack(fill="x", padx=24, pady=(18, 0), ipady=22)
        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind("<<Drop>>", self._on_drop)
        self.drop_frame.bind("<Enter>", lambda e: self.drop_frame.configure(highlightbackground=AZUL))
        self.drop_frame.bind("<Leave>", lambda e: self.drop_frame.configure(highlightbackground="#cbd5e1"))
        tk.Label(self.drop_frame, text="📂", font=("Segoe UI", 26), bg=BLANCO).pack()
        tk.Label(self.drop_frame, text="Arrastra aquí tus archivos .docx",
                 font=("Segoe UI", 11, "bold"), fg=AZUL, bg=BLANCO).pack()
        tk.Label(self.drop_frame, text="(puedes soltar varios a la vez)",
                 font=("Segoe UI", 9), fg="#64748b", bg=BLANCO).pack()

        # ── Botones: seleccionar + cancelar ────────────────────────────────
        btn_row = tk.Frame(self, bg=FONDO)
        btn_row.pack(pady=10)
        self.btn_browse = tk.Button(btn_row, text="Seleccionar archivos .docx",
                  font=("Segoe UI", 10, "bold"),
                  bg=AMARILLO, fg=AZUL, activebackground="#e6b800",
                  relief="flat", cursor="hand2", padx=16, pady=8,
                  command=self._on_browse)
        self.btn_browse.pack(side="left", padx=(0, 8))
        self.btn_cancel = tk.Button(btn_row, text="✕  Cancelar",
                  font=("Segoe UI", 10, "bold"),
                  bg="#e2e8f0", fg="#6b7280", activebackground="#fca5a5",
                  relief="flat", cursor="hand2", padx=12, pady=8,
                  state="disabled", command=self._on_cancel)
        self.btn_cancel.pack(side="left")

        # ── Selector de estilo ───────────────────────────────────────────
        style_frame = tk.Frame(self, bg=BLANCO, highlightthickness=1,
                               highlightbackground="#e2e8f0")
        style_frame.pack(fill="x", padx=24, pady=(0, 4))
        tk.Label(style_frame, text="Estilo de salida:",
                 font=("Segoe UI", 9, "bold"), fg=AZUL, bg=BLANCO,
                 padx=10, pady=6).grid(row=0, column=0, sticky="w")
        tk.Radiobutton(style_frame, text="V1 — Estilo actual",
                       variable=self.style_var, value='v1',
                       font=("Segoe UI", 9), fg="#334155", bg=BLANCO,
                       activebackground=BLANCO, selectcolor=BLANCO,
                       cursor="hand2").grid(row=0, column=1, sticky="w", padx=4)
        tk.Radiobutton(style_frame, text="V2 — Estilo universitario (formal)",
                       variable=self.style_var, value='v2',
                       font=("Segoe UI", 9), fg="#334155", bg=BLANCO,
                       activebackground=BLANCO, selectcolor=BLANCO,
                       cursor="hand2").grid(row=0, column=2, sticky="w", padx=4)

        # ── Panel de estadísticas ────────────────────────────────────────
        self.stats_frame = tk.Frame(self, bg=BLANCO, highlightthickness=1,
                                    highlightbackground="#e2e8f0")
        self.stats_frame.pack(fill="x", padx=24)

        col_cfg = dict(font=("Segoe UI", 10), bg=BLANCO, padx=10, pady=6)
        self.stat_file    = tk.Label(self.stats_frame, text="📄  —", anchor="w", **col_cfg)
        self.stat_terms   = tk.Label(self.stats_frame, text="🗓  —  cuatrimestres", **col_cfg)
        self.stat_classes = tk.Label(self.stats_frame, text="📖  —  clases", **col_cfg)
        self.stat_file.grid(row=0, column=0, columnspan=2, sticky="w")
        self.stat_terms.grid(row=1, column=0, sticky="w")
        self.stat_classes.grid(row=1, column=1, sticky="w")

        # ── Barra de progreso ────────────────────────────────────────────
        prog_frame = tk.Frame(self, bg=FONDO)
        prog_frame.pack(fill="x", padx=24, pady=(8, 0))

        self.prog_label = tk.Label(prog_frame, text="", font=("Segoe UI", 8),
                                   fg="#64748b", bg=FONDO, anchor="w")
        self.prog_label.pack(fill="x")

        style = ttk.Style(self)
        style.theme_use("default")
        style.configure("Azul.Horizontal.TProgressbar",
                        troughcolor="#e2e8f0", background=AZUL,
                        thickness=10)
        self.progress = ttk.Progressbar(prog_frame, style="Azul.Horizontal.TProgressbar",
                                        orient="horizontal", length=512, mode="determinate")
        self.progress.pack(fill="x", pady=(2, 0))

        # ── Barra de PDFs ──────────────────────────────────────────────
        pdf_frame = tk.Frame(self, bg=FONDO)
        pdf_frame.pack(fill="x", padx=24, pady=(4, 0))
        self.pdf_prog_label = tk.Label(pdf_frame, text="", font=("Segoe UI", 8),
                                       fg="#92600a", bg=FONDO, anchor="w")
        self.pdf_prog_label.pack(fill="x")
        style.configure("Amber.Horizontal.TProgressbar",
                        troughcolor="#e2e8f0", background="#d97706", thickness=8)
        self.pdf_progress = ttk.Progressbar(pdf_frame, style="Amber.Horizontal.TProgressbar",
                                            orient="horizontal", length=512, mode="determinate")
        self.pdf_progress.pack(fill="x", pady=(2, 0))

        # ── Log ──────────────────────────────────────────────────────────
        log_frame = tk.Frame(self, bg=FONDO)
        log_frame.pack(fill="both", expand=True, padx=24, pady=(8, 16))
        tk.Label(log_frame, text="Registro:", font=("Segoe UI", 9, "bold"),
                 fg="#334155", bg=FONDO, anchor="w").pack(fill="x")
        self.log = scrolledtext.ScrolledText(log_frame, height=9,
                                             font=("Consolas", 9),
                                             bg="#1e293b", fg="#e2e8f0",
                                             insertbackground="white",
                                             relief="flat", state="disabled")
        self.log.pack(fill="both", expand=True)
        self.log.tag_config("ok",   foreground="#4ade80")
        self.log.tag_config("err",  foreground="#f87171")
        self.log.tag_config("info", foreground="#93c5fd")
        self.log.tag_config("dim",  foreground="#64748b")

    # ── Eventos ──────────────────────────────────────────────────────────
    def _on_drop(self, event):
        self._run(_parse_paths(event.data))

    def _on_browse(self):
        paths = filedialog.askopenfilenames(
            title="Seleccionar archivos .docx",
            filetypes=[("Documentos Word", "*.docx")])
        if paths:
            self._run(list(paths))

    def _on_cancel(self):
        self.cancel_event.set()
        self._log("  ⚠ Cancelando… (espere el proceso actual)\n", "err")
        self.after(0, lambda: self.btn_cancel.config(state="disabled"))

    def _set_running_state(self):
        self.btn_cancel.config(state="normal", bg="#fee2e2", fg="#991b1b")

    def _set_idle_state(self):
        self.btn_cancel.config(state="disabled", bg="#e2e8f0", fg="#6b7280")

    def _run(self, paths):
        style = self.style_var.get()
        self.cancel_event.clear()
        self.after(0, self._set_running_state)
        threading.Thread(target=self._generate, args=(paths, style), daemon=True).start()

    # ── Lógica de generación ──────────────────────────────────────────────
    def _generate(self, paths, style='v1'):
        self.after(0, self._reset_progress)
        self._log(f"── {len(paths)} archivo(s) recibido(s) ──\n", "info")
        errores = 0
        for path in paths:
            if self.cancel_event.is_set():
                break
            path = path.strip('"').strip("'")
            name = os.path.basename(path)
            if not path.lower().endswith(".docx"):
                self._log(f"  Omitiendo (no es .docx): {name}\n", "dim")
                continue
            if not os.path.isfile(path):
                self._log(f"  No encontrado: {path}\n", "err")
                errores += 1
                continue
            self.after(0, lambda n=name: self.stat_file.config(text=f"📄  {n}"))
            self._log(f"\n{name}\n", "info")
            out_dir = os.path.dirname(os.path.abspath(path))
            try:
                generate_file(path, out_dir, on_progress=self._on_progress,
                              style=style, cancel_check=self.cancel_event.is_set)
                self._log(f"  ✓ Listo → {out_dir}\n", "ok")
            except Exception as exc:
                self._log(f"  ✗ {exc}\n", "err")
                errores += 1

        if self.cancel_event.is_set():
            self._log("\n⚠ Generación cancelada.\n", "err")
        elif errores:
            self._log(f"\n⚠ {errores} error(es).\n", "err")
        else:
            self._log("\n✅ ¡Todo generado correctamente!\n", "ok")
        self.after(0, lambda: self.prog_label.config(text="Completado"))
        self.after(0, self._set_idle_state)

    def _on_progress(self, event, *args):
        if event == 'stats':
            n_terms, n_classes = args
            self.after(0, lambda: self._set_stats(n_terms, n_classes))
        elif event == 'class':
            idx, total, name = args
            self.after(0, lambda: self._set_class_progress(idx, total, name))
        elif event == 'pdf_start':
            total, = args
            self.after(0, lambda: self._set_pdf_start(total))
        elif event == 'pdf_item':
            idx, total, name = args
            self.after(0, lambda: self._set_pdf_progress(idx, total, name))

    def _set_stats(self, n_terms, n_classes):
        plural_t = "cuatrimestre" if n_terms == 1 else "cuatrimestres"
        plural_c = "clase"        if n_classes == 1 else "clases"
        self.stat_terms.config(  text=f"🗓  {n_terms} {plural_t}")
        self.stat_classes.config(text=f"📖  {n_classes} {plural_c}")
        self.progress.config(maximum=n_classes, value=0)

    def _set_class_progress(self, idx, total, name):
        self.progress.config(value=idx)
        short = name[:48] + "…" if len(name) > 48 else name
        self.prog_label.config(text=f"Clase {idx}/{total}: {short}")
        self._log(f"  · {name}\n", "dim")

    def _set_pdf_start(self, total):
        self.pdf_progress.config(maximum=max(total, 1), value=0)
        self.pdf_prog_label.config(text=f"PDFs: preparando {total} clase(s)…")
        self._log("  [Iniciando generación de PDFs…]\n", "dim")

    def _set_pdf_progress(self, idx, total, name):
        self.pdf_progress.config(value=idx)
        short = name[:44] + "…" if len(name) > 44 else name
        self.pdf_prog_label.config(text=f"PDF {idx}/{total}: {short}")

    def _reset_progress(self):
        self.stat_file.config(   text="📄  —")
        self.stat_terms.config(  text="🗓  —  cuatrimestres")
        self.stat_classes.config(text="📖  —  clases")
        self.progress.config(value=0, maximum=1)
        self.prog_label.config(text="")
        self.pdf_progress.config(value=0, maximum=1)
        self.pdf_prog_label.config(text="")

    def _log(self, msg, tag=""):
        self.log.configure(state="normal")
        self.log.insert("end", msg, tag)
        self.log.see("end")
        self.log.configure(state="disabled")


if __name__ == "__main__":
    App().mainloop()

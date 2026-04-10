"""Diagnostic tracking system for generation issues and remediation suggestions."""


class DiagnosticCollector:
    """Collects and reports issues during DOCX generation with remediation suggestions."""

    def __init__(self):
        self.issues = []  # List of (class_name, issue_type, details)

    def report_missing_rubricas(self, class_name):
        """Report that no rúbricas were detected for a class."""
        self.issues.append((
            class_name,
            "missing_rubricas",
            "Sin rúbricas detectadas"
        ))

    def report_missing_cronograma_table(self, class_name):
        """Report that no cronograma table was found."""
        self.issues.append((
            class_name,
            "missing_cronograma",
            "Tabla de cronograma no encontrada"
        ))

    def report_missing_weeks(self, class_name, weeks_detected):
        """Report when weeks are missing or incomplete."""
        self.issues.append((
            class_name,
            "missing_weeks",
            f"Semanas incompletas o mal formateadas detectadas ({weeks_detected} registradas)"
        ))

    def report_missing_unit_names(self, class_name):
        """Report when unit names are missing from weekly indices."""
        self.issues.append((
            class_name,
            "missing_unit_names",
            "Nombres de unidades faltantes en índices semanales"
        ))

    def get_remediation_suggestions(self, issue_type):
        """Return specific remediation suggestion for each issue type."""
        suggestions = {
            "missing_rubricas": (
                "Verificar que las rúbricas comiencen con 'Rúbrica' o 'Rúbricas' y sean párrafos cortos (<80 caracteres). "
                "Evitar títulos largos o con formato especial."
            ),
            "missing_cronograma": (
                "Revisar que exista una tabla con encabezados 'Semana(s)' y 'Contenidos'/'Materiales'. "
                "Las tablas deben tener al menos 3 filas y estar correctamente formateadas."
            ),
            "missing_weeks": (
                "Verificar formato de semanas en cronograma: deben ser números (1-15) o rangos (1-2, 3-5). "
                "Revisar que no falten encabezados o celdas vacías interrumpan la tabla."
            ),
            "missing_unit_names": (
                "Asegurar que cada semana tenga un nombre/título de unidad en la tabla de cronograma. "
                "Las celdas 'Unidad/Tema' no deben estar vacías."
            ),
        }
        return suggestions.get(issue_type, "Ver detalles del documento.")

    def format_summary(self):
        """Format diagnostic summary for display."""
        if not self.issues:
            return "\n✓ Sin problemas detectados.\n"

        # Group issues by class
        by_class = {}
        for class_name, issue_type, details in self.issues:
            if class_name not in by_class:
                by_class[class_name] = []
            by_class[class_name].append((issue_type, details))

        lines = ["\n" + "═" * 60]
        lines.append("  DIAGNÓSTICO")
        lines.append("═" * 60)

        for class_name in sorted(by_class.keys()):
            issues = by_class[class_name]
            lines.append(f"\n  📌 {class_name}")
            for issue_type, details in issues:
                lines.append(f"     • {details}")
                suggestion = self.get_remediation_suggestions(issue_type)
                lines.append(f"       → {suggestion}")

        lines.append("\n" + "═" * 60 + "\n")
        return "\n".join(lines)

    def has_issues(self):
        """Return True if any issues were reported."""
        return len(self.issues) > 0

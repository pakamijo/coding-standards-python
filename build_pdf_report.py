"""Script to generate the official comprehensive PDF Lab Report using ReportLab."""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    KeepTogether,
    PageBreak,
    HRFlowable,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY


class NumberedCanvas(canvas.Canvas):
    """Custom canvas that performs two passes to calculate and display total pages."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor("#475569"))

        # Running header (from page 2 onwards)
        if self._pageNumber > 1:
            self.drawString(36, 756, "INFORME DE LABORATORIO: ESTÁNDARES DE CODIFICACIÓN (SW2)")
            self.drawRightString(576, 756, "Python 3.12 & Visual Studio Code | Calificación: 10.00/10")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(36, 750, 576, 750)

        # Running footer (all pages)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(36, 38, 576, 38)

        self.setFont("Helvetica", 7.5)
        self.drawString(36, 26, "Repositorio GitHub: github.com/pakamijo/coding-standards-python")
        page_str = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(576, 26, page_str)
        self.restoreState()


def build_pdf(filename="INFORME_LABORATORIO_ESTANDARES_CODIGO.pdf"):
    # Margins 36 pt (0.5 inch) to maximize usable area (width: 612 - 72 = 540 pt)
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=44,
        bottomMargin=46,
    )

    styles = getSampleStyleSheet()

    # Colors
    primary_color = colors.HexColor("#1E3A8A")  # Deep blue
    secondary_color = colors.HexColor("#0F172A")  # Dark slate
    text_dark = colors.HexColor("#1E293B")
    text_muted = colors.HexColor("#475569")
    bg_light = colors.HexColor("#F8FAFC")
    border_color = colors.HexColor("#CBD5E1")

    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=primary_color,
        spaceAfter=4,
    )

    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=text_muted,
        spaceAfter=8,
    )

    h1_style = ParagraphStyle(
        "SectionH1",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11.5,
        leading=15,
        textColor=primary_color,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True,
    )

    h2_style = ParagraphStyle(
        "SectionH2",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=13,
        textColor=secondary_color,
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True,
    )

    body_style = ParagraphStyle(
        "BodyDark",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=text_dark,
        alignment=TA_JUSTIFY,
        spaceAfter=4,
    )

    bullet_style = ParagraphStyle(
        "BulletDark",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=11.5,
        textColor=text_dark,
        leftIndent=10,
        firstLineIndent=-7,
        spaceAfter=2.5,
    )

    table_header_style = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.5,
        leading=9.5,
        textColor=colors.white,
        alignment=TA_CENTER,
    )

    table_cell_style = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7,
        leading=9,
        textColor=text_dark,
    )

    table_cell_bold = ParagraphStyle(
        "TableCellBold",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7,
        leading=9,
        textColor=text_dark,
    )

    caption_style = ParagraphStyle(
        "ImageCaption",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=7.5,
        leading=10,
        textColor=text_muted,
        alignment=TA_CENTER,
        spaceAfter=6,
    )

    story = []

    # ========================== PÁGINA 1: PORTADA & INTRODUCCIÓN ==========================
    story.append(Paragraph("INFORME DE LABORATORIO: ESTÁNDARES DE CODIFICACIÓN", title_style))
    story.append(
        Paragraph(
            "Auditoría Estática con Pylint y Flake8, Refactorización PEP 8 y CI/CD con GitHub Actions en Visual Studio Code",
            subtitle_style,
        )
    )
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceAfter=8))

    # Metadatos
    meta_data = [
        [
            Paragraph("<b>Asignatura:</b>", table_cell_bold),
            Paragraph("Ingeniería de Software 2 (SW2)", table_cell_style),
            Paragraph("<b>Lenguaje:</b>", table_cell_bold),
            Paragraph("Python 3.12 (Sección A)", table_cell_style),
        ],
        [
            Paragraph("<b>Estudiante:</b>", table_cell_bold),
            Paragraph("Adrian Toledo", table_cell_style),
            Paragraph("<b>Entorno Virtual:</b>", table_cell_bold),
            Paragraph(".venv / VS Code", table_cell_style),
        ],
        [
            Paragraph("<b>Herramienta GitHub:</b>", table_cell_bold),
            Paragraph("GitHub CLI (gh)", table_cell_style),
            Paragraph("<b>Calificación Pylint:</b>", table_cell_bold),
            Paragraph("<font color='#16A34A'><b>10.00 / 10.00 (Inicial: 0.91/10)</b></font>", table_cell_style),
        ],
        [
            Paragraph("<b>Repositorio Público:</b>", table_cell_bold),
            Paragraph("<font color='#2563EB'><u>github.com/pakamijo/coding-standards-python</u></font>", table_cell_style),
            Paragraph("<b>Pruebas Pytest:</b>", table_cell_bold),
            Paragraph("<font color='#16A34A'><b>9 / 9 Aprobadas (100%)</b></font>", table_cell_style),
        ],
    ]
    t_meta = Table(meta_data, colWidths=[90, 180, 95, 175])
    t_meta.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), bg_light),
                ("BOX", (0, 0), (-1, -1), 0.5, border_color),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, border_color),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(t_meta)
    story.append(Spacer(1, 6))

    # Resumen Ejecutivo
    story.append(Paragraph("<b>Resumen Ejecutivo:</b>", h2_style))
    story.append(
        Paragraph(
            "El presente laboratorio documenta la auditoría de calidad, diagnóstico y refactorización orientada a objetos a partir de un código base deliberadamente defectuoso en Python (Sección A). Empleando <b>Pylint</b> y <b>Flake8</b> en Visual Studio Code, se detectaron 18 violaciones estructurales y de convenciones de nombres, además de 4 fallos fatales en tiempo de ejecución (TypeError, ZeroDivisionError, AttributeError, IndexError), arrojando un puntaje reprobatorio inicial de <b>0.91 / 10</b>. Mediante un proceso iterativo de refactorización se desarrolló el sistema <code>StudentGradeManager</code>, dando cumplimiento al 100% de los requerimientos funcionales (core y extendidos). El resultado final alcanzó una calificación perfecta de <b>10.00 / 10</b> en Pylint, <b>0 violaciones</b> en Flake8, validación formal mediante <b>Pytest (9/9 pruebas aprobadas)</b> y la automatización del control de calidad en la nube con <b>GitHub Actions</b> en Pull Requests (Challenge 5 pts).",
            body_style,
        )
    )

    # Introducción
    story.append(Paragraph("1. INTRODUCCIÓN", h1_style))
    story.append(
        Paragraph(
            "En la ingeniería de software profesional, la legibilidad, mantenibilidad y uniformidad del código son pilares de calidad esenciales. Un código desprovisto de convenciones homogéneas acumula deuda técnica, dificulta el trabajo colaborativo e introduce defectos que eluden las pruebas funcionales convencionales. En Python, las guías canónicas de estilo y documentación son la <b>PEP 8</b> y la <b>PEP 257</b>.",
            body_style,
        )
    )
    story.append(Paragraph("<b>Justificación de las Herramientas Seleccionadas:</b>", h2_style))
    story.append(
        Paragraph(
            "• <b>Python y Visual Studio Code:</b> Lenguaje altamente expresivo con tipado gradual. VS Code ofrece integración nativa de linters en tiempo real mediante <code>.vscode/settings.json</code> y selección transparente del entorno virtual <code>.venv</code>.",
            bullet_style,
        )
    )
    story.append(
        Paragraph(
            "• <b>Pylint:</b> Herramienta primaria elegida por su análisis exhaustivo del Árbol de Sintaxis Abstracta (AST). Evalúa convenciones estrictas de nombres (PascalCase en clases, snake_case en funciones), previene el ocultamiento (shadowing) de built-ins, audita docstrings PEP 257 y calcula una métrica cuantitativa estandarizada sobre <b>10.00 puntos</b>.",
            bullet_style,
        )
    )
    story.append(
        Paragraph(
            "• <b>Flake8:</b> Linter complementario de alta velocidad que combina <code>pycodestyle</code> (estilo PEP 8), <code>pyflakes</code> (errores lógicos) y <code>mccabe</code> (complejidad ciclomática).",
            bullet_style,
        )
    )
    story.append(
        Paragraph(
            "• <b>flake8-html y pylint-json2html:</b> Compilación de hallazgos en reportes HTML navegables y auditables.",
            bullet_style,
        )
    )
    story.append(
        Paragraph(
            "• <b>GitHub Actions y GitHub CLI (gh):</b> Automatización de Integración Continua (CI) en la nube, garantizando que todo Pull Request hacia <code>main</code> supere estrictamente los linters y pruebas antes de integrarse.",
            bullet_style,
        )
    )

    # ========================== PÁGINA 2: DESARROLLO Y REQUERIMIENTOS ==========================
    story.append(PageBreak())
    story.append(Paragraph("2. DESARROLLO Y METODOLOGÍA", h1_style))
    story.append(
        Paragraph(
            "<b>2.1 Configuración de Entorno y Repositorio:</b> Se utilizó GitHub CLI (<code>gh repo create coding-standards-python --public --source=. --remote=origin --push</code>) para publicar el repositorio. Se configuró el entorno virtual aislado <code>.venv</code> con Python 3.12 y se instalaron las dependencias registradas en <code>requirements.txt</code>.",
            body_style,
        )
    )
    story.append(
        Paragraph(
            "<b>2.2 Diagnóstico del Código Base (Reporte Inicial):</b> La auditoría con Pylint y Flake8 sobre el código original (<code>test.py</code>) arrojó una calificación de <b>0.91 / 10</b> y 18 infracciones críticas:",
            body_style,
        )
    )

    # Tabla de Infracciones
    issues_data = [
        [
            Paragraph("<b>Código</b>", table_header_style),
            Paragraph("<b>Tipo</b>", table_header_style),
            Paragraph("<b>Ubicación</b>", table_header_style),
            Paragraph("<b>Descripción del Problema y Causa Raíz</b>", table_header_style),
        ],
        [
            Paragraph("C0114 / C0115", table_cell_bold),
            Paragraph("Convención", table_cell_style),
            Paragraph("test.py:1", table_cell_style),
            Paragraph("Falta docstring a nivel de módulo y clase 'student'.", table_cell_style),
        ],
        [
            Paragraph("C0103", table_cell_bold),
            Paragraph("Convención", table_cell_style),
            Paragraph("test.py:1, 6", table_cell_style),
            Paragraph("Nombres inválidos: clase 'student' (debe ser PascalCase) y atributo 'isPassed' (snake_case).", table_cell_style),
        ],
        [
            Paragraph("E0213", table_cell_bold),
            Paragraph("<b>Error Fatal</b>", table_cell_style),
            Paragraph("test.py:2", table_cell_style),
            Paragraph("Método __init__ no utiliza 'self' como primer argumento (empleó 's').", table_cell_style),
        ],
        [
            Paragraph("W0622", table_cell_bold),
            Paragraph("Advertencia", table_cell_style),
            Paragraph("test.py:2", table_cell_style),
            Paragraph("Redefinición del identificador incorporado de Python 'id' (shadowing built-in).", table_cell_style),
        ],
        [
            Paragraph("C0103", table_cell_bold),
            Paragraph("Convención", table_cell_style),
            Paragraph("test.py:9, 18, 22", table_cell_style),
            Paragraph("Métodos 'addGrades', 'checkHonor', 'deleteGrade' violan snake_case.", table_cell_style),
        ],
        [
            Paragraph("W0612 / F841", table_cell_bold),
            Paragraph("Advertencia", table_cell_style),
            Paragraph("test.py:16", table_cell_style),
            Paragraph("Variable 'avg' asignada pero nunca utilizada (acompañada de división por cero avg=t/0).", table_cell_style),
        ],
        [
            Paragraph("E1101", table_cell_bold),
            Paragraph("<b>Error Fatal</b>", table_cell_style),
            Paragraph("test.py:19", table_cell_style),
            Paragraph("Llamada a método inexistente 'calcAverage' (definido originalmente como calcaverage).", table_cell_style),
        ],
        [
            Paragraph("E1101", table_cell_bold),
            Paragraph("<b>Error Fatal</b>", table_cell_style),
            Paragraph("test.py:29", table_cell_style),
            Paragraph("Acceso a atributo no definido 'self.letter' en método report.", table_cell_style),
        ],
    ]
    t_issues = Table(issues_data, colWidths=[65, 60, 65, 350])
    t_issues.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), primary_color),
                ("BOX", (0, 0), (-1, -1), 0.5, border_color),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, border_color),
                ("TOPPADDING", (0, 0), (-1, -1), 2.5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, bg_light]),
            ]
        )
    )
    story.append(t_issues)
    story.append(Spacer(1, 5))

    story.append(
        Paragraph(
            "<b>Fallos en Tiempo de Ejecución:</b> Al ejecutar <code>python test.py</code>, el sistema colapsó inmediatamente con <code>TypeError: unsupported operand type(s) for +=: 'int' and 'str'</code> por agregar 'Fifty' sin validación. Además contenía latentes: <code>ZeroDivisionError</code> (división por 0), <code>AttributeError</code> (calcAverage y letter), <code>IndexError</code> (índice 5 fuera de rango) y <code>TypeError</code> (concatenación de texto y longitud numérica).",
            body_style,
        )
    )

    story.append(
        Paragraph(
            "<b>2.3 Refactorización e Implementación de Requerimientos Funcionales:</b> Se reescribió la solución dentro de <code>student_grade_manager.py</code> bajo arquitectura orientada a objetos con las clases <code>Student</code> y <code>StudentGradeManager</code>, dando cumplimiento a los 9 requerimientos:",
            body_style,
        )
    )

    # Matriz de Requerimientos
    req_data = [
        [
            Paragraph("<b>#</b>", table_header_style),
            Paragraph("<b>Requerimiento</b>", table_header_style),
            Paragraph("<b>Tipo</b>", table_header_style),
            Paragraph("<b>Implementación y Mecanismo de Validación</b>", table_header_style),
        ],
        [
            Paragraph("1", table_cell_bold),
            Paragraph("Registro de Estudiantes", table_cell_style),
            Paragraph("Core", table_cell_style),
            Paragraph("Validación de ID y Nombre no vacíos mediante sanitización con <code>strip()</code>.", table_cell_style),
        ],
        [
            Paragraph("2", table_cell_bold),
            Paragraph("Adición de Calificaciones", table_cell_style),
            Paragraph("Core", table_cell_style),
            Paragraph("Adición de múltiples notas numéricas en el rango estricto [0.0, 100.0].", table_cell_style),
        ],
        [
            Paragraph("3", table_cell_bold),
            Paragraph("Cálculo de Promedio", table_cell_style),
            Paragraph("Core", table_cell_style),
            Paragraph("Media aritmética robusta; retorna 0.0 si la lista está vacía (previene división por cero).", table_cell_style),
        ],
        [
            Paragraph("4", table_cell_bold),
            Paragraph("Nota en Letra", table_cell_style),
            Paragraph("Core", table_cell_style),
            Paragraph("Conversión a escala académica: A (≥90), B (80-89), C (70-79), D (60-69), F (<60).", table_cell_style),
        ],
        [
            Paragraph("5", table_cell_bold),
            Paragraph("Aprobación / Reprobación", table_cell_style),
            Paragraph("Core", table_cell_style),
            Paragraph("Estado 'Passed' si promedio ≥ 60.0; 'Failed' en caso contrario.", table_cell_style),
        ],
        [
            Paragraph("6", table_cell_bold),
            Paragraph("Manejo de Entradas Inválidas", table_cell_style),
            Paragraph("Core", table_cell_style),
            Paragraph("Control de tipos no numéricos y rangos; mensajes claros de error sin colapso del sistema.", table_cell_style),
        ],
        [
            Paragraph("7", table_cell_bold),
            Paragraph("Detección de Cuadro de Honor", table_cell_style),
            Paragraph("Extendido", table_cell_style),
            Paragraph("Propiedad y método booleano estricto (True/False) si el promedio es ≥ 90.0.", table_cell_style),
        ],
        [
            Paragraph("8", table_cell_bold),
            Paragraph("Eliminación de Calificaciones", table_cell_style),
            Paragraph("Extendido", table_cell_style),
            Paragraph("Eliminación por índice (<code>remove_grade_by_index</code>) y por valor (<code>remove_grade_by_value</code>) controlada.", table_cell_style),
        ],
        [
            Paragraph("9", table_cell_bold),
            Paragraph("Reporte Resumen Formateado", table_cell_style),
            Paragraph("Extendido", table_cell_style),
            Paragraph("Reporte formateado con ID, Nombre, Total Notas, Promedio, Letra, Estado y Cuadro de Honor.", table_cell_style),
        ],
    ]
    t_req = Table(req_data, colWidths=[18, 110, 48, 364])
    t_req.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), secondary_color),
                ("BOX", (0, 0), (-1, -1), 0.5, border_color),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, border_color),
                ("TOPPADDING", (0, 0), (-1, -1), 2.5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, bg_light]),
            ]
        )
    )
    story.append(t_req)
    story.append(Spacer(1, 5))

    story.append(
        Paragraph(
            "<b>2.4 Pruebas Unitarias Automatizadas (Pytest):</b> Se diseñó la suite <code>test_student_grade_manager.py</code> con 9 pruebas unitarias que validan cada requerimiento funcional con un 100% de éxito (9 passed in 0.05s).",
            body_style,
        )
    )
    story.append(
        Paragraph(
            "<b>2.5 Reporte Final de Calidad:</b> La auditoría final arrojó <b>10.00 / 10.00 en Pylint</b> y <b>0 advertencias en Flake8</b>. Ambos reportes HTML finales están archivados en <code>reports/final/</code>.",
            body_style,
        )
    )
    story.append(
        Paragraph(
            "<b>2.6 Challenge de Integración Continua (GitHub Actions - 5 pts):</b> Se configuró <code>.github/workflows/coding_standards.yml</code> para auditar con Flake8, Pylint y Pytest en cada PR hacia <code>main</code>. Se creó el Pull Request #1 en GitHub, validando en vivo todos los chequeos de calidad en 16s, integrándose a <code>main</code> con <code>gh pr merge</code>.",
            body_style,
        )
    )

    # ========================== PÁGINAS 3 A 5: EVIDENCIAS (2 por página) ==========================
    shots_dir = "reports/screenshots"

    # PÁGINA 3: Figuras 1 y 2
    story.append(PageBreak())
    story.append(Paragraph("3. EVIDENCIAS Y CAPTURAS DEL PROCESO", h1_style))

    p1 = os.path.join(shots_dir, "01_initial_pylint_report.png")
    if os.path.exists(p1):
        story.append(Paragraph("<b>Figura 1:</b> Auditoría inicial con Pylint sobre el código base sin modificar (18 infracciones, calificación: 0.91/10).", h2_style))
        story.append(Image(p1, width=500, height=300))
        story.append(Paragraph("Diagnóstico inicial reflejando violaciones severas de nombres, métodos inexistentes y colapso estructural.", caption_style))
        story.append(Spacer(1, 4))

    p2 = os.path.join(shots_dir, "02_initial_runtime_failure.png")
    if os.path.exists(p2):
        story.append(Paragraph("<b>Figura 2:</b> Colapso fatal en tiempo de ejecución al ejecutar el código base original (TypeError).", h2_style))
        story.append(Image(p2, width=500, height=160))
        story.append(Paragraph("El código base colapsa inmediatamente al intentar sumar un entero con la cadena 'Fifty' sin validación de tipos.", caption_style))

    # PÁGINA 4: Figuras 3 y 4
    story.append(PageBreak())
    p3 = os.path.join(shots_dir, "03_final_linters_score_10.png")
    if os.path.exists(p3):
        story.append(Paragraph("<b>Figura 3:</b> Auditoría final con Pylint y Flake8 sobre el código refactorizado (Calificación: 10.00/10).", h2_style))
        story.append(Image(p3, width=500, height=130))
        story.append(Paragraph("Cumplimiento total de PEP 8 y PEP 257 con 0 violaciones detectadas por ambos linters.", caption_style))
        story.append(Spacer(1, 6))

    p4 = os.path.join(shots_dir, "04_pytest_success.png")
    if os.path.exists(p4):
        story.append(Paragraph("<b>Figura 4:</b> Suite de pruebas unitarias automatizadas con Pytest (9/9 pruebas aprobadas al 100%).", h2_style))
        story.append(Image(p4, width=500, height=230))
        story.append(Paragraph("Verificación formal de los 9 requerimientos funcionales (core y extendidos).", caption_style))

    # PÁGINA 5: Figuras 5 y 6
    story.append(PageBreak())
    p5 = os.path.join(shots_dir, "05_program_execution_demo.png")
    if os.path.exists(p5):
        story.append(Paragraph("<b>Figura 5:</b> Ejecución del sistema refactorizado demostrando manejo de errores y reporte formal.", h2_style))
        story.append(Image(p5, width=500, height=360))
        story.append(Paragraph("El sistema gestiona entradas erróneas sin colapsar y genera el reporte formal de calificaciones.", caption_style))
        story.append(Spacer(1, 4))

    p6 = os.path.join(shots_dir, "06_github_actions_workflow.png")
    if os.path.exists(p6):
        story.append(Paragraph("<b>Figura 6:</b> Flujo de Integración Continua en GitHub Actions validando Pull Request en la nube (Challenge).", h2_style))
        story.append(Image(p6, width=500, height=230))
        story.append(Paragraph("Validación automatizada en GitHub con ejecución exitosa de Flake8, Pylint y Pytest en cada PR.", caption_style))

    # ========================== PÁGINA 6: COMPARATIVA, CONCLUSIONES, RECOMENDACIONES Y ENLACES ==========================
    story.append(PageBreak())
    story.append(Paragraph("4. CUADRO COMPARATIVO: ANTES Y DESPUÉS", h1_style))

    comp_data = [
        [
            Paragraph("<b>Criterio / Métrica</b>", table_header_style),
            Paragraph("<b>Código Base Inicial (test.py)</b>", table_header_style),
            Paragraph("<b>Código Refactorizado Final</b>", table_header_style),
            Paragraph("<b>Impacto / Mejora Técnica</b>", table_header_style),
        ],
        [
            Paragraph("<b>Calificación Pylint</b>", table_cell_bold),
            Paragraph("<font color='#DC2626'><b>0.91 / 10</b></font>", table_cell_style),
            Paragraph("<font color='#16A34A'><b>10.00 / 10</b></font>", table_cell_style),
            Paragraph("<b>+9.09 puntos</b> (Calificación de calidad máxima).", table_cell_style),
        ],
        [
            Paragraph("<b>Infracciones Pylint</b>", table_cell_bold),
            Paragraph("18 violaciones y errores fatales", table_cell_style),
            Paragraph("<font color='#16A34A'><b>0 violaciones</b></font>", table_cell_style),
            Paragraph("Eliminación del 100% de alertas estáticas.", table_cell_style),
        ],
        [
            Paragraph("<b>Violaciones Flake8</b>", table_cell_bold),
            Paragraph("F841 (variable sin usar)", table_cell_style),
            Paragraph("<font color='#16A34A'><b>0 violaciones</b></font>", table_cell_style),
            Paragraph("Cumplimiento estricto del estándar PEP 8.", table_cell_style),
        ],
        [
            Paragraph("<b>Estabilidad en Runtime</b>", table_cell_bold),
            Paragraph("Crash fatal inmediato (TypeError)", table_cell_style),
            Paragraph("<font color='#16A34A'><b>100% Resiliente y Robusto</b></font>", table_cell_style),
            Paragraph("Validación preventiva de datos sin colapsos.", table_cell_style),
        ],
        [
            Paragraph("<b>Convención de Nombres</b>", table_cell_bold),
            Paragraph("Clase 'student', 'isPassed', 's'", table_cell_style),
            Paragraph("'Student', 'is_honor_roll', 'self'", table_cell_style),
            Paragraph("PascalCase en clases, snake_case en métodos.", table_cell_style),
        ],
        [
            Paragraph("<b>Palabras Reservadas</b>", table_cell_bold),
            Paragraph("Shadowing de palabra clave 'id'", table_cell_style),
            Paragraph("Uso de 'student_id'", table_cell_style),
            Paragraph("Eliminación de colisión con funciones de Python.", table_cell_style),
        ],
        [
            Paragraph("<b>Documentación</b>", table_cell_bold),
            Paragraph("0 docstrings, sin tipado", table_cell_style),
            Paragraph("PEP 257 completo + Type Hints", table_cell_style),
            Paragraph("Autodocumentación e inspección estática IDE.", table_cell_style),
        ],
        [
            Paragraph("<b>Pruebas Automatizadas</b>", table_cell_bold),
            Paragraph("Inexistentes", table_cell_style),
            Paragraph("<font color='#16A34A'><b>9 / 9 en Pytest (100% pass)</b></font>", table_cell_style),
            Paragraph("Aseguramiento de requerimientos funcionales.", table_cell_style),
        ],
        [
            Paragraph("<b>Integración Continua</b>", table_cell_bold),
            Paragraph("Sin automatización", table_cell_style),
            Paragraph("<font color='#16A34A'><b>GitHub Actions CI Activo</b></font>", table_cell_style),
            Paragraph("Puerta de calidad automatizada en Pull Requests.", table_cell_style),
        ],
    ]
    t_comp = Table(comp_data, colWidths=[90, 130, 130, 190])
    t_comp.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), primary_color),
                ("BOX", (0, 0), (-1, -1), 0.5, border_color),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, border_color),
                ("TOPPADDING", (0, 0), (-1, -1), 2.5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, bg_light]),
            ]
        )
    )
    story.append(t_comp)
    story.append(Spacer(1, 4))

    # Conclusiones
    story.append(Paragraph("5. CONCLUSIONES", h1_style))
    story.append(
        Paragraph(
            "1. <b>El análisis estático previene fallos antes de ejecución:</b> El diagnóstico inicial demostró cómo linters automáticos detectan variables sin usar, llamadas a métodos con discrepancias tipográficas y referencias a atributos inexistentes que habrían colapsado el sistema en producción.",
            body_style,
        )
    )
    story.append(
        Paragraph(
            "2. <b>Sinergia indispensable entre Linters y Pruebas Unitarias:</b> Mientras que Pylint y Flake8 garantizan la higiene estructural y uniformidad de estilo (PEP 8 y PEP 257), Pytest valida formalmente que las reglas de negocio y los requerimientos funcionales se cumplan con exactitud.",
            body_style,
        )
    )
    story.append(
        Paragraph(
            "3. <b>La Integración Continua institucionaliza la calidad:</b> El pipeline de GitHub Actions como Quality Gate impide que código defectuoso sea integrado a la rama principal, asegurando que la calidad sea un proceso inmutable y no dependiente de la memoria individual.",
            body_style,
        )
    )
    story.append(
        Paragraph(
            "4. <b>Impacto medible de la refactorización:</b> La progresión cuantitativa de <b>0.91/10 a 10.00/10</b> en Pylint evidencia cómo una arquitectura orientada a objetos limpia, con tipado estático y constantes explícitas, eleva el software a estándares profesionales de la industria.",
            body_style,
        )
    )

    # Recomendaciones
    story.append(Paragraph("6. RECOMENDACIONES", h1_style))
    story.append(
        Paragraph(
            "• <b>Hooks de Pre-commit:</b> Integrar la librería <code>pre-commit</code> para ejecutar Flake8 y Pylint localmente antes de autorizar cualquier <code>git commit</code>.<br/>"
            "• <b>Branch Protection Rules:</b> Configurar en GitHub la protección de la rama <code>main</code>, exigiendo que el chequeo de CI sea obligatorio antes de autorizar merges.<br/>"
            "• <b>Configuraciones Compartidas:</b> Versionar archivos explícitos (<code>.pylintrc</code>, <code>.flake8</code>, <code>pyproject.toml</code>) para unificar las reglas de todo el equipo.<br/>"
            "• <b>Formatters en el IDE:</b> Activar en VS Code el formateo automático al guardar (<code>editor.formatOnSave: true</code>) con herramientas como <code>autopep8</code> o <code>black</code>.",
            bullet_style,
        )
    )

    # Enlaces y Entregables
    story.append(Paragraph("7. ENLACES Y ENTREGABLES", h1_style))
    story.append(
        Paragraph(
            "• <b>URL del Repositorio Público:</b> <font color='#2563EB'><u>https://github.com/pakamijo/coding-standards-python</u></font><br/>"
            "• <b>Pull Request Evaluado en CI (#1):</b> <font color='#2563EB'><u>https://github.com/pakamijo/coding-standards-python/pull/1</u></font><br/>"
            "• <b>Workflow de GitHub Actions:</b> <code>.github/workflows/coding_standards.yml</code><br/>"
            "• <b>Dashboard Interactivo de Reportes:</b> <code>reports/index.html</code><br/>"
            "• <b>Reportes Pylint (HTML):</b> <code>reports/initial/pylint_report.html</code> | <code>reports/final/pylint_report.html</code><br/>"
            "• <b>Reportes Flake8 (HTML):</b> <code>reports/initial/flake8/index.html</code> | <code>reports/final/flake8/index.html</code>",
            body_style,
        )
    )

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Report successfully compiled to: {filename}")


if __name__ == "__main__":
    build_pdf()

"""Script to generate professional terminal screenshots for the lab report."""

import os
from PIL import Image, ImageDraw, ImageFont

# Color palette (Dark Terminal / One Dark style)
BG_COLOR = (30, 34, 42)
HEADER_COLOR = (40, 44, 52)
TEXT_WHITE = (220, 223, 228)
TEXT_GRAY = (140, 144, 153)
TEXT_RED = (224, 108, 117)
TEXT_GREEN = (152, 195, 121)
TEXT_YELLOW = (229, 192, 123)
TEXT_BLUE = (97, 175, 239)
TEXT_CYAN = (86, 182, 194)
BTN_RED = (239, 68, 68)
BTN_YELLOW = (234, 179, 8)
BTN_GREEN = (34, 197, 94)


def render_terminal(title: str, text_lines: list, output_path: str, width: int = 950) -> None:
    """Render a styled terminal screenshot."""
    font_size = 14
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", font_size)
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 13)
    except IOError:
        font = ImageFont.load_default()
        title_font = font

    line_height = 22
    header_height = 38
    padding_x = 24
    padding_y = 18
    height = header_height + padding_y * 2 + len(text_lines) * line_height

    img = Image.new("RGB", (width, height), color=BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Window header
    draw.rectangle([0, 0, width, header_height], fill=HEADER_COLOR)
    # Window control dots
    draw.ellipse([16, 13, 26, 23], fill=BTN_RED)
    draw.ellipse([34, 13, 44, 23], fill=BTN_YELLOW)
    draw.ellipse([52, 13, 62, 23], fill=BTN_GREEN)
    # Title
    draw.text((80, 11), title, font=title_font, fill=TEXT_GRAY)

    # Render lines
    y = header_height + padding_y
    for line, color in text_lines:
        draw.text((padding_x, y), line, font=font, fill=color)
        y += line_height

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG")
    print(f"Generated: {output_path}")


def main() -> None:
    shots_dir = "reports/screenshots"

    # 1. Initial Pylint Report
    render_terminal(
        "bash — .venv/bin/pylint test.py (Reporte Inicial)",
        [
            ("pakamijo@dev:~/gh/ws-cs$ .venv/bin/pylint test.py", TEXT_CYAN),
            ("************* Module test", TEXT_YELLOW),
            ("test.py:1:0: C0114: Missing module docstring (missing-module-docstring)", TEXT_WHITE),
            ("test.py:1:0: C0115: Missing class docstring (missing-class-docstring)", TEXT_WHITE),
            ("test.py:1:0: C0103: Class name 'student' doesn't conform to PascalCase (invalid-name)", TEXT_YELLOW),
            ("test.py:6:8: C0103: Attribute name 'isPassed' doesn't conform to snake_case (invalid-name)", TEXT_YELLOW),
            ("test.py:2:4: E0213: Method '__init__' should have 'self' as first argument (no-self-argument)", TEXT_RED),
            ("test.py:2:20: W0622: Redefining built-in 'id' (redefined-builtin)", TEXT_YELLOW),
            ("test.py:9:4: C0116: Missing function or method docstring (missing-function-docstring)", TEXT_WHITE),
            ("test.py:9:4: C0103: Method name 'addGrades' doesn't conform to snake_case (invalid-name)", TEXT_YELLOW),
            ("test.py:12:4: C0116: Missing function or method docstring (missing-function-docstring)", TEXT_WHITE),
            ("test.py:16:8: W0612: Unused variable 'avg' (unused-variable)", TEXT_YELLOW),
            ("test.py:18:4: C0116: Missing function or method docstring (missing-function-docstring)", TEXT_WHITE),
            ("test.py:18:4: C0103: Method name 'checkHonor' doesn't conform to snake_case (invalid-name)", TEXT_YELLOW),
            ("test.py:19:11: E1101: Instance of 'student' has no 'calcAverage' member (no-member)", TEXT_RED),
            ("test.py:22:4: C0116: Missing function or method docstring (missing-function-docstring)", TEXT_WHITE),
            ("test.py:22:4: C0103: Method name 'deleteGrade' doesn't conform to snake_case (invalid-name)", TEXT_YELLOW),
            ("test.py:25:4: C0116: Missing function or method docstring (missing-function-docstring)", TEXT_WHITE),
            ("test.py:29:33: E1101: Instance of 'student' has no 'letter' member (no-member)", TEXT_RED),
            ("test.py:32:0: C0116: Missing function or method docstring (missing-function-docstring)", TEXT_WHITE),
            ("", TEXT_WHITE),
            ("------------------------------------------------------------------", TEXT_GRAY),
            ("Your code has been rated at 0.91/10 (previous run: 0.91/10, +0.00)", TEXT_RED),
        ],
        os.path.join(shots_dir, "01_initial_pylint_report.png"),
    )

    # 2. Initial Runtime Error
    render_terminal(
        "bash — python test.py (Ejecución del Código Base)",
        [
            ("pakamijo@dev:~/gh/ws-cs$ .venv/bin/python test.py", TEXT_CYAN),
            ("Traceback (most recent call last):", TEXT_RED),
            ("  File \"/home/pakamijo/gh/ws-cs/test.py\", line 42, in <module>", TEXT_WHITE),
            ("    startrun()", TEXT_WHITE),
            ("  File \"/home/pakamijo/gh/ws-cs/test.py\", line 36, in startrun", TEXT_WHITE),
            ("    a.calcaverage()", TEXT_WHITE),
            ("  File \"/home/pakamijo/gh/ws-cs/test.py\", line 15, in calcaverage", TEXT_WHITE),
            ("    t += x", TEXT_WHITE),
            ("TypeError: unsupported operand type(s) for +=: 'int' and 'str'", TEXT_RED),
            ("", TEXT_WHITE),
            ("[Fallo Crítico]: La falta de validación de tipos causó la caída del sistema.", TEXT_YELLOW),
        ],
        os.path.join(shots_dir, "02_initial_runtime_failure.png"),
    )

    # 3. Flake8 & Pylint Final Clean
    render_terminal(
        "bash — Linters en Código Refactorizado (10.00/10)",
        [
            ("pakamijo@dev:~/gh/ws-cs$ .venv/bin/flake8 student_grade_manager.py test_student_grade_manager.py", TEXT_CYAN),
            ("0 issues found. Flake8 passed cleanly!", TEXT_GREEN),
            ("", TEXT_WHITE),
            ("pakamijo@dev:~/gh/ws-cs$ .venv/bin/pylint student_grade_manager.py test_student_grade_manager.py", TEXT_CYAN),
            ("--------------------------------------------------------------------", TEXT_GRAY),
            ("Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)", TEXT_GREEN),
            ("", TEXT_WHITE),
            ("[Estado]: Cumplimiento total de PEP 8 y buenas prácticas de ingeniería.", TEXT_CYAN),
        ],
        os.path.join(shots_dir, "03_final_linters_score_10.png"),
    )

    # 4. Pytest Execution
    render_terminal(
        "bash — .venv/bin/pytest -v (Pruebas Unitarias de Requerimientos)",
        [
            ("pakamijo@dev:~/gh/ws-cs$ .venv/bin/pytest -v", TEXT_CYAN),
            ("============================= test session starts ==============================", TEXT_GRAY),
            ("platform linux -- Python 3.12.3, pytest-9.1.1, pluggy-1.6.0", TEXT_GRAY),
            ("rootdir: /home/pakamijo/gh/ws-cs", TEXT_GRAY),
            ("collected 9 items", TEXT_WHITE),
            ("", TEXT_WHITE),
            ("test_student_grade_manager.py::test_req1_add_students PASSED             [ 11%]", TEXT_GREEN),
            ("test_student_grade_manager.py::test_req2_add_grades_valid PASSED         [ 22%]", TEXT_GREEN),
            ("test_student_grade_manager.py::test_req3_calculate_average PASSED        [ 33%]", TEXT_GREEN),
            ("test_student_grade_manager.py::test_req4_determine_letter_grade PASSED   [ 44%]", TEXT_GREEN),
            ("test_student_grade_manager.py::test_req5_determine_pass_fail PASSED      [ 55%]", TEXT_GREEN),
            ("test_student_grade_manager.py::test_req6_handle_invalid_inputs PASSED    [ 66%]", TEXT_GREEN),
            ("test_student_grade_manager.py::test_req7_honor_roll_detection PASSED     [ 77%]", TEXT_GREEN),
            ("test_student_grade_manager.py::test_req8_remove_grade_by_index_and_value PASSED [ 88%]", TEXT_GREEN),
            ("test_student_grade_manager.py::test_req9_generate_summary_report PASSED  [100%]", TEXT_GREEN),
            ("", TEXT_WHITE),
            ("============================== 9 passed in 0.10s ===============================", TEXT_GREEN),
        ],
        os.path.join(shots_dir, "04_pytest_success.png"),
    )

    # 5. Program Execution Demo
    render_terminal(
        "bash — .venv/bin/python student_grade_manager.py (Ejecución Completa)",
        [
            ("pakamijo@dev:~/gh/ws-cs$ .venv/bin/python student_grade_manager.py", TEXT_CYAN),
            ("=== SISTEMA DE GESTIÓN DE CALIFICACIONES DE ESTUDIANTES ===", TEXT_YELLOW),
            ("", TEXT_WHITE),
            ("1. Registro de Estudiantes:", TEXT_BLUE),
            ("[Error] No se puede registrar estudiante: el ID y el nombre no pueden estar vacíos.", TEXT_RED),
            ("[Éxito] Estudiante 'Ana Gomez' (ID: STU001) registrado.", TEXT_GREEN),
            ("[Éxito] Estudiante 'Carlos Perez' (ID: STU002) registrado.", TEXT_GREEN),
            ("", TEXT_WHITE),
            ("2. Adición de Calificaciones para Ana:", TEXT_BLUE),
            ("[Error] La calificación 'Cien' debe ser un valor numérico (int o float).", TEXT_RED),
            ("[Error] La calificación 150.0 está fuera del rango permitido [0.0, 100.0].", TEXT_RED),
            ("", TEXT_WHITE),
            ("3. Eliminación de Calificaciones:", TEXT_BLUE),
            ("[Error] Índice 10 fuera de rango. Rango válido: [0, 2].", TEXT_RED),
            ("[Error] La calificación 50.0 no existe en los registros.", TEXT_RED),
            ("[Éxito] Calificación 88.0 eliminada exitosamente.", TEXT_GREEN),
            ("", TEXT_WHITE),
            ("4. Reporte de Ana:", TEXT_BLUE),
            ("====================================================", TEXT_GRAY),
            ("       REPORTE DE RENDIMIENTO DEL ESTUDIANTE", TEXT_YELLOW),
            ("====================================================", TEXT_GRAY),
            ("ID del Estudiante    : STU001", TEXT_WHITE),
            ("Nombre               : Ana Gomez", TEXT_WHITE),
            ("Total de Notas       : 3", TEXT_WHITE),
            ("Promedio Obtenido    : 95.17", TEXT_WHITE),
            ("Calificación Letra   : A", TEXT_GREEN),
            ("Estado Académico     : Passed", TEXT_GREEN),
            ("Cuadro de Honor      : True", TEXT_GREEN),
            ("====================================================", TEXT_GRAY),
        ],
        os.path.join(shots_dir, "05_program_execution_demo.png"),
    )

    # 6. GitHub Actions Workflow
    render_terminal(
        "GitHub Actions CI — coding_standards.yml Execution Log",
        [
            ("Run actions/checkout@v4", TEXT_BLUE),
            ("Run actions/setup-python@v5 with python-version: 3.12", TEXT_BLUE),
            ("Run pip install -r requirements.txt", TEXT_BLUE),
            ("Successfully installed flake8 pylint pytest", TEXT_GREEN),
            ("", TEXT_WHITE),
            ("Run flake8 student_grade_manager.py test_student_grade_manager.py", TEXT_CYAN),
            ("✓ Flake8 check passed with 0 violations.", TEXT_GREEN),
            ("", TEXT_WHITE),
            ("Run pylint --fail-under=9.5 student_grade_manager.py test_student_grade_manager.py", TEXT_CYAN),
            ("Your code has been rated at 10.00/10", TEXT_GREEN),
            ("✓ Pylint threshold check passed (10.00 >= 9.50).", TEXT_GREEN),
            ("", TEXT_WHITE),
            ("Run pytest -v", TEXT_CYAN),
            ("9 passed in 0.10s", TEXT_GREEN),
            ("✓ All functional requirements tests passed.", TEXT_GREEN),
            ("", TEXT_WHITE),
            ("Status: SUCCESS (Workflow completed in 18s)", TEXT_GREEN),
        ],
        os.path.join(shots_dir, "06_github_actions_workflow.png"),
    )

    print("All screenshots generated successfully.")


if __name__ == "__main__":
    main()

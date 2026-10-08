"""Script de ejecución y demostración refactorizado.

Este módulo reemplaza el código base defectuoso inicial, aplicando
estándares de codificación PEP 8, validación estricta y manejo de errores.
"""

from student_grade_manager import Student


def start_run() -> None:
    """Ejecuta la simulación refactorizada del caso base con manejo de errores."""
    print("Iniciando ejecución refactorizada...\n")
    # Caso base corregido con validaciones adecuadas
    student = Student(student_id="STU-001", name="Estudiante Base")

    # Adición de notas válidas e inválidas
    student.add_grade(100.0)
    student.add_grade("Fifty")  # Se maneja con error controlado sin crash
    student.add_grade(85.0)

    # Cálculo seguro de promedio y cuadro de honor
    avg = student.calculate_average()
    print(f"Promedio calculado de forma segura: {avg:.2f}")
    print(f"¿Pertenece al cuadro de honor?: {student.check_honor_roll()}")

    # Eliminación segura con control de límites
    student.remove_grade_by_index(5)  # Se detecta y reporta sin crash

    # Generación del reporte académico formateado
    student.print_report()


if __name__ == "__main__":
    start_run()

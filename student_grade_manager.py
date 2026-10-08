"""Student Grade Management System.

This module provides classes and functions to manage student records,
grades, calculations (averages, letter grades, pass/fail status, honor roll),
and formatted reporting while enforcing coding standards (PEP 8).
"""

from typing import Any, Optional

# Constants for grading thresholds and boundaries
MIN_GRADE: float = 0.0
MAX_GRADE: float = 100.0
PASSING_THRESHOLD: float = 60.0
HONOR_ROLL_THRESHOLD: float = 90.0

GRADE_A_MIN: float = 90.0
GRADE_B_MIN: float = 80.0
GRADE_C_MIN: float = 70.0
GRADE_D_MIN: float = 60.0


class Student:
    """Represents a student and their academic grading records.

    Attributes:
        student_id (str): Unique identifier of the student.
        name (str): Full name of the student.
        grades (list[float]): Collection of recorded numerical grades.
    """

    def __init__(self, student_id: str, name: str) -> None:
        """Initialize a new Student record with ID and Name validation.

        Args:
            student_id: Unique identifier for the student.
            name: Full name of the student.
        """
        clean_id = str(student_id).strip()
        clean_name = str(name).strip()

        if not clean_id or not clean_name:
            print(
                f"[Error de Validación] El ID ('{student_id}') y el nombre "
                f"('{name}') no pueden estar vacíos."
            )

        self.student_id: str = clean_id
        self.name: str = clean_name
        self.grades: list[float] = []

    def add_grade(self, grade: Any) -> bool:
        """Add a numeric grade within the valid range [0, 100].

        Args:
            grade: Numerical grade value to append.

        Returns:
            bool: True if grade was successfully validated and added,
                  False otherwise.
        """
        if not isinstance(grade, (int, float)) or isinstance(grade, bool):
            print(
                f"[Error] La calificación '{grade}' debe ser un valor "
                "numérico (int o float)."
            )
            return False

        numeric_grade = float(grade)
        if not MIN_GRADE <= numeric_grade <= MAX_GRADE:
            print(
                f"[Error] La calificación {numeric_grade} está fuera del rango "
                f"permitido [{MIN_GRADE}, {MAX_GRADE}]."
            )
            return False

        self.grades.append(numeric_grade)
        return True

    def calculate_average(self) -> float:
        """Calculate the arithmetic mean of all registered grades.

        Returns:
            float: Average grade, or 0.0 if no grades are recorded.
        """
        if not self.grades:
            return 0.0
        return sum(self.grades) / len(self.grades)

    def get_letter_grade(self) -> str:
        """Convert the student's average grade into a letter grade.

        Returns:
            str: Letter grade ('A', 'B', 'C', 'D', or 'F').
        """
        avg = self.calculate_average()
        if avg >= GRADE_A_MIN:
            return "A"
        if avg >= GRADE_B_MIN:
            return "B"
        if avg >= GRADE_C_MIN:
            return "C"
        if avg >= GRADE_D_MIN:
            return "D"
        return "F"

    def get_pass_fail_status(self) -> str:
        """Determine whether the student passed or failed.

        Returns:
            str: 'Passed' if average is >= 60, otherwise 'Failed'.
        """
        return "Passed" if self.calculate_average() >= PASSING_THRESHOLD else "Failed"

    @property
    def is_honor_roll(self) -> bool:
        """Determine whether the student qualifies for the Honor Roll.

        Returns:
            bool: True if average >= 90, otherwise False.
        """
        return self.calculate_average() >= HONOR_ROLL_THRESHOLD

    def check_honor_roll(self) -> bool:
        """Explicit method to check honor roll qualification.

        Returns:
            bool: True if average >= 90, otherwise False.
        """
        return self.is_honor_roll

    def remove_grade_by_index(self, index: int) -> bool:
        """Remove a grade specified by its zero-based index.

        Args:
            index: Zero-based position of the grade to remove.

        Returns:
            bool: True if removed successfully, False if out of bounds.
        """
        if not isinstance(index, int) or isinstance(index, bool):
            print(f"[Error] El índice '{index}' debe ser un entero.")
            return False

        if index < 0 or index >= len(self.grades):
            max_idx = max(0, len(self.grades) - 1)
            print(
                f"[Error] Índice {index} fuera de rango. "
                f"Rango válido: [0, {max_idx}]."
            )
            return False

        removed_grade = self.grades.pop(index)
        print(f"[Éxito] Calificación {removed_grade} eliminada en el índice {index}.")
        return True

    def remove_grade_by_value(self, value: Any) -> bool:
        """Remove the first occurrence of a grade by its numerical value.

        Args:
            value: Numerical value to find and remove.

        Returns:
            bool: True if removed successfully, False if not found or invalid.
        """
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            print(f"[Error] El valor a remover '{value}' debe ser numérico.")
            return False

        target_value = float(value)
        try:
            self.grades.remove(target_value)
            print(f"[Éxito] Calificación {target_value} eliminada exitosamente.")
            return True
        except ValueError:
            print(
                f"[Error] La calificación {target_value} no existe "
                "en los registros."
            )
            return False

    def generate_report(self) -> str:
        """Generate a formatted academic summary report.

        Returns:
            str: Multi-line string report containing all student metrics.
        """
        avg = self.calculate_average()
        letter = self.get_letter_grade()
        status = self.get_pass_fail_status()
        honor = self.is_honor_roll
        count = len(self.grades)

        header_border = "=" * 52
        lines = [
            header_border,
            "       REPORTE DE RENDIMIENTO DEL ESTUDIANTE",
            header_border,
            f"ID del Estudiante    : {self.student_id}",
            f"Nombre               : {self.name}",
            f"Total de Notas       : {count}",
            f"Promedio Obtenido    : {avg:.2f}",
            f"Calificación Letra   : {letter}",
            f"Estado Académico     : {status}",
            f"Cuadro de Honor      : {honor}",
            header_border,
        ]
        return "\n".join(lines)

    def print_report(self) -> None:
        """Print the generated summary report to the standard output."""
        print(self.generate_report())


class StudentGradeManager:
    """Manages a registry of students and provides batch operations."""

    def __init__(self) -> None:
        """Initialize an empty student registry."""
        self.students: dict[str, Student] = {}

    def add_student(self, student_id: str, name: str) -> Optional[Student]:
        """Create and register a new student if inputs are valid.

        Args:
            student_id: Non-empty unique student identifier.
            name: Non-empty student name.

        Returns:
            Optional[Student]: Created Student instance, or None if invalid.
        """
        clean_id = str(student_id).strip()
        clean_name = str(name).strip()

        if not clean_id or not clean_name:
            print(
                "[Error] No se puede registrar estudiante: el ID y el nombre "
                "no pueden estar vacíos."
            )
            return None

        if clean_id in self.students:
            print(f"[Error] Ya existe un estudiante con el ID '{clean_id}'.")
            return None

        student = Student(clean_id, clean_name)
        self.students[clean_id] = student
        print(f"[Éxito] Estudiante '{clean_name}' (ID: {clean_id}) registrado.")
        return student

    def get_student(self, student_id: str) -> Optional[Student]:
        """Retrieve a student by their ID.

        Args:
            student_id: ID of the student to look up.

        Returns:
            Optional[Student]: Student instance if found, None otherwise.
        """
        clean_id = str(student_id).strip()
        student = self.students.get(clean_id)
        if not student:
            print(f"[Error] Estudiante con ID '{clean_id}' no encontrado.")
            return None
        return student


def main() -> None:
    """Demonstrate the Student Grade Management System functionality."""
    print("=== SISTEMA DE GESTIÓN DE CALIFICACIONES DE ESTUDIANTES ===\n")
    manager = StudentGradeManager()

    # 1. Validación de entradas al crear estudiantes
    print("1. Registro de Estudiantes:")
    manager.add_student("  ", "")  # Inválido
    student_ana = manager.add_student("STU001", "Ana Gomez")
    student_carlos = manager.add_student("STU002", "Carlos Perez")

    if student_ana:
        # 2. Agregar calificaciones válidas e inválidas
        print("\n2. Adición de Calificaciones para Ana:")
        student_ana.add_grade(95.0)
        student_ana.add_grade(92.5)
        student_ana.add_grade(88.0)
        student_ana.add_grade("Cien")  # Inválido: no numérico
        student_ana.add_grade(150.0)   # Inválido: fuera de rango

        # 3. Remover calificación por índice y valor con manejo de errores
        print("\n3. Eliminación de Calificaciones:")
        student_ana.remove_grade_by_index(10)      # Inválido: fuera de rango
        student_ana.remove_grade_by_value(50.0)    # Inválido: no existe
        student_ana.remove_grade_by_value(88.0)    # Válido
        student_ana.add_grade(98.0)                # Válido

        # 4. Reporte para estudiante de Cuadro de Honor
        print("\n4. Reporte de Ana:")
        student_ana.print_report()

    if student_carlos:
        print("\n5. Calificaciones y Reporte para Carlos:")
        student_carlos.add_grade(55.0)
        student_carlos.add_grade(62.0)
        student_carlos.print_report()


if __name__ == "__main__":
    main()

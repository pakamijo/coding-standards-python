"""Unit tests for the Student Grade Management System.

Tests verify all core and extended functional requirements:
1. Add students
2. Add grades (range 0-100)
3. Calculate average grade
4. Determine letter grade (A, B, C, D, F)
5. Determine pass/fail status
6. Handle invalid inputs gracefully without crashing
7. Honor roll detection (boolean)
8. Remove grades by value and by index
9. Generate formatted summary report
"""

# pylint: disable=redefined-outer-name


import pytest

from student_grade_manager import (
    GRADE_A_MIN,
    GRADE_B_MIN,
    GRADE_C_MIN,
    GRADE_D_MIN,
    MAX_GRADE,
    MIN_GRADE,
    Student,
    StudentGradeManager,
)


@pytest.fixture
def sample_student() -> Student:
    """Fixture providing a fresh student instance for testing."""
    return Student(student_id="STU100", name="Alice Smith")


def test_req1_add_students() -> None:
    """Req 1: Verify student creation with name and ID."""
    student = Student("STU001", "John Doe")
    assert student.student_id == "STU001"
    assert student.name == "John Doe"
    assert not student.grades

    manager = StudentGradeManager()
    created = manager.add_student("STU002", "Jane Doe")
    assert created is not None
    assert manager.get_student("STU002") is not None


def test_req2_add_grades_valid(sample_student: Student) -> None:
    """Req 2: Verify adding valid numeric grades within 0-100."""
    assert sample_student.add_grade(95.0) is True
    assert sample_student.add_grade(72.5) is True
    assert sample_student.add_grade(MIN_GRADE) is True
    assert sample_student.add_grade(MAX_GRADE) is True
    assert sample_student.grades == [95.0, 72.5, 0.0, 100.0]


def test_req3_calculate_average(sample_student: Student) -> None:
    """Req 3: Verify arithmetic mean calculation."""
    assert sample_student.calculate_average() == 0.0

    sample_student.add_grade(80.0)
    sample_student.add_grade(90.0)
    sample_student.add_grade(100.0)
    assert sample_student.calculate_average() == 90.0


def test_req4_determine_letter_grade(sample_student: Student) -> None:
    """Req 4: Verify letter grade conversion (A, B, C, D, F)."""
    # Grade A: >= 90
    sample_student.grades = [GRADE_A_MIN]
    assert sample_student.get_letter_grade() == "A"

    # Grade B: 80 - 89.9
    sample_student.grades = [GRADE_B_MIN]
    assert sample_student.get_letter_grade() == "B"

    # Grade C: 70 - 79.9
    sample_student.grades = [GRADE_C_MIN]
    assert sample_student.get_letter_grade() == "C"

    # Grade D: 60 - 69.9
    sample_student.grades = [GRADE_D_MIN]
    assert sample_student.get_letter_grade() == "D"

    # Grade F: < 60
    sample_student.grades = [59.9]
    assert sample_student.get_letter_grade() == "F"


def test_req5_determine_pass_fail(sample_student: Student) -> None:
    """Req 5: Verify pass/fail status determination."""
    sample_student.grades = [60.0]
    assert sample_student.get_pass_fail_status() == "Passed"

    sample_student.grades = [59.9]
    assert sample_student.get_pass_fail_status() == "Failed"


def test_req6_handle_invalid_inputs(sample_student: Student) -> None:
    """Req 6: Verify validation of grades, IDs, names without crashing."""
    # Non-numeric grade
    assert sample_student.add_grade("Fifty") is False
    assert sample_student.add_grade(None) is False
    assert sample_student.add_grade([10]) is False

    # Grade out of range
    assert sample_student.add_grade(-1.0) is False
    assert sample_student.add_grade(101.0) is False

    # Manager empty ID and Name handling
    manager = StudentGradeManager()
    assert manager.add_student("", "Valid Name") is None
    assert manager.add_student("ID123", "") is None
    assert manager.add_student("   ", "   ") is None


def test_req7_honor_roll_detection(sample_student: Student) -> None:
    """Req 7: Verify honor roll detection returns boolean True/False."""
    sample_student.grades = [90.0, 95.0]
    assert sample_student.is_honor_roll is True
    assert sample_student.check_honor_roll() is True

    sample_student.grades = [89.9]
    assert sample_student.is_honor_roll is False
    assert sample_student.check_honor_roll() is False


def test_req8_remove_grade_by_index_and_value(sample_student: Student) -> None:
    """Req 8: Verify grade removal with graceful error handling."""
    sample_student.add_grade(95.0)
    sample_student.add_grade(85.0)
    sample_student.add_grade(75.0)

    # Valid remove by index
    assert sample_student.remove_grade_by_index(1) is True
    assert sample_student.grades == [95.0, 75.0]

    # Invalid index (out of range)
    assert sample_student.remove_grade_by_index(10) is False
    assert sample_student.remove_grade_by_index(-1) is False

    # Valid remove by value
    assert sample_student.remove_grade_by_value(95.0) is True
    assert sample_student.grades == [75.0]

    # Invalid remove by value (not in list)
    assert sample_student.remove_grade_by_value(100.0) is False
    # Non-numeric value
    assert sample_student.remove_grade_by_value("invalid") is False


def test_req9_generate_summary_report(sample_student: Student) -> None:
    """Req 9: Verify formatted summary report output."""
    sample_student.add_grade(92.0)
    sample_student.add_grade(96.0)
    report = sample_student.generate_report()

    assert "STU100" in report
    assert "Alice Smith" in report
    assert "Total de Notas" in report
    assert "94.00" in report
    assert "Calificación Letra   : A" in report
    assert "Estado Académico     : Passed" in report
    assert "Cuadro de Honor      : True" in report

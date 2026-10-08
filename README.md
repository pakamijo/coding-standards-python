# Sistema de Gestión de Calificaciones de Estudiantes (Student Grade Management System)

[![Coding Standards CI](https://github.com/pakamijo/coding-standards-python/actions/workflows/coding_standards.yml/badge.svg)](https://github.com/pakamijo/coding-standards-python/actions/workflows/coding_standards.yml)
![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)
![Pylint Score](https://img.shields.io/badge/pylint-10.00%2F10-brightgreen.svg)
![Flake8](https://img.shields.io/badge/flake8-0%20violations-brightgreen.svg)
![Tests](https://img.shields.io/badge/tests-9%2F9%20passed-brightgreen.svg)

Actividad de laboratorio de **Estándares de Codificación (Coding Standards - SW2)** enfocada en la auditoría estática, refactorización dirigida por calidad (PEP 8) e integración continua (CI/CD) para Python en Visual Studio Code.

---

## 📌 Resumen del Proyecto

Este repositorio contiene la resolución integral de la actividad de estándares de codificación:
1. **Código Base Inicial:** Evaluación del código original defectuoso (`test.py`) con Pylint y Flake8, documentando 18 infracciones críticas y una calificación de **0.91 / 10**.
2. **Refactorización Completa:** Implementación orientada a objetos en `student_grade_manager.py` alcanzando un puntaje perfecto de **10.00 / 10** en Pylint y **0 advertencias** en Flake8.
3. **Requerimientos Funcionales:** Cumplimiento del 100% de los requerimientos base y extendidos (registro de estudiantes, calificaciones, promedios, notas en letra, aprobación/reprobación, cuadro de honor, eliminación por índice/valor y reporte formateado).
4. **Pruebas Automatizadas:** Suite de 9 pruebas unitarias con Pytest verificando cada requerimiento.
5. **CI/CD con GitHub Actions (Challenge):** Flujo de trabajo automatizado que ejecuta Flake8, Pylint y Pytest en cada Pull Request y push a la rama `main`.

---

## 🛠️ Tecnologías y Entorno

- **Lenguaje:** Python 3.12
- **Editor:** Visual Studio Code con configuración en `.vscode/settings.json`
- **Gestión de Entorno Virtual:** `python3 -m venv .venv`
- **Herramientas de Estándares de Codificación:**
  - `pylint`: Análisis estático profundo, métricas de calidad y diseño de clases.
  - `flake8`: Verificación estricta de estilo PEP 8 y errores de sintaxis.
  - `flake8-html` y `pylint-json2html`: Generación de reportes visuales en formato HTML.
- **Framework de Pruebas:** `pytest`
- **Control de Versiones y CLI:** `git` y `gh` (GitHub CLI)
- **Integración Continua:** GitHub Actions

---

## 🚀 Instalación y Puesta en Marcha

### 1. Clonar el Repositorio
```bash
git clone https://github.com/pakamijo/coding-standards-python.git
cd coding-standards-python
```

### 2. Configurar el Entorno Virtual (`.venv`)
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🧪 Ejecución de Auditorías y Pruebas

### Ejecutar Flake8 (Estándares PEP 8)
```bash
flake8 student_grade_manager.py test_student_grade_manager.py test.py
```

### Ejecutar Pylint (Calidad y Diseño)
```bash
pylint student_grade_manager.py test_student_grade_manager.py test.py
```

### Ejecutar Pruebas Unitarias con Pytest
```bash
pytest -v
```

### Ejecutar la Demostración del Sistema
```bash
python student_grade_manager.py
# O ejecutar el runner refactorizado:
python test.py
```

---

## 📊 Comparativa de Métricas de Calidad

| Métrica | Código Base Inicial | Código Refactorizado Final |
| :--- | :---: | :---: |
| **Calificación Pylint** | `0.91 / 10` | **`10.00 / 10`** |
| **Infracciones Pylint** | 18 violaciones / errores | **0 violaciones** |
| **Infracciones Flake8** | F841 (variable no usada) | **0 violaciones** |
| **Estabilidad Runtime** | Crash fatal (`TypeError`, `ZeroDivisionError`) | **Robusto con validación de entradas** |
| **Pruebas Unitarias** | 0 pruebas | **9 / 9 pruebas aprobadas (100%)** |
| **Documentación** | Sin docstrings | **PEP 257 completo + Type Hints** |

---

## 📁 Estructura del Proyecto

```text
├── .github/
│   └── workflows/
│       └── coding_standards.yml      # Challenge: Workflow de GitHub Actions (CI)
├── .vscode/
│   └── settings.json                 # Configuración de Python y linters en VS Code
├── reports/
│   ├── index.html                    # Dashboard interactivo de reportes
│   ├── initial/                      # Reporte inicial (Pylint HTML y Flake8 HTML)
│   ├── final/                        # Reporte final con 0 infracciones (HTML)
│   └── screenshots/                  # Capturas de evidencia del proceso
├── .flake8                           # Configuración de reglas para Flake8
├── .gitignore                        # Archivos excluidos de Git
├── .pylintrc                         # Configuración personalizada de Pylint
├── generate_screenshots.py           # Generador de capturas de evidencia
├── requirements.txt                  # Dependencias del proyecto
├── student_grade_manager.py          # Implementación principal con todas las reglas
├── test_student_grade_manager.py     # Suite de 9 pruebas funcionales en Pytest
├── test.py                           # Runner de demostración refactorizado
└── INFORME_LABORATORIO_ESTANDARES_CODIGO.md # Informe formal de laboratorio (Español)
```

---

## 📄 Reportes HTML
Los reportes completos generados por las herramientas están disponibles en la carpeta `reports/`:
- **Dashboard Global:** [`reports/index.html`](reports/index.html)
- **Reporte Inicial Pylint:** [`reports/initial/pylint_report.html`](reports/initial/pylint_report.html)
- **Reporte Final Pylint:** [`reports/final/pylint_report.html`](reports/final/pylint_report.html)
- **Reporte Final Flake8:** [`reports/final/flake8/index.html`](reports/final/flake8/index.html)

---

## 👤 Autor
- **Estudiante:** Adrian Toledo
- **Repositorio:** [https://github.com/pakamijo/coding-standards-python](https://github.com/pakamijo/coding-standards-python)

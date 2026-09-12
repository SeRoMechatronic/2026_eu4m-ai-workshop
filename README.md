# IA aplicada con verificación para EU4M

Material completo para un curso presencial de 8 horas dirigido a estudiantes del
primer semestre de EU4M en la Universidad de Oviedo.

La versión formal para coordinación está en
[Propuesta_final_EU4M_IA_verificada.docx](docs/Propuesta_final_EU4M_IA_verificada.docx).

El curso combina trabajo académico y una práctica mecatrónica. Cada uso relevante
de inteligencia artificial sigue el protocolo PVRD:

1. **Prompt**: definir propósito, contexto y criterio de aceptación.
2. **Verificar**: contrastar la salida con una fuente, cálculo, prueba o dato.
3. **Refinar**: corregir la salida o reformular la petición.
4. **Documentar**: registrar la decisión, los cambios y los límites.

## Inicio rápido

### Estudiantes

1. Lea [la guía del estudiante](docs/student_guide.md).
2. Descargue las plantillas de [registro PVRD](templates/pvrd_log.csv) y
   [matriz de fuentes](templates/source_matrix.csv).
3. Abra el
   [notebook del caso del actuador](notebooks/03_actuator_case_student.ipynb).
4. Conserve todas sus evidencias hasta el cierre del curso.

[Abrir el notebook en Colab](https://colab.research.google.com/github/SeRoMechatronic/2026_eu4m-ai-workshop/blob/main/notebooks/03_actuator_case_student.ipynb)
cuando el repositorio sea público. Si continúa privado, siga la
[configuración de Colab](docs/colab_setup.md). El notebook también funciona
localmente con Python 3.10 o posterior.

### Docente

1. Lea [la guía docente](docs/instructor_guide.md).
2. Revise [la política de herramientas](docs/tool_policy.md) con la coordinación.
3. Ejecute la comprobación completa:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/run_all.py
```

4. Utilice el [plan de contingencia](docs/contingency_plan.md) si falla internet o
   una herramienta externa.
5. Complete la [lista de comprobación](docs/release_checklist.md).

## Estructura

| Ruta | Contenido |
|---|---|
| `slides/` | Cuatro presentaciones editables, una por módulo |
| `docs/` | Programa, guías, política, accesibilidad y referencias |
| `activities/` | Enunciados para los cuatro módulos |
| `templates/` | Entregables editables |
| `notebooks/` | Notebook del estudiante y versión resuelta |
| `data/` | Datos sintéticos por escenario y metadatos de generación |
| `results/` | Características y resultados de referencia |
| `instructor/` | Soluciones, claves y rúbricas |
| `src/`, `scripts/`, `tests/` | Caso reproducible y validación automática |

## Límites del caso técnico

El actuador es un modelo sintético de una masa controlada por PD. Sirve para
enseñar verificación, diseño de pruebas y razonamiento sobre fallos. No representa
un actuador industrial concreto y sus resultados no deben presentarse como
validación de un sistema de diagnóstico real.

La justificación del alcance se documenta en
[decisiones de diseño](docs/design_rationale.md) y la procedencia de las
afirmaciones en [procedencia y contraste](docs/provenance.md).

## Licencias

- Código: licencia MIT.
- Diapositivas, guías y actividades: Creative Commons Attribution 4.0.
- Las publicaciones citadas mantienen sus licencias originales.

## Autor

José Sebastián Rojas Ordóñez  
Antiguo alumno de EU4M  
Investigador predoctoral en IKERLAN y University of the Basque Country (UPV/EHU)

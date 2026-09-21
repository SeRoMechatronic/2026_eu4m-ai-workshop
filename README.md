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

## Este es el repositorio maestro

Contiene soluciones, la clave del reto, las diapositivas con notas y las pruebas.
**No debe publicarse.** El alumnado recibe solo `dist/student_pack/`, que
`scripts/build_packs.py` genera con una lista blanca y comprueba (sin soluciones,
sin casos del reto, sin enlaces rotos).

| Audiencia | Qué recibe | Dónde |
|---|---|---|
| Estudiantes | `dist/student_pack/` | Repositorio público (Colab abre de ahí) |
| Docente | `dist/instructor_kit/`: todo, más `handouts/` y `offline/` | Portátil, USB y nube personal |

## Inicio rápido (docente)

Requiere Python 3.10 o posterior.

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
python scripts/run_all.py          # datos, notebooks, figuras, pruebas y preflight
python scripts/build_packs.py --offline --zip --out ../eu4m_dist
```

Use una carpeta de salida **fuera de OneDrive**: OneDrive puede bloquear el borrado de
carpetas recién creadas. Después:

1. Lea [la guía docente](docs/instructor_guide.md) y la
   [política de herramientas](docs/tool_policy.md).
2. Publique el repositorio de estudiantes con `scripts/prepare_public_repo.py` (véase
   [colab_setup.md](docs/colab_setup.md)).
3. Ejecute `python scripts/check_public_urls.py`.
4. Complete la [lista de comprobación](docs/release_checklist.md) y consulte el
   [plan de contingencia](docs/contingency_plan.md).

## Portabilidad

El notebook del caso es autocontenido: incluye el simulador y prueba tres fuentes de
datos (archivos locales, GitHub, simulador integrado), aceptando solo la que
coincide con la huella SHA-256 registrada. Funciona igual en Colab, Jupyter local y
sin conexión. El kit del docente añade los notebooks ya ejecutados en HTML, las
diapositivas en PDF y sus notas en texto.

### Entornos verificados

| Entorno | Resultado |
|---|---|
| Windows · Python 3.11.9 · pandas 3.0.2 · numpy 2.2.3 · matplotlib 3.10.8 | Pruebas y `run_all.py` correctos |
| Windows · Python 3.11.9 · pandas 2.3.3 · numpy 2.4.6 · matplotlib 3.11.2 | Pruebas y `run_all.py` correctos |
| GitHub Actions: Linux 3.11, Linux 3.10 con `pandas<3`, Windows 3.11 | Definidos en `.github/workflows/ci.yml` |

Los hashes de datos son idénticos en todas las combinaciones probadas.

## Estructura

| Ruta | Contenido |
|---|---|
| `slides/` | Cuatro presentaciones editables con notas y tiempos, una por módulo |
| `docs/` | Programa, guías, política, accesibilidad y referencias |
| `activities/` | Enunciados para los cuatro módulos |
| `templates/` | Entregables editables |
| `notebooks/` | Comprobación de acceso, notebook del estudiante y versión resuelta |
| `data/` | Datos sintéticos por escenario, metadatos y casos del reto (solo instructor) |
| `results/` | Características y resultados de referencia |
| `instructor/` | Soluciones, clave y generador del reto, rúbricas |
| `packs/` | README y requisitos del paquete de estudiantes |
| `src/`, `scripts/`, `tests/` | Caso reproducible, herramientas de construcción y validación |

### Scripts

| Script | Función |
|---|---|
| `run_all.py` | Regenera datos, notebooks y figuras; ejecuta notebooks, pruebas y `preflight` |
| `generate_dataset.py` | Datos por escenario, resultados y `metadata.json` con huellas |
| `build_notebooks.py` | Construye los tres notebooks desde celdas revisadas |
| `build_agenda.py` | Regenera la agenda de la guía docente desde las notas de las diapositivas |
| `build_packs.py` | Paquete de estudiantes (verificado) y kit del docente |
| `prepare_public_repo.py` | Crea el repositorio público local (1 commit y etiqueta), sin publicar |
| `check_public_urls.py` | Comprueba el repositorio público tras publicarlo |
| `export_offline.py` | HTML ejecutado, notas y PDF de las diapositivas |
| `instructor/generate_challenge_cases.py` | Casos A, B y C con semilla privada |

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

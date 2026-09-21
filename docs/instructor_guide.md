# Guía docente

## Propósito

Esta guía permite impartir el curso sin depender de una marca concreta de IA. La
actividad gira alrededor del protocolo PVRD y de un único caso mecatrónico.

## Qué contiene cada repositorio

Este repositorio es el **maestro y privado**: incluye soluciones, la clave del reto,
las diapositivas con notas y las pruebas. El alumnado recibe solo el paquete que
genera `scripts/build_packs.py`:

| Salida | Contenido | Destino |
|---|---|---|
| `dist/student_pack/` | Guías, actividades, plantillas, notebooks de estudiante, datos y simulador | Repositorio **público** (Colab abre de ahí) |
| `dist/instructor_kit/` | Todo el maestro, `handouts/` (casos A, B y C) y `offline/` (HTML ejecutado y PDF) | Portátil del docente y USB |

`build_packs.py` rechaza el paquete de estudiantes si contiene una solución, la
clave, un caso del reto, una diapositiva o un enlace roto.

## Preparación siete días antes

- Confirmar horario, aula, tamaño del grupo (hasta 30 estudiantes) y carácter evaluable.
- Confirmar qué asistentes de IA autoriza la Universidad.
- Ejecutar `python scripts/run_all.py` en un entorno limpio.
- Generar los paquetes: `python scripts/build_packs.py --offline --zip`.
- Publicar el contenido de `dist/student_pack/` en el repositorio público y crear la
  etiqueta `v1.0.0` (los notebooks descargan los datos de esa etiqueta).
- Ejecutar `python scripts/check_public_urls.py`: comprueba que los enlaces públicos
  responden y que los datos descargados tienen la huella esperada.
- Probar Colab con una cuenta de profesor y **dos cuentas ordinarias de estudiante EU4M**
  (véase [colab_setup.md](colab_setup.md)).
- Enviar al alumnado, 3–4 días antes, el enlace del repositorio público y la
  comprobación de acceso (`notebooks/00_access_check.ipynb`).
- Copiar `dist/instructor_kit/` a un USB y a la nube personal.

## Preparación el mismo día

- Abrir localmente las cuatro presentaciones (o sus PDF de `offline/`).
- Mantener una copia local del dataset y del notebook resuelto.
- Tener a mano `handouts/case_A.csv`, `case_B.csv` y `case_C.csv`.
- Preparar una respuesta errónea real de la herramienta que se vaya a demostrar.
- No utilizar datos internos de IKERLAN, UPV/EHU, EU4M o proyectos de estudiantes.

## Agenda detallada

Los tiempos salen de las notas de las diapositivas y esta sección se regenera con
`python scripts/build_agenda.py`; una prueba automática falla si se desincroniza.
La propuesta `.docx` describe los mismos bloques con menos detalle. En ambas fuentes
cada módulo suma 120 minutos, y en el módulo 4 los cinco bloques coinciden.

<!-- agenda:start -->

### Módulo 1  Usar IA con criterio  (120 min)

| Minutos | Diapositiva | Contenido | Acción docente |
|---:|---:|---|---|
| 0–5 | 1 | Usar IA con criterio | Bienvenida y encuadre. |
| 5–10 | 2 | Resultado de estas dos horas | Explique el contrato de aprendizaje y muestre templates/pvrd_log.csv. |
| 10–20 | 3 | Qué hace bien un modelo generativo | Pida ejemplos del grupo. |
| 20–28 | 4 | Dónde se rompe la confianza | Ejemplo oral: un DOI verosímil no es evidencia hasta resolverlo. |
| 28–38 | 5 | La regla central | Haga que el grupo reformule una salida de IA como hipótesis comprobable. |
| 38–48 | 6 | PVRD: el ciclo de trabajo | Modele una entrada completa en pvrd_log.csv. |
| 48–58 | 7 | Un prompt que se puede evaluar | Trabajo guiado: cada pareja mejora un prompt propio con los cuatro bloques. |
| 58–88 | 8 | Actividad · Auditoría de una respuesta | Use activities/module_1_claim_audit.md. |
| 88–98 | 9 | ¿Qué prueba corresponde a qué afirmación? | Debrief de la actividad. |
| 98–106 | 10 | Datos, privacidad y acceso | Abra docs/tool_policy.md. |
| 106–113 | 11 | Si la herramienta falla, el aprendizaje continúa | Muestre docs/contingency_plan.md. |
| 113–120 | 12 | Cierre del módulo | Comprobación individual: 60 segundos para escribir respuesta. |

### Módulo 2  Investigación y comunicación académica  (120 min)

| Minutos | Diapositiva | Contenido | Acción docente |
|---:|---:|---|---|
| 0–5 | 1 | Investigación académica | Recupere PVRD. |
| 5–10 | 2 | Producto del módulo | Muestre templates/source_matrix.csv y el criterio de evaluación de instructor/rubric.md. |
| 10–20 | 3 | Una pregunta que guía la búsqueda | Cada estudiante transforma un tema propio. |
| 20–28 | 4 | La IA ayuda a diseñar la búsqueda | La IA puede sugerir sinónimos; no debe inventar el conjunto final de artículos. |
| 28–36 | 5 | Jerarquía práctica de comprobación | Aclare que una fuente ‘de nivel alto’ puede no ser pertinente. |
| 36–46 | 6 | DOI ≠ evidencia completa | Demuéstrelo con DOI 10.1016/j.arcontrol.2004.12.002. |
| 46–76 | 7 | Actividad · Verificar tres referencias | Use activities/module_2_source_verification.md y source_packet.md. |
| 76–91 | 8 | De la matriz a la síntesis | Cada pareja redacta tres frases: convergencia, diferencia y vacío. |
| 91–99 | 9 | Paráfrasis, traducción y citas | Ejercicio oral: transformar ‘proves’ en ‘reports under…’. |
| 99–106 | 10 | Tres trampas frecuentes | Pida al grupo una versión corregida de cada trampa. |
| 106–113 | 11 | Revisión entre pares en 90 segundos | Intercambio de matrices. |
| 113–120 | 12 | Cierre del módulo | Recoja la fila corregida. |

### Módulo 3  IA en una tarea mecatrónica  (120 min)

| Minutos | Diapositiva | Contenido | Acción docente |
|---:|---:|---|---|
| 0–5 | 1 | Caso mecatrónico reproducible | Presente el caso como didáctico: modelo de masa puntual controlada por PD. |
| 5–10 | 2 | Pregunta de ingeniería | Abra data/metadata.json. |
| 10–18 | 3 | El modelo cabe en tres ecuaciones | Derive verbalmente el efecto de g y del sesgo. |
| 18–26 | 4 | Diseño experimental | Muestre scripts/generate_dataset.py. |
| 26–38 | 5 | Las señales cuentan historias distintas | La figura se regenera desde los tres CSV de data/. |
| 38–46 | 6 | Contrato de datos antes del gráfico | Ejecute la celda ‘Contrato del dataset’. |
| 46–86 | 7 | Notebook · del dato a la prueba | Use notebooks/03_actuator_case_student.ipynb y activities/module_3_engineering_case.md. |
| 86–98 | 8 | Resultados: separar indicio y confirmación | Valores exactos en results/scenario_summary.csv. |
| 98–105 | 9 | La trampa del sesgo de sensor | Respuesta a la pregunta del notebook: el controlador regula la medida sesgada. |
| 105–111 | 10 | IA para código: aceptación antes que sintaxis | Conecte con tests/test_analysis.py. |
| 111–116 | 11 | Qué se puede afirmar | Pida que localicen palabras de alcance: ‘esta configuración’, ‘mediano’, ‘simulado’. |
| 116–120 | 12 | Cierre del módulo | Salida: cada estudiante propone una medición real siguiente y explica qué incertidumbre reduce. |

### Módulo 4  Reto integrado  (120 min)

| Minutos | Diapositiva | Contenido | Acción docente |
|---:|---:|---|---|
| 0–2 | 1 | Reto integrado | Explique que la evaluación premia evidencia y límites. |
| 2–6 | 2 | El reto | Entregue handouts/case_A.csv o handouts/case_B.csv, uno por pareja, al empezar el módulo. |
| 6–10 | 3 | Entregables | Plantilla: templates/engineering_brief.md. |
| 10–15 | 4 | Rúbrica visible desde el inicio | Abra instructor/rubric.md. |
| 15–20 | 5 | Una conclusión defendible tiene cuatro capas | Modele una frase que incluya las cuatro capas. |
| 20–25 | 6 | Dos fuentes, dos funciones | Fuentes recomendadas: Isermann DOI 10.1016/j.arcontrol.2004.12.002; Lei et al. DOI 10.1016/j.ymssp.2019.106587. |
| 25–65 | 7 | Producción del reto | Use activities/module_4_integrated_challenge.md. |
| 65–80 | 8 | Revisión cruzada | La crítica debe apuntar a evidencia, no estilo. |
| 80–100 | 9 | Defensa en 90 segundos | Con hasta 10 parejas defienden todas; con más, sortee 10 defensas (90 s más 30 s de cambio) y el resto entrega solo el informe. |
| 100–115 | 10 | Prueba individual de salida | Use instructor/exit_ticket.md; solución y criterios en instructor/exit_ticket_solution.md. |
| 115–118 | 11 | Transferencia a la tesis y al laboratorio | Pida una tarea de la próxima semana donde aplicarán PVRD. |
| 118–120 | 12 | Cierre del taller | Cierre y recogida. |

<!-- agenda:end -->

**Evidencia al cierre de cada módulo**

| Módulo | Evidencia |
|---|---|
| 1 | Primera entrada individual del registro PVRD, con una afirmación rechazada o corregida y su evidencia |
| 2 | Matriz individual con al menos tres fuentes comprobadas y un párrafo respaldado por ellas |
| 3 | Artefacto técnico breve con una prueba ejecutada y una conclusión que cite la evidencia |
| 4 | Informe por parejas, registro PVRD individual y prueba individual de salida |

## Notas por módulo

### Módulo 3

Antes de abrir el notebook, cada pareja escribe **dos requisitos medibles** con umbral,
unidad y condición de prueba (diez de los cuarenta minutos de la diapositiva 7). Es
el ensayo del requisito medible que se evalúa en el informe del módulo 4.

### Módulo 4

- **Casos.** Entregue `case_A.csv` a la mitad de las parejas y `case_B.csv` a la otra
  mitad. No están en el repositorio público. Los estudiantes pueden subirlos a Colab
  con `files.upload()`. Se generan con `instructor/generate_challenge_cases.py` y una
  semilla privada: no coinciden con ninguna ejecución del dataset del módulo 3.
- **Defensas.** Cada defensa dura 90 segundos más 30 de cambio, así que en 20 minutos
  caben 10. Con hasta 10 parejas defienden todas; con más, sortee 10 y el resto
  entrega solo el informe.
- **Prueba de salida.** Use `case_C.csv`: un caso que ningún equipo ha analizado.
  Puede usarse el notebook propio, pero no materiales del docente ni IA.
- **Etiquetas.** `instructor/challenge_key.json` no se comparte hasta el debrief.
- **Sobre la primera muestra.** En los casos con sesgo de sensor, la primera lectura
  ya está desplazada 0,12 m respecto de una referencia de 0 m y una velocidad
  nula. Un estudiante puede inferir un desplazamiento si asume que la masa parte de
  x = 0. Es un supuesto del simulador que el archivo no permite comprobar: acéptelo
  como hipótesis bien justificada, no como confirmación.

## Preguntas para la puesta en común

- ¿Qué parte de la respuesta podía comprobarse directamente?
- ¿Qué supuesto cambió la conclusión?
- ¿Qué evidencia faltaría para usar el resultado en un sistema real?
- ¿Qué aportó la IA que no aportaba una búsqueda o cálculo convencional?
- ¿Quién conserva la responsabilidad de la decisión?

## Uso de las soluciones

Las soluciones muestran respuestas mínimas aceptables. También se aceptan
conclusiones distintas cuando el estudiante aporta evidencia suficiente y mantiene
los límites del caso. No premie la coincidencia literal con la solución.

## Después del curso

- Conservar los entregables según la política de la Universidad.
- Registrar fallos de acceso, conceptos que consumieron más tiempo y preguntas repetidas.
- Publicar soluciones solo después de recoger la prueba individual.
- Si reutiliza el reto, regenere los casos con otra semilla privada
  (`instructor/generate_challenge_cases.py`) y actualice las soluciones.
- Actualizar enlaces y herramientas antes de cada nueva edición.

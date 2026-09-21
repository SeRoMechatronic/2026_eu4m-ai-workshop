# Decisiones de diseño

## Qué se conserva de la propuesta original

La idea central es relevante: estudiantes de primer semestre necesitan usar IA en
tareas académicas y técnicas sin confundir fluidez con evidencia. Por eso el curso
mantiene investigación, escritura, código y una aplicación mecatrónica dentro de
un único método verificable.

## Qué se cambia

Un laboratorio centrado desde el inicio en MuJoCo, clasificación de fallos y
métricas de aprendizaje automático exige demasiado contexto para ocho horas y
desplaza los resultados académicos de la propuesta. Ese enfoque puede ser una
extensión avanzada, pero no constituye el núcleo del curso.

El caso base utiliza un modelo de masa puntual controlada por PD porque permite:

- inspeccionar las ecuaciones y el código;
- regenerar los datos en segundos;
- mostrar la diferencia entre señal medida y estado real simulado;
- diseñar pruebas sin exigir experiencia previa en aprendizaje automático;
- discutir por qué un ejemplo reproducible todavía no es representativo.

## Decisión sobre IA generativa

La IA se utiliza para proponer borradores, consultas, código o interpretaciones.
La evaluación recae en la verificación: fuente, cálculo, prueba, decisión y límite.
El curso no depende de una marca, cuenta premium ni API.

## Decisión sobre portabilidad y distribución

Colab es la ruta principal por su simplicidad, pero el curso no depende de ella ni de
GitHub. Tres decisiones lo garantizan:

- **Notebook autocontenido.** Incluye el simulador (copiado literalmente de
  `simulation.py`) y prueba tres fuentes de datos, aceptando solo la que coincide con la
  huella SHA-256 registrada. Si no hay red ni archivos, regenera los datos exactos.
- **Repositorio maestro privado y paquete público.** El alumnado solo recibe lo que
  `scripts/build_packs.py` autoriza. Así las soluciones y la clave del reto no llegan
  al repositorio del que abre Colab.
- **Casos del reto fuera del dataset.** Los casos A y B proceden de una semilla privada
  y no son ejecuciones del dataset del módulo 3; el caso C alimenta la prueba de salida
  con un caso que ningún equipo ha analizado.

## Extensión avanzada sugerida

Después del curso base puede añadirse un bloque independiente de 3 a 4 horas con
simulación física, extracción de ventanas, entrenamiento y evaluación de un
clasificador. Esa extensión debe incluir separación por ejecución, prevención de
fuga de datos, línea base, incertidumbre y reproducción exacta de métricas.


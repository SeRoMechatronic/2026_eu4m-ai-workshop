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

## Extensión avanzada sugerida

Después del curso base puede añadirse un bloque independiente de 3 a 4 horas con
simulación física, extracción de ventanas, entrenamiento y evaluación de un
clasificador. Esa extensión debe incluir separación por ejecución, prevención de
fuga de datos, línea base, incertidumbre y reproducción exacta de métricas.


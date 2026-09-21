# Changelog

## 1.0.0  2026-09-12 (revisión del 2026-09-21, antes de la primera edición)

- Primera versión completa del curso presencial de 8 horas.
- Cuatro módulos con evaluación individual y por parejas.
- Caso reproducible de actuador lineal.
- Notebook del estudiante y solución.
- Guías, actividades, plantillas, rúbrica y plan de contingencia.

### Revisión previa a impartir el curso

**Portabilidad**

- El notebook es autocontenido: incluye el simulador y carga los datos desde archivos
  locales, desde una etiqueta fija de GitHub o regenerándolos, aceptando solo la fuente
  cuyo SHA-256 coincide con `data/metadata.json`.
- Nuevo notebook de comprobación de acceso para enviar al alumnado antes de la primera sesión.
- `scripts/build_packs.py` genera el paquete de estudiantes (lista blanca verificada) y
  el kit del docente; `scripts/export_offline.py` añade HTML ejecutado, PDF y notas.
- Repositorio maestro privado y repositorio público solo de estudiante.
- `scripts/check_public_urls.py` comprueba el repositorio público tras publicarlo.
- Compatible con pandas 2 y 3 (`pandas>=2.0,<4`).

**Correcciones**

- Windows: los CSV se escriben con LF y los hashes no dependen de los finales de línea
  (`run_all.py` fallaba en Windows). Se añade `.gitattributes`.
- Ya no se requiere un CSV combinado ignorado por Git: `pytest` funciona en un clon limpio.
- Reto del módulo 4: los casos A y B eran copias de ejecuciones del dataset etiquetado.
  Se regeneran con una semilla privada, se añade el caso C para la prueba de salida y
  una prueba impide que vuelvan a coincidir.
- Diapositivas: temporización del módulo 4 alineada con la guía y la propuesta (15/65/20/15/5),
  informe de una página, matriz de fuentes individual, un caso por pareja.
- La agenda de la guía docente se genera desde las notas de las diapositivas.
- Actividad 3: se añade el paso de requisitos medibles; actividad 4: defensas acotadas
  a 10 y carga del caso en Colab.
- La solución del notebook incluye la prueba del solapamiento entre pérdida del actuador y
  sesgo del sensor; la clave de la prueba de salida recoge el matiz de la primera muestra.
- El umbral de saturación sigue el límite de fuerza; se rechazan más de 100 ejecuciones
  por escenario (colisión de semillas).
- CI en Linux y Windows, con comprobación de artefactos regenerados.

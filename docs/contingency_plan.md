# Plan de contingencia

## Objetivo

Ningún incidente técnico debe consumir más de diez minutos de una actividad.

## Tres capas

| Capa | Situación | Qué se hace |
|---|---|---|
| 1. En línea | Todo funciona | Colab con el enlace del repositorio público |
| 2. Sin Colab o sin cuenta | Workspace bloquea Colab o falta una cuenta | Trabajo por parejas con el portátil de quien tenga acceso; Jupyter local en el portátil del docente |
| 3. Sin Internet | Wi-Fi caída | Kit del docente: notebook ya ejecutado en HTML, PDF de las diapositivas y entorno local |

## Rutas por incidente

| Incidente | Primera respuesta | Ruta alternativa |
|---|---|---|
| Colab bloqueado por Workspace | Confirmar cuenta correcta | Jupyter local o trabajo por parejas |
| GitHub inaccesible | El notebook usa el simulador integrado sin intervención | Copia del docente en memoria USB |
| Asistente de IA no disponible | Utilizar salida preparada | Auditar la respuesta sin conexión |
| Fallo de instalación | No depurar durante la explicación | `offline/03_actuator_case_student_ejecutado.html` y capturas |
| Internet inestable | Detener consultas externas | Paquete de fuentes y DOI ya verificados |
| Estudiante sin portátil | Formar pareja | Plantilla impresa |
| Fallo del proyector | Pasar a PDF | `offline/*.pdf` en el portátil o en USB |

## Kit que debe llevar el docente

`dist/instructor_kit/` (generado con `python scripts/build_packs.py --offline --zip`),
en un USB y en su nube personal:

- repositorio maestro completo, con soluciones e instrucciones;
- `offline/`: los notebooks ejecutados en HTML, las presentaciones en PDF y sus notas
  del orador en texto (`*_notas.md`);
- `handouts/`: `case_A.csv`, `case_B.csv` y `case_C.csv`;
- presentaciones en PPTX;
- `student_pack.zip`, para compartir sin GitHub;
- las cuatro respuestas de IA de `instructor/prepared_ai_responses.md`;
- copias impresas de las plantillas y de la prueba de salida.

## Trabajar sin conexión

El notebook del caso funciona sin red: usa los archivos locales o, si no están, el
simulador integrado, y en ambos casos verifica el SHA-256. Los módulos 1 y 2 usan
`docs/source_packet.md` con los DOI ya verificados. El módulo 4 no necesita conexión.

## Criterio para volver a la ruta principal

La clase vuelve al servicio en línea únicamente cuando el acceso funciona para
todo el grupo o cuando el trabajo por parejas garantiza que nadie queda detenido.

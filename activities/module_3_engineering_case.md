# Actividad 3  Caso del actuador

## Tiempo

60 minutos: 40 minutos de notebook (los primeros 10 se dedican a los requisitos) y
20 minutos de interpretación y discusión.

## Contexto

Una masa de 1,2 kg se mueve en una dimensión mediante un controlador PD. El
dataset incluye tres escenarios: nominal, pérdida de eficacia del actuador y sesgo
del sensor. Los parámetros varían ligeramente entre ejecuciones.

## Contrato técnico

- Periodo de muestreo: 0,02 s.
- Duración de cada ejecución: 8 s.
- Fuerza ordenada limitada a ±12 N.
- Ocho ejecuciones por escenario.
- La semilla y el identificador de ejecución quedan registrados.

## Tareas

1. **Antes de abrir el notebook**, escriba dos requisitos medibles para el actuador
   nominal. Cada uno debe indicar magnitud, umbral, unidad y condición de la prueba
   (por ejemplo, el intervalo de tiempo que se ignora).
2. Abra `notebooks/03_actuator_case_student.ipynb` y ejecute las celdas. El notebook
   busca los datos en tres lugares y solo acepta una fuente si su huella SHA-256
   coincide con la registrada.
3. Compruebe el número de filas, ejecuciones y escenarios.
4. Visualice una ejecución de cada escenario.
5. Calcule las características indicadas.
6. Indique con qué cálculo comprobaría cada requisito del paso 1 y si el escenario
   nominal lo cumple.
7. Evalúe tres afirmaciones propuestas por una IA.
8. Ejecute al menos una prueba o cálculo independiente.
9. Explique por qué `position_true_m` no estaría disponible en un sistema real.
10. Proponga la siguiente medición necesaria para confirmar un sesgo del sensor.

## Entrega

Complete la tabla final del notebook y exporte:

- una figura;
- una afirmación aceptada;
- una afirmación rechazada o modificada;
- una limitación;
- una entrada PVRD.

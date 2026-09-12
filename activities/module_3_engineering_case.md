# Actividad 3  Caso del actuador

## Tiempo

60 minutos: 40 minutos de notebook y 20 minutos de interpretación y discusión.

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

1. Abra `notebooks/03_actuator_case_student.ipynb`.
2. Compruebe el número de filas, ejecuciones y escenarios.
3. Visualice una ejecución de cada escenario.
4. Calcule las características indicadas.
5. Evalúe tres afirmaciones propuestas por una IA.
6. Ejecute al menos una prueba o cálculo independiente.
7. Explique por qué `position_true_m` no estaría disponible en un sistema real.
8. Proponga la siguiente medición necesaria para confirmar un sesgo del sensor.

## Entrega

Complete la tabla final del notebook y exporte:

- una figura;
- una afirmación aceptada;
- una afirmación rechazada o modificada;
- una limitación;
- una entrada PVRD.

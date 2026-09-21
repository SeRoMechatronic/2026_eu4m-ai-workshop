# Clave de la prueba individual

## Respuesta esperada

El estudiante puede comprobar el error medido final y la fuerza ordenada con
`case_C.csv`. No puede comprobar un sesgo de 0,12 m porque el archivo operativo no
contiene posición real ni un sensor redundante. Tampoco existe un clasificador
evaluado que justifique una precisión del 95 %. Debe pedir una medición independiente
de posición, una referencia externa o una prueba calibrada.

## Matiz: la primera muestra

En `case_C.csv` la primera lectura de posición es 0,12 m con referencia 0 m y
velocidad casi nula, y la orden inicial de fuerza es negativa (unos −2 N). Un
estudiante atento puede proponer un desplazamiento del sensor. Acepte esa observación
como **hipótesis** si señala que solo es válida suponiendo que la masa parte de
x = 0, algo que el archivo no permite comprobar. No la acepte como confirmación ni
como estimación de magnitud.

## Conclusión posible

El registro es compatible con seguimiento aparente de la referencia, pero no
confirma un sesgo del sensor. La magnitud y la causa no son observables con estas
señales. Se recomienda comparar la lectura con una medición independiente antes
de decidir sobre el sensor o el actuador.

## PVRD

La decisión debe marcar la salida como modificada o rechazada, enlazar los cálculos
ejecutados y registrar la ausencia de evidencia para la cifra de precisión.

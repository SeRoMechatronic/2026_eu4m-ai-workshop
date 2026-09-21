# Actividad 4  Reto integrado

## Tiempo

65 minutos de trabajo (incluye 15 de revisión cruzada), 20 minutos de defensas y
15 minutos de prueba individual.

## Situación

El docente entrega a cada pareja un registro denominado `case_A` o `case_B`. La
etiqueta de fallo se ha retirado. Debe preparar una recomendación técnica para
decidir la siguiente prueba, no emitir un diagnóstico industrial definitivo.

El registro no procede del dataset del módulo 3: es un ensayo nuevo, con sus propios
parámetros y ruido.

## Cargar el caso

En Colab, suba el archivo que le entregó el docente y léalo:

```python
from pathlib import Path

import pandas as pd

CASE = "case_A"  # o "case_B", según el archivo recibido
if not Path(f"{CASE}.csv").exists():
    from google.colab import files
    files.upload()  # seleccione el archivo entregado
case = pd.read_csv(f"{CASE}.csv")
case.head()
```

## Producto por parejas

Complete [la plantilla de informe](../templates/engineering_brief.md) en una página.
Debe contener:

1. pregunta técnica;
2. observaciones reproducibles;
3. una afirmación principal;
4. evidencia académica verificada;
5. explicación de la incertidumbre;
6. prueba o medición siguiente;
7. declaración del uso de IA.

## Restricciones

- No puede utilizar señales que no aparezcan en el archivo del caso.
- No puede convertir el nombre del archivo o los resultados de otros equipos en evidencia.
- No puede intentar reproducir el archivo con el simulador ni buscar su origen.
- Si los datos no permiten distinguir dos explicaciones, debe declararlo.
- Cada miembro mantiene su propio registro PVRD.

## Defensa

Cada defensa dura 90 segundos, más 30 de cambio:

- 30 segundos para la evidencia;
- 30 segundos para la conclusión y su límite;
- 30 segundos para la siguiente prueba.

En 20 minutos caben 10 defensas. Con más de 10 parejas, el docente sortea 10; las
demás entregan solo el informe.

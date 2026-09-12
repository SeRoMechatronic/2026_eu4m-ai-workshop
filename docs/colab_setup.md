# Configuración de Google Colab

## Decisión del curso

Colab es una ruta de ejecución, no un requisito pedagógico. El curso base:

- utiliza CPU;
- no necesita GPU ni TPU;
- no necesita una API generativa;
- no necesita montar Google Drive;
- puede ejecutarse localmente con Python 3.10 o posterior.

## Comprobación con cuentas EU4M

El docente debe realizar esta prueba al menos siete días antes:

1. abrir Colab con una cuenta ordinaria de estudiante EU4M;
2. confirmar que el administrador de Google Workspace permite el servicio;
3. abrir `notebooks/03_actuator_case_student.ipynb`;
4. cargar `data/actuator_signals.csv` si el repositorio todavía es privado;
5. ejecutar todas las celdas y comprobar que aparece `PASS El archivo cumple el contrato`;
6. cerrar la sesión, repetir con una segunda cuenta y registrar fecha y resultado.

## Repositorio público

Cuando el repositorio sea público, el notebook puede abrirse con:

<https://colab.research.google.com/github/SeRoMechatronic/2026_eu4m-ai-workshop/blob/main/notebooks/03_actuator_case_student.ipynb>

La primera celda lee el CSV combinado local si existe y, en caso contrario,
reconstruye el dataset desde las tres partes de la rama `main`.

## Repositorio privado

La opción más simple y segura es descargar el notebook y el CSV, abrir el notebook
en Colab y cargar el CSV en `data/actuator_signals.csv`. No introduzca un token de
GitHub en una celda ni lo incluya en un enlace compartido.

## Ruta alternativa

Si Colab está bloqueado o no ofrece recursos, siga `docs/contingency_plan.md` y use
Jupyter local. Los recursos gratuitos de Colab no están garantizados y el acceso
con Workspace depende de la configuración del administrador.

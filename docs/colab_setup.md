# Configuración de Google Colab

## Decisión del curso

Colab es una ruta de ejecución, no un requisito pedagógico. El curso base:

- utiliza CPU;
- no necesita GPU ni TPU;
- no necesita una API generativa;
- no necesita montar Google Drive;
- puede ejecutarse localmente con Python 3.10 o posterior;
- **no depende de Colab ni de GitHub para funcionar**: el notebook del caso incluye
  el simulador y verifica la huella SHA-256 de los datos (véase más abajo).

## Cómo obtiene los datos el notebook

El notebook prueba tres fuentes por orden y solo acepta una si el SHA-256 del dataset
coincide con el registrado en `data/metadata.json`:

1. **Archivos locales** (`data/` o el directorio actual). En Colab aparece «no
   encontrado»: es normal.
2. **GitHub**, desde la etiqueta `v1.0.0` del repositorio público.
3. **Simulador integrado**: regenera exactamente los mismos datos, sin red.

Una sesión de Colab sin acceso a GitHub sigue funcionando. Un archivo alterado (por
ejemplo, guardado desde una hoja de cálculo) se descarta y se usa la fuente siguiente.

## Publicación (docente)

1. `python scripts/build_packs.py` genera `dist/student_pack/`.
2. Publique ese contenido en el repositorio público
   `SeRoMechatronic/2026_eu4m-ai-workshop-student`, rama `main`. Nunca publique este
   repositorio maestro: contiene soluciones y la clave del reto.
3. Cree la etiqueta `v1.0.0` en el repositorio público.
4. `python scripts/check_public_urls.py` confirma que los enlaces responden y que los
   datos descargados tienen la huella esperada.

## Enlaces para el alumnado

- Comprobación de acceso:
  <https://colab.research.google.com/github/SeRoMechatronic/2026_eu4m-ai-workshop-student/blob/main/notebooks/00_access_check.ipynb>
- Notebook del caso:
  <https://colab.research.google.com/github/SeRoMechatronic/2026_eu4m-ai-workshop-student/blob/main/notebooks/03_actuator_case_student.ipynb>

## Comprobación con cuentas EU4M

El docente debe realizar esta prueba al menos siete días antes, con una cuenta de
profesor y **dos cuentas ordinarias de estudiante**:

1. abrir la comprobación de acceso y ejecutar todo: debe aparecer `ACCESO_OK`;
2. confirmar que el administrador de Google Workspace permite el servicio;
3. abrir el notebook del caso y ejecutar todo;
4. comprobar que aparecen `SHA-256: faa229bd…` y `PASS El archivo cumple el contrato`;
5. anotar la fuente que usó el notebook (`GitHub (v1.0.0)` o `simulador integrado`);
6. cerrar la sesión, repetir con la segunda cuenta y registrar fecha y resultado.

| Fecha | Cuenta | Comprobación de acceso | Notebook del caso | Fuente de datos |
|---|---|---|---|---|
| | | | | |
| | | | | |

## Repositorio privado o sin publicar

Colab no puede leer un repositorio privado sin un token, y **no debe introducirse un
token de GitHub en una celda ni en un enlace compartido**. Si aún no ha publicado el
repositorio, descargue el notebook y ábralo en Colab con *Archivo → Subir cuaderno*.
No hace falta subir datos: el simulador integrado los regenera y verifica.

## Ruta alternativa

Si Colab está bloqueado o no ofrece recursos, siga `docs/contingency_plan.md` y use
Jupyter local. Los recursos gratuitos de Colab no están garantizados y el acceso
con Workspace depende de la configuración del administrador.

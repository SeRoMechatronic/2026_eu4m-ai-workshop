# Lista de comprobación para impartir o publicar

## Al modificar materiales

- [ ] `python scripts/run_all.py` termina con código 0.
- [ ] El workflow de GitHub Actions está en verde en Linux y en Windows.
- [ ] Si cambió una diapositiva, `python scripts/build_agenda.py` y la prueba de agenda pasan.
- [ ] Si cambió el simulador o el reto, se regeneraron datos, casos y soluciones.

## Siete días antes

- [ ] Confirmar fecha, aula, número de estudiantes y carácter evaluable.
- [ ] Revisar la política institucional de IA y datos.
- [ ] `python scripts/build_packs.py --offline --zip` sin errores.
- [ ] Publicar `dist/student_pack/` en el repositorio público y crear la etiqueta `v1.0.0`.
- [ ] `python scripts/check_public_urls.py` termina con código 0.
- [ ] Probar Colab con una cuenta de profesor y dos cuentas EU4M ordinarias
      (tabla de [colab_setup.md](colab_setup.md)).
- [ ] Ejecutar `python scripts/run_all.py` en un entorno limpio del portátil de clase.
- [ ] Copiar `dist/instructor_kit/` a un USB y a la nube personal.

## Tres o cuatro días antes

- [ ] Enviar al alumnado el enlace del repositorio público y la comprobación de acceso.
- [ ] Recoger las líneas `ACCESO_OK` y resolver cuentas bloqueadas (trabajo por parejas).

## Un día antes

- [ ] Abrir las cuatro presentaciones y revisar las notas (o sus PDF).
- [ ] Abrir el notebook de estudiante y el resuelto en el portátil de clase, sin red.
- [ ] Comprobar los casos A, B y C de `handouts/` y guardar la clave fuera de la carpeta compartida.
- [ ] Preparar copias digitales o impresas de PVRD, matriz y prueba de salida.
- [ ] Guardar `instructor/prepared_ai_responses.md` para trabajo sin conexión.
- [ ] Probar el proyector y el adaptador con las diapositivas en PDF.

## Después

- [ ] Recoger evidencia individual antes de compartir soluciones.
- [ ] Registrar fallos de acceso y tiempos reales.
- [ ] Guardar solo los datos permitidos por la normativa institucional.
- [ ] Crear una versión o etiqueta nueva si se modifican materiales evaluables.
- [ ] Antes de reutilizar el reto, regenerar los casos con otra semilla privada.

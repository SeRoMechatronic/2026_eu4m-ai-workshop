# Respuestas preparadas para contingencias

Estas salidas son deliberadamente imperfectas. Se utilizan cuando no hay acceso a
un asistente de IA. No deben presentarse como hechos ni como soluciones.

## Módulo 1  Umbral universal

> La norma ISO 13374 establece que un error de posición superior a 0,05 m confirma
> una pérdida de eficacia del actuador. Este umbral puede aplicarse a cualquier
> sistema mecatrónico. DOI: 10.1234/actuator.2021.305.

Riesgos preparados: norma sin parte ni cláusula, universalidad, DOI no verificado,
confusión entre indicio y confirmación.

## Módulo 2  Bibliografía plausible

> Tres estudios de García et al. (2022), Müller y Chen (2023) y Smith (2024)
> demuestran que los LLM reducen un 40 % el tiempo de investigación sin afectar la
> precisión. Todos coinciden en recomendar el uso libre de citas generadas.

Riesgos preparados: referencias sin metadatos, cifra sin población o diseño,
generalización y recomendación que no se deriva de evidencia localizada.

## Módulo 3  Código que responde otra pregunta

```python
features = data.groupby("scenario").mean(numeric_only=True)
best = features["tracking_rmse_true_m"].idxmax()
print("Diagnóstico confirmado:", best)
```

Riesgos preparados: usa etiqueta y señal de validación, agrega antes de separar
ejecuciones, llama «diagnóstico» a una comparación descriptiva y no tiene tests.

## Módulo 4  Exceso de certeza

> El caso B confirma un sesgo de sensor de 0,12 m con una precisión del 95 % porque
> el error medido es pequeño. El sensor debe sustituirse inmediatamente.

Riesgos preparados: magnitud no observable con el archivo operativo, precisión
inventada, ausencia de hipótesis alternativas y recomendación sin prueba de
seguridad o calibración.


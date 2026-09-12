# Registro de procedencia y contraste

Última revisión: 12 de septiembre de 2026.

| Afirmación utilizada | Fuente primaria o registro | Comprobación | Uso permitido en el curso |
|---|---|---|---|
| La alfabetización en IA debe adaptarse al conocimiento, contexto y riesgo | Comisión Europea, AI Literacy Q&A | Página oficial revisada | Marco docente; no equivale a dictamen jurídico de la Universidad |
| La orientación educativa debe ser humana y proteger datos | UNESCO, *Guidance for generative AI in education and research* | Registro institucional y documento comprobados | Política y discusión ética |
| Conviene validar afirmaciones, comprobar citas y documentar límites | NIST AI 600-1, DOI `10.6028/NIST.AI.600-1` | DOI y PDF oficial comprobados | Fundamento de PVRD |
| Los sistemas de generación pueden producir contenido no respaldado | Ji et al., DOI `10.1145/3571730` | Metadatos de Crossref y resumen editorial comprobados | Riesgo general; no estima la tasa de error de una herramienta concreta |
| Los LLM presentan oportunidades y riesgos educativos | Kasneci et al., DOI `10.1016/j.lindif.2023.102274` | DOI y metadatos comprobados | Contexto educativo; no política institucional |
| La IA generativa cambia prácticas de educación en ingeniería | Qadir, DOI `10.1109/EDUCON54358.2023.10125121` | DOI y registro IEEE comprobados | Contexto de educación en ingeniería |
| Los residuos son un concepto central del diagnóstico basado en modelos | Isermann, DOI `10.1016/j.arcontrol.2004.12.002` | DOI, metadatos y alcance del artículo comprobados | Marco conceptual; no valida el actuador sintético |
| El diagnóstico basado en datos depende de datos y evaluación adecuados | Lei et al., DOI `10.1016/j.ymssp.2019.106587` | DOI, metadatos y alcance de la revisión comprobados | Contexto; no prueba el rendimiento del notebook |
| Workspace puede restringir Colab y los recursos gratuitos no son garantizados | Google Colab FAQ | Página oficial revisada | Justifica la ruta alternativa local |

## Evidencia propia del repositorio

- `src/eu4m_workshop/simulation.py` define el modelo, parámetros y semillas.
- `data/metadata.json` registra propósito, configuración y hashes SHA-256.
- `tests/` verifica reproducibilidad, cálculos, separación de respuestas y estructura docente.
- `results/scenario_summary.csv` contiene medianas descriptivas; no contiene una
  prueba de significancia ni una estimación de precisión diagnóstica.

## Regla de actualización

Antes de una nueva edición, comprobar enlaces oficiales, condiciones de las
herramientas y normativa institucional. No cambiar una conclusión técnica sin
actualizar su fuente, prueba o límite.


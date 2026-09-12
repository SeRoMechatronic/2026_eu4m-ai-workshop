#!/usr/bin/env python3
"""Build the student and instructor notebooks from reviewed source cells."""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import nbformat as nbf


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ROOT / "notebooks"


def markdown(text: str):
    return nbf.v4.new_markdown_cell(dedent(text).strip())


def code(text: str):
    return nbf.v4.new_code_cell(dedent(text).strip())


def base_cells():
    return [
        markdown(
            """
            # Caso del actuador lineal

            Este notebook utiliza datos sintéticos para practicar verificación de
            afirmaciones técnicas. El modelo no representa un actuador industrial
            específico y no valida un sistema real de diagnóstico.

            **Objetivos**

            - comprobar la procedencia y estructura de los datos;
            - comparar señales medidas y señales de validación;
            - decidir qué afirmaciones respaldan los resultados;
            - documentar límites y la siguiente prueba necesaria.
            """
        ),
        markdown(
            """
            ## 1  Carga reproducible

            La ruta local se utiliza en una copia del repositorio. Si el notebook se
            abre en Colab desde el repositorio público, se descarga el mismo CSV desde
            la rama `main`. No se solicita acceso a Google Drive.
            """
        ),
        code(
            """
            from pathlib import Path

            import matplotlib.pyplot as plt
            import numpy as np
            import pandas as pd

            REPOSITORY = "SeRoMechatronic/2026_eu4m-ai-workshop"
            PART_NAMES = [
                "actuator_signals_nominal.csv",
                "actuator_signals_actuator_loss.csv",
                "actuator_signals_sensor_bias.csv",
            ]
            # Jupyter ejecuta normalmente desde ``notebooks/``; Colab lo hace desde
            # el directorio de carga. Se prueban ambos casos antes de usar la red.
            DATA_DIRS = [Path("data"), Path("../data"), Path(".")]
            LOCAL_DATA = next(
                (folder / "actuator_signals.csv" for folder in DATA_DIRS
                 if (folder / "actuator_signals.csv").exists()),
                None,
            )
            LOCAL_PARTS = next(
                ([folder / name for name in PART_NAMES] for folder in DATA_DIRS
                 if all((folder / name).exists() for name in PART_NAMES)),
                None,
            )

            if LOCAL_DATA is not None:
                data = pd.read_csv(LOCAL_DATA)
                source = str(LOCAL_DATA)
            elif LOCAL_PARTS is not None:
                data = pd.concat([pd.read_csv(path) for path in LOCAL_PARTS], ignore_index=True)
                source = " + ".join(map(str, LOCAL_PARTS))
            else:
                base = f"https://raw.githubusercontent.com/{REPOSITORY}/main/data"
                urls = [f"{base}/{name}" for name in PART_NAMES]
                data = pd.concat([pd.read_csv(url) for url in urls], ignore_index=True)
                source = "rama main (3 partes)"
            print(f"Fuente: {source}")
            print(f"Filas: {len(data):,}")
            data.head()
            """
        ),
        markdown(
            """
            ## 2  Contrato del dataset

            Antes de interpretar una gráfica, compruebe que el archivo corresponde al
            experimento descrito: 24 ejecuciones, tres escenarios equilibrados, 400
            muestras por ejecución y periodo de 0,02 s.
            """
        ),
        code(
            """
            expected_columns = {
                "run_id", "scenario", "seed", "time_s", "reference_m",
                "position_measured_m", "velocity_measured_m_s", "force_command_n",
                "position_true_m", "velocity_true_m_s", "force_applied_n",
            }
            assert expected_columns.issubset(data.columns)
            assert data["run_id"].nunique() == 24
            assert data["scenario"].nunique() == 3
            assert data.groupby("scenario")["run_id"].nunique().eq(8).all()
            assert data.groupby("run_id").size().eq(400).all()
            assert not data.isna().any().any()
            print("PASS  El archivo cumple el contrato.")
            """
        ),
        markdown(
            """
            ## 3  Señales representativas

            Compare una ejecución de cada escenario. La posición medida representa lo
            que ve el controlador. La posición real es una señal de validación disponible
            únicamente porque el caso es simulado.
            """
        ),
        code(
            """
            colors = {
                "nominal": "#2A6F97",
                "actuator_loss": "#C14953",
                "sensor_bias": "#E09F3E",
            }
            fig, axes = plt.subplots(3, 1, figsize=(11, 8), sharex=True)
            for scenario, color in colors.items():
                run = data[data["run_id"] == f"{scenario}_00"]
                axes[0].plot(run["time_s"], run["position_measured_m"], label=scenario, color=color)
                axes[1].plot(run["time_s"], run["position_true_m"], label=scenario, color=color)
                axes[2].plot(run["time_s"], run["force_command_n"], label=scenario, color=color)
            ref = data[data["run_id"] == "nominal_00"]
            axes[0].plot(ref["time_s"], ref["reference_m"], "k--", label="reference")
            axes[1].plot(ref["time_s"], ref["reference_m"], "k--", label="reference")
            axes[0].set_ylabel("Posición medida [m]")
            axes[1].set_ylabel("Posición real [m]")
            axes[2].set_ylabel("Orden de fuerza [N]")
            axes[2].set_xlabel("Tiempo [s]")
            axes[0].legend(ncol=4, fontsize=8)
            for ax in axes:
                ax.grid(alpha=0.25)
            plt.tight_layout()
            plt.show()
            """
        ),
        markdown(
            """
            **Pregunta breve**

            En el escenario con sesgo, ¿por qué el error calculado con la posición
            medida puede parecer pequeño mientras la posición real está desplazada?
            Escriba su respuesta en el registro PVRD.
            """
        ),
        markdown(
            """
            ## 4  Características por ejecución

            Se ignora el primer segundo para reducir el peso de la condición inicial.
            Las características de posición real y residual sirven para validar la
            simulación. Un sistema real necesitaría una medición independiente o un
            modelo que produjera una referencia comparable.
            """
        ),
        code(
            """
            rows = []
            for run_id, run in data.groupby("run_id"):
                g = run[run["time_s"] >= 1.0]
                measured_error = g["reference_m"] - g["position_measured_m"]
                true_error = g["reference_m"] - g["position_true_m"]
                residual = g["position_measured_m"] - g["position_true_m"]
                rows.append({
                    "run_id": run_id,
                    "scenario": g["scenario"].iloc[0],
                    "tracking_rmse_measured_m": np.sqrt(np.mean(measured_error**2)),
                    "tracking_rmse_true_m": np.sqrt(np.mean(true_error**2)),
                    "mean_sensor_residual_m": residual.mean(),
                    "force_command_rms_n": np.sqrt(np.mean(g["force_command_n"]**2)),
                    "force_saturation_fraction": np.mean(np.abs(g["force_command_n"]) >= 11.999),
                })

            features = pd.DataFrame(rows).sort_values("run_id").reset_index(drop=True)
            summary = features.groupby("scenario").median(numeric_only=True)
            summary.round(4)
            """
        ),
        markdown(
            """
            ## 5  Tres afirmaciones propuestas por una IA

            1. «El escenario con mayor RMSE real mediano es el de pérdida del actuador».
            2. «El sesgo puede confirmarse usando solo las señales operativas del lazo».
            3. «Los resultados prueban que el método funcionará en cualquier actuador».

            Para cada afirmación, indique evidencia, decisión y límite. Utilice
            `aceptar`, `modificar` o `rechazar` como decisión.
            """
        ),
    ]


def student_notebook():
    nb = nbf.v4.new_notebook()
    nb["metadata"] = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.11"},
        "colab": {"name": "03_actuator_case_student.ipynb", "provenance": []},
    }
    nb["cells"] = base_cells() + [
        code(
            """
            audit = pd.DataFrame([
                {"claim": 1, "decision": "PENDIENTE", "evidence": "", "remaining_limit": ""},
                {"claim": 2, "decision": "PENDIENTE", "evidence": "", "remaining_limit": ""},
                {"claim": 3, "decision": "PENDIENTE", "evidence": "", "remaining_limit": ""},
            ])
            audit
            """
        ),
        markdown(
            """
            ## 6  Prueba independiente

            Elija una afirmación y escriba un `assert`, cálculo o gráfico que permita
            comprobarla. No utilice el nombre del escenario como única evidencia.
            """
        ),
        code(
            """
            # Ejemplo de estructura. Sustituya la condición por su propia verificación.
            observed_runs = features["run_id"].nunique()
            assert observed_runs == 24
            print("Prueba ejecutada. Documente qué afirmación comprueba.")
            """
        ),
        markdown(
            """
            ## 7  Evidencia final

            Copie la tabla de auditoría completada en su entrega. Incluya:

            - una afirmación aceptada;
            - una afirmación rechazada o modificada;
            - la prueba ejecutada;
            - una medición que faltaría en un sistema real;
            - la ubicación de su entrada PVRD.
            """
        ),
    ]
    return nb


def solution_notebook():
    nb = nbf.v4.new_notebook()
    nb["metadata"] = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.11"},
    }
    nb["cells"] = base_cells() + [
        code(
            """
            audit = pd.DataFrame([
                {
                    "claim": 1,
                    "decision": "aceptar",
                    "evidence": "summary['tracking_rmse_true_m']; máximo mediano por escenario",
                    "remaining_limit": "Resultado del modelo sintético y de esta configuración",
                },
                {
                    "claim": 2,
                    "decision": "rechazar",
                    "evidence": "El residual usa position_true_m, señal no operativa",
                    "remaining_limit": "Hace falta sensor redundante, referencia externa o modelo validado",
                },
                {
                    "claim": 3,
                    "decision": "rechazar",
                    "evidence": "Solo 24 ejecuciones simuladas de un modelo didáctico",
                    "remaining_limit": "No hay validación con otros actuadores, cargas o datos reales",
                },
            ])
            audit
            """
        ),
        markdown(
            """
            ## 6  Pruebas de las decisiones

            La primera prueba confirma una propiedad limitada al dataset. La segunda
            muestra que la señal necesaria para confirmar el sesgo pertenece a la
            validación de la simulación.
            """
        ),
        code(
            """
            largest = summary["tracking_rmse_true_m"].idxmax()
            assert largest == "actuator_loss"

            operational_columns = {
                "time_s", "reference_m", "position_measured_m",
                "velocity_measured_m_s", "force_command_n",
            }
            validation_only = {"position_true_m", "velocity_true_m_s", "force_applied_n"}
            assert operational_columns.issubset(data.columns)
            assert validation_only.issubset(data.columns)
            print("PASS  Las pruebas respaldan las decisiones documentadas.")
            """
        ),
        markdown(
            """
            ## 7  Interpretación orientativa

            La pérdida del actuador aumenta el error real en esta configuración. El
            sesgo del sensor resulta visible al comparar medida y posición real, pero
            esa comparación no estaría disponible con un único sensor real. La
            conclusión responsable propone una medición independiente y evita
            generalizar desde un caso sintético.
            """
        ),
    ]
    return nb


def assign_stable_cell_ids(notebook, prefix: str) -> None:
    """Avoid noisy notebook diffs when materials are rebuilt."""
    for index, cell in enumerate(notebook["cells"], start=1):
        cell["id"] = f"{prefix}-{index:02d}"


def main() -> None:
    NOTEBOOKS.mkdir(exist_ok=True)
    for name, prefix, notebook in (
        ("03_actuator_case_student.ipynb", "student", student_notebook()),
        ("03_actuator_case_solution.ipynb", "solution", solution_notebook()),
    ):
        assign_stable_cell_ids(notebook, prefix)
        nbf.write(notebook, NOTEBOOKS / name)
        print(NOTEBOOKS / name)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build the student, solution and access-check notebooks from reviewed cells.

The notebooks are self-contained: the simulator is copied verbatim from
``src/eu4m_workshop/simulation.py`` and the dataset is verified against the
SHA-256 recorded in ``data/metadata.json`` whichever source provides it.
"""

from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent

import nbformat as nbf

from course_config import DATA_REF, PUBLIC_REPOSITORY


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ROOT / "notebooks"
SIMULATION_SOURCE = ROOT / "src" / "eu4m_workshop" / "simulation.py"
METADATA = ROOT / "data" / "metadata.json"

SIMULATOR_HEADER = '#@title Simulador de referencia (no hace falta modificarlo) { display-mode: "form" }\n'
HIDDEN_CELL = {
    "cellView": "form",
    "jupyter": {"source_hidden": True},
}


def markdown(text: str):
    return nbf.v4.new_markdown_cell(dedent(text).strip())


def code(text: str, metadata: dict | None = None):
    cell = nbf.v4.new_code_cell(dedent(text).strip())
    if metadata:
        cell["metadata"].update(metadata)
    return cell


def expected_sha256() -> str:
    return json.loads(METADATA.read_text(encoding="utf-8"))["sha256"]["combined_dataset"]


def simulator_cell():
    """Embed the reviewed simulator so the notebook never depends on the network."""
    source = SIMULATION_SOURCE.read_text(encoding="utf-8").strip()
    return code(SIMULATOR_HEADER + source, HIDDEN_CELL)


def loader_cell():
    template = """
        import hashlib
        import io
        import urllib.request
        from pathlib import Path

        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd

        REPOSITORY = "@@REPOSITORY@@"
        DATA_REF = "@@DATA_REF@@"
        EXPECTED_SHA256 = "@@SHA256@@"
        PART_NAMES = [
            "actuator_signals_nominal.csv",
            "actuator_signals_actuator_loss.csv",
            "actuator_signals_sensor_bias.csv",
        ]


        def canonical_sha256(df):
            \"\"\"SHA-256 del CSV canónico: finales de línea LF y ocho decimales.\"\"\"
            text = df.to_csv(index=False, float_format="%.8f", lineterminator="\\n")
            return hashlib.sha256(text.encode("utf-8")).hexdigest()


        def from_local_files():
            # Jupyter suele ejecutar desde notebooks/; Colab, desde el directorio de carga.
            for folder in (Path("data"), Path("../data"), Path(".")):
                paths = [folder / name for name in PART_NAMES]
                if all(path.exists() for path in paths):
                    return pd.concat([pd.read_csv(path) for path in paths], ignore_index=True)
            return None


        def from_github():
            base = f"https://raw.githubusercontent.com/{REPOSITORY}/{DATA_REF}/data"
            frames = []
            for name in PART_NAMES:
                with urllib.request.urlopen(f"{base}/{name}", timeout=10) as response:
                    frames.append(pd.read_csv(io.BytesIO(response.read())))
            return pd.concat(frames, ignore_index=True)


        SOURCES = [
            ("archivos locales", from_local_files),
            (f"GitHub ({DATA_REF})", from_github),
            ("simulador integrado", simulate_dataset),
        ]

        data = None
        for source, loader in SOURCES:
            try:
                candidate = loader()
            except Exception as error:
                print(f"- {source}: no disponible ({type(error).__name__})")
                continue
            if candidate is None:
                print(f"- {source}: no encontrado")
            elif canonical_sha256(candidate) != EXPECTED_SHA256:
                print(f"- {source}: la huella SHA-256 no coincide; se descarta")
            else:
                data = candidate
                break

        assert data is not None, "Ninguna fuente produjo el dataset esperado."
        print(f"Fuente: {source}")
        print(f"Filas: {len(data):,}")
        data.head()
    """
    text = (
        dedent(template)
        .replace("@@REPOSITORY@@", PUBLIC_REPOSITORY)
        .replace("@@DATA_REF@@", DATA_REF)
        .replace("@@SHA256@@", expected_sha256())
    )
    return code(text)


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

            El notebook busca los datos en tres lugares, por orden, y **solo acepta
            una fuente si su huella SHA-256 coincide con la registrada en
            `data/metadata.json`**:

            1. archivos locales (una copia del repositorio);
            2. GitHub, desde la etiqueta fijada del repositorio público;
            3. el simulador integrado, que regenera exactamente los mismos datos.

            Ver «no encontrado» en la primera fuente es normal en Colab. No se solicita
            acceso a Google Drive. La celda del simulador aparece plegada; puede
            abrirla para leer el modelo completo.
            """
        ),
        simulator_cell(),
        loader_cell(),
        markdown(
            """
            ## 2  Contrato del dataset

            Antes de interpretar una gráfica, compruebe que el archivo corresponde al
            experimento descrito: 24 ejecuciones, tres escenarios equilibrados, 400
            muestras por ejecución y periodo de 0,02 s. La huella SHA-256 confirma que
            los valores son exactamente los del experimento de referencia.
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
            assert canonical_sha256(data) == EXPECTED_SHA256
            print(f"SHA-256: {canonical_sha256(data)}")
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
                    "remaining_limit": (
                        "Resultado del modelo sintético y de esta configuración. La diferencia con "
                        "sensor_bias es menor que la dispersión entre ejecuciones; solo la "
                        "diferencia con nominal es robusta"
                    ),
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

            La primera prueba confirma una propiedad limitada al dataset y muestra hasta
            dónde llega: la pérdida del actuador supera siempre al nominal, pero sus
            rangos se solapan con los del sesgo del sensor. La segunda muestra que la
            señal necesaria para confirmar el sesgo pertenece a la validación de la
            simulación.
            """
        ),
        code(
            """
            largest = summary["tracking_rmse_true_m"].idxmax()
            assert largest == "actuator_loss"

            by_scenario = {
                s: features.loc[features["scenario"] == s, "tracking_rmse_true_m"]
                for s in ("nominal", "actuator_loss", "sensor_bias")
            }
            # Separación robusta frente al nominal...
            assert by_scenario["actuator_loss"].min() > by_scenario["nominal"].max()
            # ...pero sin separación frente a sensor_bias: los rangos se solapan.
            assert by_scenario["actuator_loss"].min() < by_scenario["sensor_bias"].max()

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

            La pérdida del actuador aumenta el error real en esta configuración, sin
            ambigüedad frente al escenario nominal. Frente al sesgo del sensor la
            diferencia es demasiado pequeña para sostener un orden fiable. El sesgo
            resulta visible al comparar medida y posición real, pero esa comparación
            no estaría disponible con un único sensor real. La conclusión responsable
            propone una medición independiente y evita generalizar desde un caso
            sintético.
            """
        ),
    ]
    return nb


def access_check_notebook():
    nb = nbf.v4.new_notebook()
    nb["metadata"] = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.11"},
        "colab": {"name": "00_access_check.ipynb", "provenance": []},
    }
    url = f"https://raw.githubusercontent.com/{PUBLIC_REPOSITORY}/{DATA_REF}/data/metadata.json"
    nb["cells"] = [
        markdown(
            """
            # Comprobación de acceso

            Esta prueba dura dos minutos. Compruebe que puede abrir el notebook, ejecutar
            código y dibujar una gráfica **antes** de la primera sesión.

            1. Menú **Entorno de ejecución → Ejecutar todo** (en Jupyter: *Run All*).
            2. Espere a que termine la última celda.
            3. Envíe al docente la línea que empieza por `ACCESO_OK`.

            Si aparece un error, envíe una captura de pantalla. No instale nada ni
            cambie la configuración por su cuenta.
            """
        ),
        code(
            """
            import platform
            import urllib.request

            import matplotlib
            import matplotlib.pyplot as plt
            import numpy as np
            import pandas as pd

            fig, ax = plt.subplots(figsize=(4, 2))
            ax.plot(np.arange(6) ** 2, marker="o")
            ax.set_title("Gráfica de prueba")
            plt.show()
            """
        ),
        code(
            f"""
            try:
                urllib.request.urlopen("{url}", timeout=10).close()
                github = "sí"
            except Exception:
                github = "no"

            print(
                "ACCESO_OK"
                f" | Python {{platform.python_version()}}"
                f" | numpy {{np.__version__}}"
                f" | pandas {{pd.__version__}}"
                f" | matplotlib {{matplotlib.__version__}}"
                f" | GitHub: {{github}}"
            )
            if github == "no":
                print(
                    "Aviso: no hay acceso a GitHub desde este entorno. El notebook del "
                    "curso funcionará igualmente con el simulador integrado."
                )
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
        ("00_access_check.ipynb", "access", access_check_notebook()),
        ("03_actuator_case_student.ipynb", "student", student_notebook()),
        ("03_actuator_case_solution.ipynb", "solution", solution_notebook()),
    ):
        assign_stable_cell_ids(notebook, prefix)
        path = NOTEBOOKS / name
        # Escribir bytes evita que Windows convierta LF en CRLF.
        path.write_bytes(nbf.writes(notebook).encode("utf-8") + b"\n")
        print(path)


if __name__ == "__main__":
    main()

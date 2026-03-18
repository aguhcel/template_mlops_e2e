**Título:** Plan para convertir el repo en un template OSS E2E ML/GenAI (Cookiecutter)

**Resumen**
- Transformar el repo en un template Cookiecutter “baterías incluidas” para E2E ML/GenAI con tracking, versionado de datos, orquestación y API de inferencia, apuntando a Python 3.11 y licencia Apache-2.0.

**Cambios clave**
1. **Estructura y scaffolding**
- Convertir a plantilla Cookiecutter con `cookiecutter.json` y carpeta `{{cookiecutter.project_slug}}/`.
- Generar paquete real en `src/{{cookiecutter.package_name}}/` con módulos base: `data/`, `features/`, `models/`, `pipelines/`, `serving/`, `utils/`.
- Añadir `README` templado, `LICENSE` Apache-2.0, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`.

2. **MLOps completo (MLflow + DVC + Prefect)**
- DVC: agregar `dvc.yaml` con etapas mínimas `data_prepare`, `train`, `evaluate`, `register`.
- MLflow: configurar tracking local por defecto y registrar modelos; ejemplo de entrenamiento e inferencia usando un modelo simple.
- Prefect: flujo `pipeline_flow.py` que orqueste las etapas DVC/MLflow y permita ejecución local.

3. **API y serving**
- FastAPI con rutas `/health` y `/predict`, modelo cargado desde el último artefacto registrado en MLflow (fallback local).
- Configuración via `pydantic-settings` y `.env` de ejemplo.

4. **Calidad, pruebas y DX**
- Separar dependencias runtime y dev en `pyproject.toml` (`[project.optional-dependencies].dev`).
- Agregar `ruff` (lint/format) y `pytest` + `pytest-cov` en dev deps.
- `Makefile` con targets: `install`, `lint`, `format`, `test`, `serve`, `train`, `pipeline`, `dvc-pull`.

5. **CI/CD**
- GitHub Actions con jobs de `lint` y `test` para PRs.
- Opcional: job manual para `pipeline` sin credenciales externas.

**Cambios en interfaces públicas**
- API FastAPI: endpoints públicos `/health` y `/predict`.
- Comandos de usuario: `make serve`, `make train`, `make pipeline`.
- Archivos clave públicos en template: `dvc.yaml`, `mlflow` config local, `prefect` flow.

**Plan de pruebas**
1. `make lint` y `make test`.
2. `make serve` y request a `/health` y `/predict`.
3. `make train` y validación de registro de modelo en MLflow local.
4. `make pipeline` para ejecución E2E local.

**Supuestos**
- Python objetivo 3.11.
- Stack MLOps: MLflow + DVC + Prefect.
- Licencia Apache-2.0.
- CI/CD en GitHub Actions.

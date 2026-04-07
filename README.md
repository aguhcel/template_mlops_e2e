# Template_MLOps_E2E

This repository is for creating a template for ML/Gen AI projects end-to-end.

## Requirements
- Python 3.x

## How to create virtual enviroment with uv
### Install uv
```
 pip install --upgrade pip
 pip install uv
```

### Install specific python version
```
 uv python install 3.x
```

### Create a virtual enviroment with uv
```
 uv venv -p 3.x <ENV_NAME>
```

### Activate virtual enviroment
```
 source <ENV_NAME>/bin/activate
```

## How to initialize the project
### Install dependencies
```
 make install
```

### Test project
```
 make test
```

### Run pre-commit checks
```
 make run-pre-commit
```

This repository includes a pre-commit hook that validates stages after try to make a push.

### Run API
```
uvicorn app.api.router.v0.main:app --reload --port <0-65536>
```
 **OR**
```
make run-app
```

### DVC (example data)
```
make init-dvc-local DVC_REMOTE_PATH=/absolute/path/to/dvc_remote_local
make dvc-track-example
```

### Directory structure
```
Template_MLOps_E2E/
├── LICENSE     
├── README.md                  
├── Makefile                     # Makefile with commands like `make install` or `make test`     
├── .python-version              # Python version use for this template
├── pyproject.toml               # Toml file with dependencies in this template
├── uv.lock                      # Lock file containing the source of the dependencies used in this template
│
├── app                          # FastAPI bootstrap (includes routers)
│   └── api                      # Contains the app
│      └── router                # App entrypoints
│          └── v0                # Version of the app
│
├── configs                      # Config files (models and training hyperparameters)
│   └── model1_config.yaml              
│
├── data                         # Directory to save the data
│   ├── bronze                   # Original from source
│   ├── silver                   # Filter/transformed data.
│   └── gold                     # The final, canonical data sets for modeling.
│
├── docs                         # Project documentation.
│
├── models                       # Trained and serialized models.
│
├── notebooks                    # Jupyter notebooks.
│
├── references                   # Data dictionaries, manuals, and all other explanatory materials.
│
├── reports                      # Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures                  # Generated graphics and figures to be used in reporting.
│
├── src                          # Source code for use in this project.
│   └── template_mlops_e2e       # Makes src a Python module.
│       ├── api                  # MVC (Controllers + Views)
│       │   ├── controllers       # FastAPI routers (Controllers)
│       │   └── views             # Pydantic schemas (Views)
│       ├── data                 # ETL / preprocessing code
│       ├── features             # Feature engineering
│       ├── models               # ML logic (Models)
│       └── pipelines            # Orchestration local/prefect
│       
└── tests                        # Test code for Units Test in this project.
    └── __init__.py              # Makes test a Python module.
```

## TODO
* Add: dockerfile
  
* Add: more commands for makefile

* Add: More steps for CI/CD
    * Fix: Issues in CI/CD

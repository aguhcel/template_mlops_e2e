# Template_MLOps_E2E

The following repository, is for create a template for ML/Gen AI proyects E2E

##  Requirements 
 - Python 3.X

## How to init the project
### Install depedencies
```
 make install
```

### Test project
```
 make test
```

### Run API
```
uvicorn app.api.router.v0.main:app --reload --port <0-65536>
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
├── app                          # Directory to expose the app to other services
│   └── api                      # Cointains the app
│      └── router                # Routers to expose ML/GEN AI systems
│          ├── healthcheck       # Healthcheck router
│          │   └── model         # Response model for healthcheck
│          └── v0                # Version of the app
│
├── configs                      # Config files (models and training hyperparameters)
│   └── model1_config.yaml              
│
├── data                         # Directory from save the data
│   ├── bronce                   # Original from source
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
├── requirements.txt             # The requirements file for reproducing the analysis environment.
├── src                          # Source code for use in this project.
│   └── __init__.py              # Makes src a Python module.
│
└── test                         # Test code for Units Test in this project.
    └── __init__.py              # Makes test a Python module.
```

## TODO
* Fix: test/coverage command for all repository

* Add: Subdirectories for pattern VCM (Model, View, Controller)

* Add: dockerfile
* Add: more commads for makefile
    * run uvicorn

* Add: More steps for CI/CD
    * Fix: Issues in CI/CD
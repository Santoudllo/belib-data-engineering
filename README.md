# belib-data-engineering
Pipeline de données complet pour collecter, traiter et visualiser les données des points de recharge pour véhicules électriques de l'API Belib'. Utilisez Airflow, Kafka, Spark et des outils de visualisation pour une analyse approfondie des données. Automatisez les workflows avec GitHub Actions pour un développement et un déploiement efficaces.


## workflow



## arborescence du pepeline 
```
belib-pipeline/
├── conf/
│   ├── base/
│   ├── local/
│   ├── logging.yml
├── data/
│   ├── 01_raw/
│   │   ├── belib_data.csv
│   ├── 02_intermediate/
│   ├── 03_primary/
│   ├── 04_feature/
│   ├── 05_model_input/
│   ├── 06_models/
│   ├── 07_model_output/
│   ├── 08_reporting/
│   ├── 09_tracking/
├── docs/
├── notebooks/
├── src/
│   ├── belib_pipeline/
│   │   ├── __init__.py
│   │   ├── __main__.py
│   │   ├── nodes.py
│   │   ├── pipeline_registry.py
│   │   ├── pipelines/
│   │   │   ├── data_processing/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── nodes.py
│   │   │   │   ├── pipeline.py
│   │   │   ├── data_science/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── nodes.py
│   │   │   │   ├── pipeline.py
│   │   │   ├── reporting/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── nodes.py
│   │   │   │   ├── pipeline.py
│   ├── settings.py
├── tests/
├── .gitignore
├── pyproject.toml
├── README.md
├── requirements.txt


```
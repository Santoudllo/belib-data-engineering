# belib-data-engineering
Pipeline de données complet pour collecter, traiter et visualiser les données des points de recharge pour véhicules électriques de l'API Belib'. Utilisez Airflow, Kafka, Spark et des outils de visualisation pour une analyse approfondie des données. Automatisez les workflows avec GitHub Actions pour un développement et un déploiement efficaces.


## workflow



## arborescence du pepeline 
```
Belib-workflo/
├── conf/
│   ├── base/
│   │   ├── catalog.yml
│   │   ├── logging.yml
│   │   └── parameters.yml
│   └── local/
├── data/
│   ├── 01_raw/
│   ├── 02_intermediate/
│   ├── 03_primary/
│   ├── 04_feature/
│   ├── 05_model_input/
│   ├── 06_models/
│   └── 09_reporting/
├── src/
│   └── Belib_workflo/
│       ├── __init__.py
│       ├── nodes.py
│       ├── pipelines.py
│       ├── settings.py
│       └── datasets/
│           ├── __init__.py
│           └── json_dict_dataset.py
└── README.md


```
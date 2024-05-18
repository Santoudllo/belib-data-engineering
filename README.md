# belib-data-engineering
Pipeline de données complet pour collecter, traiter et visualiser les données des points de recharge pour véhicules électriques de l'API Belib'. Utilisez Airflow, Kafka, Spark et des outils de visualisation pour une analyse approfondie des données. Automatisez les workflows avec GitHub Actions pour un développement et un déploiement efficaces.


## workflow



## arborescence du répertoire du pepeline 
```
my_project/
|-- conf/
|   |-- base/
|   |   |-- catalog.yml
|   |   |-- logging.yml
|   |-- local/
|       |-- credentials.yml
|-- data/
|   |-- 01_raw/
|   |   |-- belib_data.csv
|   |-- 02_intermediate/
|   |-- 03_primary/
|   |-- 04_features/
|   |-- 05_model_input/
|   |-- 06_models/
|   |-- 07_model_output/
|   |-- 08_reporting/
|   |-- 09_tracking/
|-- notebooks/
|-- src/
|   |-- my_project/
|       |-- nodes/
|           |-- preprocess.py
|           |-- train_model.py
|           |-- track_metrics.py
|           |-- generate_reports.py
|       |-- pipelines/
|           |-- data_engineering.py
|           |-- machine_learning.py
|           |-- reporting.py
|       |-- run.py
```
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from pymongo import MongoClient
from urllib.parse import quote_plus
from kafka import KafkaConsumer
import json

# Fonction pour récupérer les données de Kafka et les charger dans MongoDB
def kafka_to_mongodb():
    username = 'santoudllo'
    password = '@Santou20'
    dbname = 'belib_database'
    collection_name = 'belib.collection'
    mongodb_uri = f"mongodb+srv://{quote_plus(username)}:{quote_plus(password)}@bike.kvgkgvj.mongodb.net/{dbname}?retryWrites=true&w=majority"
    
    kafka_topic = "belib_data_topic"
    bootstrap_servers = 'localhost:9092'
    
    # Connexion à Kafka
    consumer = KafkaConsumer(kafka_topic, bootstrap_servers=bootstrap_servers, auto_offset_reset='earliest', group_id='belib_group')
    
    data = []
    for message in consumer:
        data.append(json.loads(message.value.decode('utf-8')))
    
    # Connexion à MongoDB et insertion des données
    if data:
        client = MongoClient(mongodb_uri)
        db = client[dbname]
        collection = db[collection_name]
        collection.insert_many(data)
        print("Data fetched successfully from Kafka and saved to MongoDB.")
    else:
        print("No data fetched from Kafka.")

# Paramètres du DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 5, 15),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Création du DAG
dag = DAG(
    'kafka_to_mongodb',
    default_args=default_args,
    description='Récupère les données de Kafka et les charge dans MongoDB toutes les heures.',
    schedule_interval=timedelta(hours=1),
)

# Création de l'opérateur Python
kafka_to_mongodb_operator = PythonOperator(
    task_id='kafka_to_mongodb_task',
    python_callable=kafka_to_mongodb,
    dag=dag,
)

# Définition des dépendances entre les tâches
kafka_to_mongodb_operator

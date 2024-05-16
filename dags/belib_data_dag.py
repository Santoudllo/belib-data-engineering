from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from kafka import KafkaProducer
import json
import requests

# Définition des paramètres de la DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 5, 15),  # Date de début de la DAG
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Définition de la DAG
dag = DAG(
    'belib_data_pipeline',
    default_args=default_args,
    description='DAG pour récupérer les données Belib et les envoyer à Kafka',
    schedule_interval='@hourly',  # Exécution toutes les heures
)

# Classe pour récupérer les données de l'API Belib' et les envoyer à Kafka
class BelibAPIClient:
    def __init__(self, api_url, kafka_topic, bootstrap_servers):
        self.api_url = api_url
        self.kafka_topic = kafka_topic
        self.bootstrap_servers = bootstrap_servers
        self.producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    def fetch_data(self, limit=20):
        try:
            response = requests.get(self.api_url, params={'limit': limit})
            if response.status_code == 200:
                data = response.json()
                self.producer.send(self.kafka_topic, value=data)
                return data
            else:
                print(f"Failed to fetch data. Status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

# Fonction pour exécuter la récupération des données et l'envoi à Kafka
def fetch_and_send_to_kafka():
    api_url = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/belib-points-de-recharge-pour-vehicules-electriques-disponibilite-temps-reel/records"
    kafka_topic = "belib_data_topic"
    bootstrap_servers = 'localhost:9092'
    client = BelibAPIClient(api_url, kafka_topic, bootstrap_servers)
    client.fetch_data()

# Créez un opérateur Python pour exécuter la fonction
fetch_and_send_task = PythonOperator(
    task_id='fetch_and_send_to_kafka',
    python_callable=fetch_and_send_to_kafka,
    dag=dag,
)

# Définir les dépendances des tâches
fetch_and_send_task

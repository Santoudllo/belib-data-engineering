import requests
from dotenv import load_dotenv
import os
from kafka import KafkaProducer
import json

class BelibAPIClient:
    def __init__(self, api_url):
        self.api_url = api_url

    def fetch_data(self, limit=20):
        try:
            print(f"Récupération des données depuis l'API : {self.api_url} avec une limite : {limit}")
            response = requests.get(self.api_url, params={'limit': limit})
            print(f"Code de statut de la réponse : {response.status_code}")
            print(f"Contenu de la réponse : {response.text}")

            if response.status_code == 200:
                json_data = response.json()
                total_records = json_data.get('total_count', None)
                records = json_data.get('results', [])
                return records, total_records
            else:
                print(f"Échec de la récupération des données. Code de statut : {response.status_code}, Réponse : {response.text}")
                return None, None
        except Exception as e:
            print(f"Une erreur s'est produite lors de la récupération des données de l'API : {e}")
            return None, None

class KafkaPipeline:
    def __init__(self, kafka_bootstrap_server):
        # Créer un producteur Kafka
        self.producer = KafkaProducer(bootstrap_servers=kafka_bootstrap_server,
                                       value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    def send_data_to_kafka(self, topic, data):
        try:
            if data:
                for record in data:
                    self.producer.send(topic, record)
                self.producer.flush()
                print(f"{len(data)} documents envoyés au topic Kafka : {topic}.")
            else:
                print("Aucune donnée à envoyer.")
        except Exception as e:
            print(f"Erreur lors de l'envoi des données vers Kafka : {e}")

    def close_connection(self):
        self.producer.close()
        print("Connexion au producteur Kafka fermée.")

def main():
    load_dotenv()

    # Récupérer l'URL de l'API et le serveur Kafka depuis le fichier .env
    api_url = os.getenv("API_URL")
    kafka_bootstrap_server = os.getenv("KAFKA_BOOTSTRAP_SERVER", "localhost:9092")  # Défaut à localhost:9092
    
    if not api_url:
        print("L'API_URL n'est pas définie dans le fichier .env.")
        return

    # Créer une instance du client API
    api_client = BelibAPIClient(api_url)

    # Récupérer les données depuis l'API
    data, total_records = api_client.fetch_data(limit=50)
    if data:
        print(f"{len(data)} enregistrements récupérés avec succès depuis l'API.")
        if total_records is not None:
            print(f"Total des enregistrements dans l'API : {total_records}")
        else:
            print("Le nombre total d'enregistrements n'est pas disponible.")

        # Initialiser le pipeline Kafka
        kafka_pipeline = KafkaPipeline(kafka_bootstrap_server)

        # Envoyer les données au topic Kafka
        kafka_pipeline.send_data_to_kafka('input-topic', data)

        # Fermer la connexion au producteur Kafka
        kafka_pipeline.close_connection()
    else:
        print("Échec de la récupération des données depuis l'API.")

if __name__ == "__main__":
    main()

import os
import json
import requests
from kafka import KafkaProducer
from dotenv import load_dotenv

class APIToKafka:
    def __init__(self, api_url):
        self.api_url = api_url
        self.producer = KafkaProducer(
            bootstrap_servers='localhost:9092',
            value_serializer=lambda x: json.dumps(x).encode('utf-8')  # Sérialisation des données en JSON
        )

    def fetch_and_send_data(self, limit=50):
        try:
            print(f"Récupération des données depuis l'API : {self.api_url} avec une limite : {limit}")
            response = requests.get(self.api_url, params={'limit': limit})
            if response.status_code == 200:
                data = response.json().get('results', [])
                print(f"{len(data)} enregistrements récupérés depuis l'API.")

                for record in data:
                    self.producer.send('input-topic', value=record)
                    print(f"Envoi du message au topic Kafka : {record}")

                self.producer.flush()
                print("Tous les messages ont été envoyés à Kafka.")
            else:
                print(f"Erreur lors de la récupération des données : {response.status_code}")
        except Exception as e:
            print(f"Erreur : {e}")
        finally:
            self.producer.close()
            print("Connexion au producteur Kafka fermée.")

if __name__ == "__main__":
    load_dotenv()
    api_url = os.getenv("API_URL")
    if not api_url:
        print("L'API_URL n'est pas définie dans le fichier .env.")
    else:
        api_to_kafka = APIToKafka(api_url)
        api_to_kafka.fetch_and_send_data()

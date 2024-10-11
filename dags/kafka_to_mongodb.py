import os
import json
from dotenv import load_dotenv
from kafka import KafkaConsumer
from pymongo import MongoClient

class MongoDBPipeline:
    def __init__(self):
        load_dotenv()
        self.mongodb_uri = os.getenv('MONGO_URI')
        self.dbname = os.getenv('MONGO_DBNAME')

        # Initialiser la connexion à MongoDB
        self.client = MongoClient(self.mongodb_uri)
        self.db = self.client[self.dbname]
        self.collection = self.db['belib']  # Nom de la collection

    def insert_data_to_mongodb(self, data):
        try:
            if data:
                # Insérer les données dans MongoDB
                result = self.collection.insert_many(data)
                print(f"{len(result.inserted_ids)} documents insérés dans MongoDB.")
            else:
                print("Aucune donnée à insérer.")
        except Exception as e:
            print(f"Erreur lors de l'insertion des données dans MongoDB : {e}")

    def close_connection(self):
        self.client.close()
        print("Connexion à MongoDB fermée.")

def is_valid_json(message):
    try:
        json.loads(message)
        return True
    except json.JSONDecodeError:
        return False

def consume_kafka_messages():
    load_dotenv()
    consumer = KafkaConsumer(
        'input-topic',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group',
        value_deserializer=lambda x: x.decode('utf-8')  # Désérialisation en chaîne
    )

    mongo_pipeline = MongoDBPipeline()

    for message in consumer:
        raw_message = message.value
        print(f"Message brut reçu : {raw_message}")

        if is_valid_json(raw_message):
            data = json.loads(raw_message)  # Désérialisation des données
            mongo_pipeline.insert_data_to_mongodb([data])  
        else:
            print(f"Message non valide (non JSON) reçu : {raw_message}")

    mongo_pipeline.close_connection()

if __name__ == "__main__":
    consume_kafka_messages()

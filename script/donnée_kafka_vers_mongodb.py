import pymongo
from pymongo import MongoClient
from urllib.parse import quote_plus
from kafka import KafkaConsumer
import json

class BikeDataPipeline:
    def __init__(self):
        self.username = 'santoudllo'
        self.password = '*******'
        self.dbname = 'belib_database'
        self.collection_name = 'belib.collection'
        self.mongodb_uri = f"mongodb+srv://{quote_plus(self.username)}:{quote_plus(self.password)}@bike.kvgkgvj.mongodb.net/{self.dbname}?retryWrites=true&w=majority"

    def fetch_data_from_kafka(self):
        kafka_topic = "belib_data_topic"
        bootstrap_servers = 'localhost:9092'
        
        consumer = KafkaConsumer(kafka_topic, bootstrap_servers=bootstrap_servers, auto_offset_reset='earliest', group_id='belib_group')
        data = []

        for message in consumer:
            data.append(json.loads(message.value.decode('utf-8')))
        
        return data

    def load_data_to_mongodb(self, data):
        if data:
            client = MongoClient(self.mongodb_uri)
            db = client[self.dbname]
            collection = db[self.collection_name]
            collection.insert_many(data)
            print("Data fetched successfully from Kafka and saved to MongoDB.")
            return True
        else:
            print("Failed to fetch data from Kafka.")
            return False

# Création de l'instance de la pipeline
pipeline = BikeDataPipeline()

# Récupération des données depuis Kafka
data = pipeline.fetch_data_from_kafka()

# Chargement des données dans MongoDB
if data:
    pipeline.load_data_to_mongodb(data)
else:
    print("No data fetched from Kafka.")

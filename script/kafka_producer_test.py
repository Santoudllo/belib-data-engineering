from kafka import KafkaProducer
import json
import requests
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

def main():
    api_url = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/belib-points-de-recharge-pour-vehicules-electriques-donnees-statiques/records"
    kafka_topic = "belib_data_topic"
    bootstrap_servers = 'localhost:9092'
    
    client = BelibAPIClient(api_url, kafka_topic, bootstrap_servers)
    client.fetch_data()

if __name__ == "__main__":
    main()

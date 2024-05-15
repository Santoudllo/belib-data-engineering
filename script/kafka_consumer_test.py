from kafka import KafkaConsumer
import json

def main():
    kafka_topic = "belib_data_topic"
    bootstrap_servers = 'localhost:9092'
    
    consumer = KafkaConsumer(kafka_topic, bootstrap_servers=bootstrap_servers, auto_offset_reset='earliest', group_id='belib_group')
    for message in consumer:
        data = json.loads(message.value.decode('utf-8'))
        print("Received data:")
        print(data)

if __name__ == "__main__":
    main()

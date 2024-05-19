from pymongo import MongoClient
from urllib.parse import quote_plus

class BikeDataPipeline:
    def __init__(self):
        self.username = 'santoudllo'
        self.password = '@Santou20'  # Remplacez par votre mot de passe réel
        self.dbname = 'belib_database'
        self.collection_name = 'belib.collection'
        self.mongodb_uri = f"mongodb+srv://{quote_plus(self.username)}:{quote_plus(self.password)}@bike.kvgkgvj.mongodb.net/{self.dbname}?retryWrites=true&w=majority"

    def fetch_data_from_mongodb(self):
        try:
            # Connect to MongoDB
            client = MongoClient(self.mongodb_uri)
            print("Connexion à MongoDB réussie.")
            
            # Access the database
            db = client[self.dbname]
            print(f"Accès à la base de données '{self.dbname}' réussi.")
            
            # Access the collection
            collection = db[self.collection_name]
            print(f"Accès à la collection '{self.collection_name}' réussi.")
            
            # Fetch the data
            data = list(collection.find({}))
            if not data:
                print("Aucun document trouvé dans la collection.")
            else:
                print(f"{len(data)} documents trouvés dans la collection.")
            
            return data
        
        except Exception as e:
            print(f"Erreur lors de la récupération des données depuis MongoDB : {e}")
            return None

# Fonction principale pour tester la connexion et la récupération des données
if __name__ == "__main__":
    pipeline = BikeDataPipeline()
    data = pipeline.fetch_data_from_mongodb()

    if data:
        print("Données récupérées depuis MongoDB :")
        print(data)
    else:
        print("Aucune donnée récupérée.")

import os
from pymongo import MongoClient
from dotenv import load_dotenv

class BikeDataPipeline:
    def __init__(self):
        # Charger les variables d'environnement
        load_dotenv()

        # Utilisation de l'URI MongoDB directement depuis l'environnement
        self.mongodb_uri = os.getenv('MONGO_URI')

        # Vérification que l'URI est bien chargée
        if not self.mongodb_uri:
            raise ValueError("L'URI MongoDB est manquante dans les variables d'environnement.")

        self.dbname = 'database_belib'  # Nom de la base de données mis à jour
        self.collection_name = 'belib'  # Nom de la collection mis à jour

    def fetch_data_from_mongodb(self, query=None):
        """
        Récupérer des données depuis MongoDB avec une requête optionnelle.

        :param query: dictionnaire représentant la requête MongoDB (par défaut, {} pour tout récupérer).
        :return: liste de documents récupérés ou None en cas d'erreur.
        """
        if query is None:
            query = {}  # Si aucune requête spécifique n'est fournie, récupérer tous les documents

        client = None
        try:
            # Connexion à MongoDB
            client = MongoClient(self.mongodb_uri)
            print("Connexion à MongoDB réussie.")
            
            # Accès à la base de données
            db = client[self.dbname]
            print(f"Accès à la base de données '{self.dbname}' réussi.")
            
            # Accès à la collection
            collection = db[self.collection_name]
            print(f"Accès à la collection '{self.collection_name}' réussi.")
            
            # Récupérer les données selon la requête fournie
            data = list(collection.find(query))
            if not data:
                print("Aucun document trouvé dans la collection.")
            else:
                print(f"{len(data)} documents trouvés dans la collection.")
            
            return data
        
        except Exception as e:
            print(f"Erreur lors de la récupération des données depuis MongoDB : {e}")
            return None
        
        finally:
            # Assurer que la connexion est bien fermée
            if client:
                client.close()
                print("Connexion à MongoDB fermée.")

# Fonction principale pour tester la connexion et la récupération des données
if __name__ == "__main__":
    # Charger les informations d'identification MongoDB depuis les variables d'environnement
    pipeline = BikeDataPipeline()

    # Exécution d'une requête pour récupérer les données
    data = pipeline.fetch_data_from_mongodb()

    # Affichage des données récupérées
    if data:
        print("Données récupérées depuis MongoDB :")
        print(data)
    else:
        print("Aucune donnée récupérée.")

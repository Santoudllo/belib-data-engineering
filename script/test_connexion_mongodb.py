import pymongo
from dotenv import load_dotenv
import os

# Charger les variables d'environnement à partir  .env
load_dotenv()

username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
dbname = os.getenv("MONGO_DBNAME")
connection_string = os.getenv("MONGO_URI").replace("<db_password>", password)

try:
    # Connexion à la base de données

    client = pymongo.MongoClient(connection_string)

    # Vérification de  la connexion

    if client:
        print("Connexion à MongoDB réussie !")
    else:
        print("Échec de la connexion à MongoDB.")

except Exception as e:
    print("Erreur lors de la connexion à MongoDB :", e)

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
db = client[dbname]
collection = db['belib']

# Vérifie si des documents existent dans la collection
count = collection.count_documents({})
print(f"Nombre de documents dans la collection 'belib' : {count}")

# Affiche quelques documents pour vérifier le contenu
for doc in collection.find().limit(5):
    print(doc)
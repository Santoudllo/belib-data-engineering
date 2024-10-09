import pymongo

# Informations de connexion
username = "alimousantou"
password = "c2U16agfAPFf8cqH" # definir le mot de pass 
dbname = "database_belib"

# URL de connexion
connection_string = f"mongodb+srv://alimousantou:<db_password>@ailab.wku4a.mongodb.net/"

try:
    # Connexion à la base de données
    client = pymongo.MongoClient(connection_string)

    # Vérifier la connexion
    if client:
        print("Connexion à MongoDB réussie !")
    else:
        print("Échec de la connexion à MongoDB.")

except Exception as e:
    print("Erreur lors de la connexion à MongoDB :", e)

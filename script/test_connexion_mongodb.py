import pymongo

# Informations de connexion
username = "santoudllo"
password = "*****" # definir le mot de pass 
dbname = "belib_database"

# URL de connexion
connection_string = f"mongodb+srv://santoudllo:<password>@bike.kvgkgvj.mongodb.net/?retryWrites=true&w=majority&appName=bike"

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

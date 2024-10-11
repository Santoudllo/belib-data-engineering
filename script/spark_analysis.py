import os
from dotenv import load_dotenv
from pyspark.sql import SparkSession

# Charger les variables d'environnement à partir de .env
load_dotenv()

username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
dbname = os.getenv("MONGO_DBNAME")
mongo_uri = os.getenv("MONGO_URI").replace("<db_password>", password)

# Créer une session Spark
spark = SparkSession.builder \
    .appName("MongoDBSparkIntegration") \
    .config("spark.mongodb.input.uri", mongo_uri) \
    .config("spark.mongodb.output.uri", mongo_uri) \
    .getOrCreate()

# Lire les données depuis la collection MongoDB
df = spark.read \
    .format("mongo") \
    .option("database", dbname) \
    .option("collection", "belib") \
    .load()

# Afficher le schéma des données
df.printSchema()

# Afficher le nombre de documents
count = df.count()
print(f"Nombre de documents dans la collection 'belib' : {count}")

# Afficher quelques documents pour vérifier le contenu
df.show(5)

# Arrêter la session Spark
spark.stop()

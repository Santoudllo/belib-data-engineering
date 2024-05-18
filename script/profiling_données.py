import warnings
from ydata_profiling import ProfileReport
import pandas as pd
import pdfkit
from pymongo import MongoClient
from urllib.parse import quote_plus

# Ignorer les avertissements de dépréciation de pandas_profiling
warnings.filterwarnings("ignore", category=DeprecationWarning)

class BikeDataPipeline:
    def __init__(self):
        self.username = 'santoudllo'
        self.password = '*********'
        self.dbname = 'belib_database'
        self.collection_name = 'belib.collection'
        self.mongodb_uri = f"mongodb+srv://{quote_plus(self.username)}:{quote_plus(self.password)}@bike.kvgkgvj.mongodb.net/{self.dbname}?retryWrites=true&w=majority"

    def fetch_data_from_mongodb(self):
        try:
            client = MongoClient(self.mongodb_uri)
            db = client[self.dbname]
            collection = db[self.collection_name]
            data = list(collection.find({}))  
            return data
        except Exception as e:
            print(f"Erreur lors de la récupération des données depuis MongoDB : {e}")
            return None

# Créer une instance de la pipeline
pipeline = BikeDataPipeline()
data = pipeline.fetch_data_from_mongodb()

# Afficher les données sous forme de DataFrame pandas
df = pd.DataFrame(data)

# Le rapport de profilage
prof = ProfileReport(df)

# Générer le rapport HTML
prof.to_file(output_file='../docs/rapport.html')

# Convertir en PDF et sauvegarder
pdfkit.from_file('../docs/rapport.html', '/../docs/rapport.pdf')

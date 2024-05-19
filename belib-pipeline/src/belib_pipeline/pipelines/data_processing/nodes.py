import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

def fetch_data() -> pd.DataFrame:
    return pd.read_csv("data/01_raw/belib_data.csv")

def rename_columns(data: pd.DataFrame) -> pd.DataFrame:
    rename_columns = {
        "id_pdc_local": "ID PDC local",
        "statut_pdc": "Statut du point de recharge",
        "id_station_local": "ID Station Local",
        "id_station_itinerance": "ID Station Itinérance",
        "nom_station": "Nom Station",
        "code_insee_commune": "Code INSEE Commune",
        "implantation_station": "Implantation Station",
        "nbre_pdc": "Nombre PDC",
        "date_maj": "Heure mise à jour",
        "condition_acces": "Condition Accès",
        "adresse_station": "Adresse Station",
        "coordonneesxy": "coordonneesXY",
        "arrondissement": "Arrondissement"
    }
    
    data.rename(columns=rename_columns, inplace=True)
    return data

def preprocess_data(data: pd.DataFrame) -> pd.DataFrame:
    # Suppression de la colonne 'url_description_pdc'
    if 'url_description_pdc' in data.columns:
        data = data.drop(columns=['url_description_pdc'])
    
    # Identification des caractéristiques numériques et catégorielles
    numeric_features = data.select_dtypes(include=['float', 'int']).columns
    categorical_features = data.select_dtypes(include=['object']).columns

    # Gestion des valeurs manquantes pour les caractéristiques numériques
    data[numeric_features] = data[numeric_features].fillna(data[numeric_features].mean())

    # Détection et traitement des valeurs aberrantes pour les caractéristiques numériques
    for feature in numeric_features:
        Q1 = data[feature].quantile(0.25)
        Q3 = data[feature].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - (1.5 * IQR)
        upper_bound = Q3 + (1.5 * IQR)
        data[feature] = np.where((data[feature] < lower_bound) | (data[feature] > upper_bound),
                                 data[feature].mean(), data[feature])

    # Normalisation des caractéristiques numériques
    scaler = StandardScaler()
    data[numeric_features] = scaler.fit_transform(data[numeric_features])

    # Gestion des valeurs manquantes pour les caractéristiques catégorielles
    data[categorical_features] = data[categorical_features].fillna(data[categorical_features].mode().iloc[0])

    # Encodage des caractéristiques catégorielles
    data = pd.get_dummies(data, columns=categorical_features, drop_first=True)

    return data

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

def fetch_data() -> pd.DataFrame:
    return pd.read_csv("/home/santoudllo/Desktop/Projet_perso/belib-data-engineering/belib-pipeline/data/01_raw/belib_data.csv")

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

def train_model(data: pd.DataFrame) -> dict:
    # Diviser les données en caractéristiques (X) et cible (y)
    X = data.drop(columns=["Statut du point de recharge"])
    y = data["Statut du point de recharge"]

    # Diviser les données en ensembles de formation et de test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Entraîner un modèle de forêt aléatoire
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Prédire sur l'ensemble de test
    y_pred = model.predict(X_test)

    # Calculer les métriques de performance
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)

    # Enregistrer le modèle
    model_path = "/home/santoudllo/Desktop/Projet_perso/belib-data-engineering/belib-pipeline/data/06_models/random_forest_model.pkl"
    joblib.dump(model, model_path)

    return {
        "accuracy": accuracy,
        "classification_report": report
    }

def save_metrics(metrics: dict):
    # Enregistrer les métriques de performance
    metrics_df = pd.DataFrame(metrics).transpose()
    metrics_path = "/home/santoudllo/Desktop/Projet_perso/belib-data-engineering/belib-pipeline/data/09_tracking/metrics.csv"
    metrics_df.to_csv(metrics_path)

    # Éventuellement, afficher les métriques
    print("Accuracy:", metrics["accuracy"])
    print("Classification Report:")
    print(metrics_df)

def node_train_model(preprocessed_data: pd.DataFrame) -> dict:
    return train_model(preprocessed_data)

def node_save_metrics(metrics: dict):
    save_metrics(metrics)

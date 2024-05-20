import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import json

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
    print("Columns after renaming:", data.columns)
    return data

def preprocess_data(data: pd.DataFrame) -> pd.DataFrame:
    print("Columns before preprocessing:", data.columns)
    
    # Suppression de la colonne 'url_description_pdc'
    if 'url_description_pdc' in data.columns:
        data = data.drop(columns=['url_description_pdc'])
    
    print("Columns after dropping 'url_description_pdc':", data.columns)
    
    # Identification des caractéristiques numériques et catégorielles
    numeric_features = data.select_dtypes(include=['float', 'int']).columns
    categorical_features = data.select_dtypes(include=['object']).columns

    # Gestion des valeurs manquantes pour les caractéristiques numériques
    data[numeric_features] = data[numeric_features].fillna(data[numeric_features].mean())

    print("Columns after filling numeric NaNs:", data.columns)
    
    # Détection et traitement des valeurs aberrantes pour les caractéristiques numériques
    for feature in numeric_features:
        Q1 = data[feature].quantile(0.25)
        Q3 = data[feature].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - (1.5 * IQR)
        upper_bound = Q3 + (1.5 * IQR)
        data[feature] = np.where((data[feature] < lower_bound) | (data[feature] > upper_bound),
                                 data[feature].mean(), data[feature])

    print("Columns after handling outliers:", data.columns)
    
    # Normalisation des caractéristiques numériques
    scaler = StandardScaler()
    data[numeric_features] = scaler.fit_transform(data[numeric_features])

    print("Columns after scaling numeric features:", data.columns)
    
    # Gestion des valeurs manquantes pour les caractéristiques catégorielles
    data[categorical_features] = data[categorical_features].fillna(data[categorical_features].mode().iloc[0])

    print("Columns after filling categorical NaNs:", data.columns)
    
    # Encodage des caractéristiques catégorielles, excluant la colonne "Statut du point de recharge"
    categorical_features = categorical_features.drop('Statut du point de recharge')
    data = pd.get_dummies(data, columns=categorical_features, drop_first=True)

    print("Columns after encoding categorical features:", data.columns)
    
    return data

def train_model(data: pd.DataFrame) -> dict:
    print("Columns before training:", data.columns)
    
    # Vérifier la présence de la colonne "Statut du point de recharge"
    if "Statut du point de recharge" not in data.columns:
        raise KeyError("La colonne 'Statut du point de recharge' n'est pas présente dans les données.")
    
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
    model_path = "data/06_models/random_forest_model.pkl"
    joblib.dump(model, model_path)

    return {
        "accuracy": accuracy,
        "classification_report": report
    }

def save_metrics(metrics: dict):
    # Convertir le dictionnaire de métriques en DataFrame, en traitant séparément les éléments imbriqués
    accuracy_df = pd.DataFrame({"accuracy": [metrics["accuracy"]]})
    report_df = pd.DataFrame(metrics["classification_report"]).transpose()
    
    # Sauvegarder les métriques en JSON
    accuracy_path = "data/09_tracking/accuracy.json"
    report_path = "data/09_tracking/classification_report.json"
    
    accuracy_df.to_json(accuracy_path, orient="records")
    report_df.to_json(report_path, orient="index")

    # Éventuellement, afficher les métriques
    print("Accuracy:", metrics["accuracy"])
    print("Classification Report:")
    print(report_df)

def node_train_model(preprocessed_data: pd.DataFrame) -> dict:
    return train_model(preprocessed_data)

def node_save_metrics(metrics: dict):
    save_metrics(metrics)

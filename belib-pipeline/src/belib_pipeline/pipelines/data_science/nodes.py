import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

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
    model_path = "data/06_models/random_forest_model.pkl"
    joblib.dump(model, model_path)

    return {
        "accuracy": accuracy,
        "classification_report": report
    }

def save_metrics(metrics: dict):
    # Enregistrer les métriques de performance
    metrics_df = pd.DataFrame(metrics).transpose()
    metrics_path = "data/09_tracking/model_metrics.json"
    metrics_df.to_json(metrics_path)

    # Éventuellement, afficher les métriques
    print("Accuracy:", metrics["accuracy"])
    print("Classification Report:")
    print(metrics_df)

def node_train_model(preprocessed_data: pd.DataFrame) -> dict:
    return train_model(preprocessed_data)

def node_save_metrics(metrics: dict):
    save_metrics(metrics)

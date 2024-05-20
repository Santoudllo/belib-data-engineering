import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
import joblib
from imblearn.over_sampling import SMOTE

def train_model(data: pd.DataFrame) -> dict:
    print("Début de l'entraînement du modèle...")

    # Utiliser l'ensemble complet des données pour l'entraînement
    data_sampled = data.sample(frac=1.0, random_state=42)
    print(f"Nombre de lignes après échantillonnage: {data_sampled.shape[0]}")

    # Séparer les données en caractéristiques et cible
    X = data_sampled.drop(columns=["Statut du point de recharge"])
    y = data_sampled["Statut du point de recharge"]

    # Appliquer SMOTE pour équilibrer le jeu de données
    print("Application de SMOTE...")
    smote = SMOTE(random_state=42, k_neighbors=1)
    X_resampled, y_resampled = smote.fit_resample(X, y)

    # Séparer les données resampled en ensembles d'entraînement et de test
    print("Séparation des données d'entraînement et de test...")
    X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

    # Entraîner le modèle Random Forest
    print("Entraînement du modèle Random Forest...")
    param_grid = {'n_estimators': [50], 'max_depth': [None, 10]}
    rf_model = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=5)
    rf_model.fit(X_train, y_train)

    # Prédire avec le modèle Random Forest
    print("Prédiction avec le modèle Random Forest...")
    y_pred_rf = rf_model.predict(X_test)

    # Calculer l'exactitude et le rapport de classification pour Random Forest
    rf_accuracy = accuracy_score(y_test, y_pred_rf)
    rf_report = classification_report(y_test, y_pred_rf, output_dict=True)
    rf_roc_auc = roc_auc_score(y_test, rf_model.predict_proba(X_test), multi_class='ovr')

    # Sauvegarder le modèle Random Forest
    rf_model_path = "data/06_models/random_forest_model.pkl"
    joblib.dump(rf_model, rf_model_path)
    print(f"Modèle Random Forest sauvegardé à {rf_model_path}")

    # Scores de validation croisée pour Random Forest
    rf_cross_val_scores = cross_val_score(rf_model, X, y, cv=StratifiedKFold(n_splits=5))
    print(f"Scores de validation croisée du Random Forest : {rf_cross_val_scores}")

    # Entraîner le modèle de régression logistique
    print("Entraînement du modèle de régression logistique...")
    lr_model = LogisticRegression(max_iter=1000, random_state=42)
    lr_model.fit(X_train, y_train)

    # Prédire avec le modèle de régression logistique
    print("Prédiction avec le modèle de régression logistique...")
    y_pred_lr = lr_model.predict(X_test)

    # Calculer l'exactitude et le rapport de classification pour la régression logistique
    lr_accuracy = accuracy_score(y_test, y_pred_lr)
    lr_report = classification_report(y_test, y_pred_lr, output_dict=True)
    lr_roc_auc = roc_auc_score(y_test, lr_model.predict_proba(X_test), multi_class='ovr')

    # Sauvegarder le modèle de régression logistique
    lr_model_path = "data/06_models/logistic_regression_model.pkl"
    joblib.dump(lr_model, lr_model_path)
    print(f"Modèle de régression logistique sauvegardé à {lr_model_path}")

    # Scores de validation croisée pour la régression logistique
    lr_cross_val_scores = cross_val_score(lr_model, X, y, cv=StratifiedKFold(n_splits=5))
    print(f"Scores de validation croisée de la régression logistique : {lr_cross_val_scores}")

    return {
        "rf_accuracy": rf_accuracy,
        "rf_classification_report": rf_report,
        "rf_cross_val_scores": rf_cross_val_scores.tolist(),
        "rf_roc_auc": rf_roc_auc,
        "lr_accuracy": lr_accuracy,
        "lr_classification_report": lr_report,
        "lr_cross_val_scores": lr_cross_val_scores.tolist(),
        "lr_roc_auc": lr_roc_auc
    }

def save_metrics(metrics: dict):
    metrics_path = "data/09_tracking/model_metrics.json"
    pd.Series(metrics).to_json(metrics_path)
    print(f"Métriques sauvegardées à {metrics_path}")

    print("Random Forest Accuracy:", metrics["rf_accuracy"])
    print("Random Forest ROC-AUC:", metrics["rf_roc_auc"])
    print("Random Forest Classification Report:")
    print(pd.DataFrame(metrics["rf_classification_report"]).transpose())

    print("Logistic Regression Accuracy:", metrics["lr_accuracy"])
    print("Logistic Regression ROC-AUC:", metrics["lr_roc_auc"])
    print("Logistic Regression Classification Report:")
    print(pd.DataFrame(metrics["lr_classification_report"]).transpose())

def visualize_metrics(metrics: dict):
    import matplotlib.pyplot as plt
    import seaborn as sns

    rf_report = pd.DataFrame(metrics["rf_classification_report"]).transpose()
    lr_report = pd.DataFrame(metrics["lr_classification_report"]).transpose()

    print("Random Forest Classification Report:")
    print(rf_report)

    sns.heatmap(rf_report.drop(columns=['support']).T, annot=True)
    plt.title('Random Forest Classification Report')
    plt.show()

    print("Logistic Regression Classification Report:")
    print(lr_report)

    sns.heatmap(lr_report.drop(columns=['support']).T, annot=True)
    plt.title('Logistic Regression Classification Report')
    plt.show()

def node_train_model(preprocessed_data: pd.DataFrame) -> dict:
    return train_model(preprocessed_data)

def node_save_metrics(metrics: dict):
    save_metrics(metrics)

def node_visualize_metrics(metrics: dict):
    visualize_metrics(metrics)

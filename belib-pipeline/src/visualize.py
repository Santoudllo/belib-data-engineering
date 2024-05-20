import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Charger les métriques
accuracy_df = pd.read_json("data/09_tracking/accuracy.json")
report_df = pd.read_json("data/09_tracking/classification_report.json")

# Afficher l'exactitude
print("Accuracy:", accuracy_df["accuracy"].values[0])

# Afficher le rapport de classification
print(report_df)

# Visualiser le rapport de classification
sns.heatmap(report_df.drop(columns=['support']).T, annot=True)
plt.title('Classification Report')
plt.show()

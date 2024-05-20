import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def visualize_metrics(metrics: dict):
    accuracy = metrics["accuracy"]
    classification_report = metrics["classification_report"]

    # Convert classification report to DataFrame
    report_df = pd.DataFrame(classification_report).transpose()

    # Print accuracy and classification report
    print(f"Accuracy: {accuracy}")
    print("Classification Report:")
    print(report_df)

    # Plot heatmap for classification report
    plt.figure(figsize=(10, 6))
    sns.heatmap(report_df.drop(columns=['support']).T, annot=True, cmap='viridis')
    plt.title('Classification Report Heatmap')
    plt.show()

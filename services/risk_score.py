import pandas as pd

# Load severity dataset
severity_df = pd.read_csv("data/Symptom-severity.csv")

# Create dictionary
severity_dict = dict(zip(severity_df["Symptom"], severity_df["weight"]))


def calculate_risk(selected_symptoms):

    total_score = 0

    for symptom in selected_symptoms:

        total_score += severity_dict.get(symptom, 0)

    if total_score <= 5:
        risk = "🟢 Low"

    elif total_score <= 15:
        risk = "🟡 Medium"

    else:
        risk = "🔴 High"

    return total_score, risk
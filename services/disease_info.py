import pandas as pd

description_df = pd.read_csv("data/symptom_Description.csv")
precaution_df = pd.read_csv("data/symptom_precaution.csv")


def get_description(disease):

    row = description_df[
        description_df["Disease"] == disease
    ]

    if row.empty:
        return "Description not available."

    return row.iloc[0]["Description"]

def get_precautions(disease):

    row = precaution_df[
        precaution_df["Disease"] == disease
    ]

    if row.empty:
        return []

    return [
        row.iloc[0]["Precaution_1"],
        row.iloc[0]["Precaution_2"],
        row.iloc[0]["Precaution_3"],
        row.iloc[0]["Precaution_4"],
    ]
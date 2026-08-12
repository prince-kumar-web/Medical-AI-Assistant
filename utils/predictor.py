import pickle
import numpy as np

from utils.preprocess import prepare_input


# Load trained model
with open("models/logistic_regression.pkl", "rb") as file:
    model = pickle.load(file)

# Load label encoder
with open("models/label_encoder.pkl", "rb") as file:
    label_encoder = pickle.load(file)


def predict_disease(selected_symptoms):
    """
    Returns Top 3 predicted diseases with confidence score.
    """

    # Convert symptoms to input vector
    input_vector = prepare_input(selected_symptoms)

    # Predict probabilities
    probabilities = model.predict_proba([input_vector])[0]

    # Get indices of top 3 probabilities
    top3_indices = np.argsort(probabilities)[-3:][::-1]

    predictions = []

    for index in top3_indices:
        disease = label_encoder.inverse_transform([index])[0]
        confidence = round(probabilities[index] * 100, 2)

        predictions.append({
            "disease": disease,
            "confidence": confidence
        })

    return predictions


import torch
from transformers import AutoTokenizer, AutoModel


# ==============================
# BERT MODEL
# ==============================

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

tokenizer = AutoTokenizer.from_pretrained(
    "models/bert_tokenizer"
)

bert_model = AutoModel.from_pretrained(
    "models/bert_model"
)

bert_model = bert_model.to(device)
bert_model.eval()


# ==============================
# BERT CLASSIFIER
# ==============================

with open(
    "models/bert_logistic_regression.pkl",
    "rb"
) as file:

    bert_model_classifier = pickle.load(file)


# ==============================
# BERT PREDICTION
# ==============================

def predict_disease_bert(text):
    """
    Predict Top 3 diseases from natural-language symptoms
    using BERT embeddings + Logistic Regression.
    """

    inputs = tokenizer(
        text,
        padding=True,
        truncation=True,
        max_length=64,
        return_tensors="pt"
    )

    inputs = {
        key: value.to(device)
        for key, value in inputs.items()
    }

    with torch.no_grad():

        outputs = bert_model(**inputs)

    # CLS embedding → 768 dimensions
    embedding = outputs.last_hidden_state[:, 0, :]

    embedding = embedding.cpu().numpy()

    # Prediction probabilities
    probabilities = (
        bert_model_classifier
        .predict_proba(embedding)[0]
    )

    classes = bert_model_classifier.classes_

    # Top 3
    top3_indices = np.argsort(
        probabilities
    )[-3:][::-1]

    predictions = []

    for index in top3_indices:

        predictions.append({
            "disease": classes[index],
            "confidence": round(
                probabilities[index] * 100,
                2
            )
        })

    return predictions
import pickle

# Load symptom list
with open("models/symptoms.pkl", "rb") as file:
    ALL_SYMPTOMS = pickle.load(file)


def prepare_input(selected_symptoms):
    """
    Convert selected symptoms into 132-length binary vector
    """

    input_vector = [0] * len(ALL_SYMPTOMS)

    for symptom in selected_symptoms:
        if symptom in ALL_SYMPTOMS:
            index = ALL_SYMPTOMS.index(symptom)
            input_vector[index] = 1

    return input_vector
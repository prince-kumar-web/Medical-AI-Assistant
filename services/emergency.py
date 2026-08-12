EMERGENCY_SYMPTOMS = {

    "chest_pain",

    "breathlessness",

    "coma",

    "unconsciousness",

    "internal_itching",

    "receiving_blood_transfusion",

    "receiving_unsterile_injections",

    "acute_liver_failure"
}

def check_emergency(selected_symptoms):

    matched = []

    for symptom in selected_symptoms:

        if symptom in EMERGENCY_SYMPTOMS:
            matched.append(symptom)

    return matched
import re

from utils.multilingual_symptoms import SYMPTOM_ALIASES


def normalize_text(text):

    text = str(text).lower().strip()

    # punctuation remove
    text = re.sub(r"[^\w\s]", " ", text)

    # Multiple spaces ko single space
    text = re.sub(r"\s+", " ", text)

    replacements = {
        "mein": "me",
        "m": "me",
        "hain": "hai",
        "hu": "hai",
        "ho": "hai",
        "rahi": "raha",
        "rhi": "raha",
        "kr": "kar",
    }

    words = text.split()

    normalized_words = [
        replacements.get(word, word)
        for word in words
    ]

    return " ".join(normalized_words)


def extract_symptoms(text, symptoms):

    # User text normalize
    text = normalize_text(text)

    found_symptoms = []

    # Dataset symptoms ka mapping
    symptom_map = {
        str(symptom).strip().lower(): symptom
        for symptom in symptoms
    }

    # Har symptom ke aliases check karo
    for symptom_key, aliases in SYMPTOM_ALIASES.items():

        symptom_key = str(
            symptom_key
        ).strip().lower()

        # Dataset me symptom available hai?
        if symptom_key not in symptom_map:
            continue

        # Original + aliases
        all_aliases = list(aliases)

        all_aliases.append(symptom_key)

        all_aliases.append(
            symptom_key.replace("_", " ")
        )

        # Har alias check karo
        for alias in all_aliases:

            alias = normalize_text(alias)

            if not alias:
                continue

            if alias in text:

                found_symptoms.append(
                    symptom_map[symptom_key]
                )

                break

    # Duplicate remove
    return list(
        dict.fromkeys(found_symptoms)
    )





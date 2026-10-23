
import streamlit as st
import pickle
import requests
from PIL import Image

from utils.predictor import (
    predict_disease,
    predict_disease_bert
)

from services.disease_info import (
    get_description,
    get_precautions
)

from services.risk_score import calculate_risk
from services.emergency import check_emergency

from utils.text_processor import extract_symptoms
from services.llama_chat import generate_health_response
try:
    from utils.predictor import predict_disease, predict_disease_bert
except ModuleNotFoundError as e:
    st.error(f"Diagnostic — missing module: {e.name}")
    st.stop()



# PAGE CONFIG


st.set_page_config(
    page_title="Medical AI Assistant",
    page_icon="🩺",
    layout="wide"
)


# HERO IMAGE

image = Image.open(
    "assets/ChatGPT Image Aug 10, 2026, 07_41_48 PM.png"
)

st.image(
    image,
    use_container_width=True
)








# TITLE


st.write(
    "Select your symptoms or describe them in your own words."
)

st.info(
    "⚠️ This application is for educational purposes only "
    "and does not replace professional medical advice."
)



# SESSION STATE


if "predictions" not in st.session_state:
    st.session_state.predictions = None

if "active_symptoms" not in st.session_state:
    st.session_state.active_symptoms = []

if "prediction_source" not in st.session_state:
    st.session_state.prediction_source = None



# LOAD SYMPTOMS


with open("models/symptoms.pkl", "rb") as file:
    symptoms = pickle.load(file)



# DESCRIBE YOUR SYMPTOMS


st.subheader("📝 Describe Your Symptoms")

symptom_text = st.text_area(
    "Write your symptoms in your own words:",
    placeholder=(
        "Example: mujhe khujli aur skin par daane ho rahe hain"
    ),
    height=120
)



# ANALYZE DESCRIPTION


if st.button("🔍 Analyze Symptoms"):

    if not symptom_text.strip():

        st.warning(
            "Please describe your symptoms."
        )

    else:

        extracted_symptoms = extract_symptoms(
            symptom_text,
            symptoms
        )

        if not extracted_symptoms:

            st.warning(
                "No known symptoms were detected. "
                "Try describing your symptoms differently."
            )

        else:

            st.success(
                "Symptoms detected successfully:"
            )

            for symptom in extracted_symptoms:

                st.write(
                    f"✅ {symptom.replace('_', ' ')}"
                )



# SELECT SYMPTOMS


st.subheader("🔹 Select Symptoms")

selected_symptoms = st.multiselect(
    "Choose symptoms:",
    symptoms
)



# DISEASE PREDICTION


st.subheader("🩺 Disease Prediction")



# PREDICT FROM SELECTED SYMPTOMS


if st.button("Predict Disease"):

    if len(selected_symptoms) == 0:

        st.warning(
            "Please select at least one symptom "
            "from the list above."
        )

    else:

        predictions = predict_disease(
            selected_symptoms
        )

        st.session_state.predictions = predictions

        st.session_state.active_symptoms = (
            selected_symptoms
        )

        st.session_state.prediction_source = (
            "selected_symptoms"
        )



# PREDICT FROM DESCRIPTION USING BERT


if st.button("🩺 Predict From Description"):

    if not symptom_text.strip():

        st.warning(
            "Please describe your symptoms first."
        )

    else:

        # Extract symptoms from natural-language description
        extracted_symptoms = extract_symptoms(
            symptom_text,
            symptoms
        )

        if not extracted_symptoms:

            st.warning(
                "No known symptoms were detected. "
                "Try describing your symptoms differently."
            )

        else:

            # BERT prediction
            predictions = predict_disease_bert(
                symptom_text
            )

            st.session_state.predictions = (
                predictions
            )

            st.session_state.active_symptoms = (
                extracted_symptoms
            )

            st.session_state.prediction_source = (
                "bert"
            )



# COMMON PREDICTION RESULT


if st.session_state.predictions:

    predictions = st.session_state.predictions

    active_symptoms = (
        st.session_state.active_symptoms
    )


    
    # TOP 3 DISEASES
    

    st.subheader(
        "Top 3 Possible Diseases"
    )

    for i, prediction in enumerate(
        predictions,
        start=1
    ):

        st.success(
            f"{i}. {prediction['disease']} "
            f"({prediction['confidence']}%)"
        )


   
    # TOP PREDICTED DISEASE
    

    disease = predictions[0]["disease"]


   
    # RISK SCORE
   

    score, risk = calculate_risk(
        active_symptoms
    )

    st.subheader(
        "Risk Assessment"
    )

    st.metric(
        label="Risk Score",
        value=score
    )

    st.write(
        f"Risk Level: {risk}"
    )


    
    # EMERGENCY DETECTION
   

    matched = check_emergency(
        active_symptoms
    )

    if matched:

        st.error(
            "🚨 Emergency! Please consult "
            "a doctor immediately."
        )

        st.write(
            "Emergency Symptoms Detected:"
        )

        for symptom in matched:

            st.write(
                f"• {symptom}"
            )


    
    # DISEASE DESCRIPTION
   

    st.subheader(
        "Disease Description"
    )

    description = get_description(
        disease
    )

    st.write(
        description
    )


    
    # PRECAUTIONS
    

    st.subheader(
        "Precautions"
    )

    precautions = get_precautions(
        disease
    )

    for precaution in precautions:

        st.write(
            f"✅ {precaution}"
        )



# HOSPITAL SEARCH FUNCTION


def find_hospitals(city):

    url = (
        "https://nominatim.openstreetmap.org/search"
    )

    params = {
        "q": f"hospitals in {city}",
        "format": "json",
        "limit": 5
    }

    headers = {
        "User-Agent": "Medical-AI-Assistant"
    }

    try:

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )

        if response.status_code != 200:

            return []

        return response.json()

    except requests.RequestException:

        return []



# NEARBY HOSPITALS


st.subheader("🏥 Nearby Hospitals")

city = st.text_input(
    "Enter your city",
    placeholder="e.g. Patna"
)


if st.button("Find Hospitals"):

    if not city.strip():

        st.warning(
            "Please enter your city."
        )

    else:

        hospitals = find_hospitals(
            city
        )

        if not hospitals:

            st.warning(
                "No hospitals found."
            )

        else:

            st.success(
                f"Found {len(hospitals)} hospitals "
                f"near {city}"
            )

            for i, hospital in enumerate(
                hospitals,
                start=1
            ):

                name = hospital.get(
                    "name"
                )

                if not name:

                    name = hospital.get(
                        "display_name",
                        "Hospital"
                    )

                address = hospital.get(
                    "display_name",
                    "Address not available"
                )

                latitude = hospital.get(
                    "lat"
                )

                longitude = hospital.get(
                    "lon"
                )

                st.markdown(
                    f"### 🏥 {i}. {name}"
                )

                st.write(
                    f"📍 {address}"
                )

                if latitude and longitude:

                    map_link = (
                        "https://www.openstreetmap.org/"
                        f"?mlat={latitude}"
                        f"&mlon={longitude}"
                    )

                    st.markdown(
                        f"[🗺️ Open Location on Map]"
                        f"({map_link})"
                    )

                st.divider()




    st.subheader("💬 AI Health Assistant")

user_message = st.text_area(
    "Ask a health-related question:",
    placeholder="Example: I have a headache since yesterday."
)

if st.button("Ask AI Assistant"):

    if not user_message.strip():

        st.warning("Please enter your question.")

    else:

        response = generate_health_response(
            user_message
        )

        st.write(response)            













# cd "C:\Users\princ\Videos\streamlit_projects\streamlit\Medical AI Assistant"
 
# streamlit run app.py





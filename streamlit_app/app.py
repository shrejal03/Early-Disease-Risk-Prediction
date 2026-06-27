import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load("models/disease_prediction_model.pkl")

st.title("🏥 Early Disease Risk Prediction")

st.markdown(
    "Enter patient details below to predict cardiovascular disease risk."
)

age_years = st.number_input(
    "Age (Years)",
    min_value=18,
    max_value=100,
    value=25
)

age = age_years * 365
gender_text = st.selectbox(
    "Gender",
    ["Female", "Male"]
)

gender = 1 if gender_text == "Female" else 2
height = st.number_input("Height (cm)", min_value=100, max_value=250)
weight = st.number_input("Weight (kg)", min_value=20, max_value=200)

ap_hi = st.number_input("Systolic BP (ap_hi)", min_value=50, max_value=250)
ap_lo = st.number_input("Diastolic BP (ap_lo)", min_value=30, max_value=200)

cholesterol_text = st.selectbox(
    "Cholesterol Level",
    [
        "Normal",
        "Above Normal",
        "Well Above Normal"
    ]
)

cholesterol_map = {
    "Normal": 1,
    "Above Normal": 2,
    "Well Above Normal": 3
}

cholesterol = cholesterol_map[cholesterol_text]
gluc_text = st.selectbox(
    "Glucose Level",
    [
        "Normal",
        "Above Normal",
        "Well Above Normal"
    ]
)

gluc_map = {
    "Normal": 1,
    "Above Normal": 2,
    "Well Above Normal": 3
}

gluc = gluc_map[gluc_text]

smoke_text = st.selectbox(
    "Do you smoke?",
    ["No", "Yes"]
)

smoke = 1 if smoke_text == "Yes" else 0
alco_text = st.selectbox(
    "Do you consume alcohol?",
    ["No", "Yes"]
)

alco = 1 if alco_text == "Yes" else 0
active_text = st.selectbox(
    "Physically Active?",
    ["No", "Yes"]
)

active = 1 if active_text == "Yes" else 0

age_years = age / 365
bmi = weight / ((height / 100) ** 2)


if ap_hi >= 140 or ap_lo >= 90:
    bp_stage2 = 1
    bp_stage1 = 0
    bp_normal = 0

elif ap_hi >= 130 or ap_lo >= 80:
    bp_stage2 = 0
    bp_stage1 = 1
    bp_normal = 0

else:
    bp_stage2 = 0
    bp_stage1 = 0
    bp_normal = 1

input_data = pd.DataFrame({
    "age": [age],
    "gender": [gender],
    "height": [height],
    "weight": [weight],
    "ap_hi": [ap_hi],
    "ap_lo": [ap_lo],
    "cholesterol": [cholesterol],
    "gluc": [gluc],
    "smoke": [smoke],
    "alco": [alco],
    "active": [active],
    "age_years": [age_years],
    "bmi": [bmi],
    "bp_category_Hypertension Stage 1": [bp_stage1],
    "bp_category_Hypertension Stage 2": [bp_stage2],
    "bp_category_Normal": [bp_normal]
})


if st.button("Predict"):
    prediction = model.predict(input_data)

    if prediction[0] == 1:
        st.error("High Disease Risk")
    else:
        st.success("Low Disease Risk")
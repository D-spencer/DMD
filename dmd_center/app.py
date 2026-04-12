import streamlit as st
import numpy as np
import pickle

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="DMD Clinical Space", layout="wide")

# -------------------------------
# LOAD MODELS (Make sure you have these)
# -------------------------------
# Replace with your actual model paths
# diabetes_model = pickle.load(open("models/diabetes.pkl", "rb"))
# heart_model = pickle.load(open("models/heart.pkl", "rb"))
# bp_model = pickle.load(open("models/bp.pkl", "rb"))

# TEMPORARY (for testing UI)
def fake_model(input_data):
    return np.random.choice([0, 1]), np.random.randint(50, 95)

# -------------------------------
# HEADER
# -------------------------------
st.markdown(
    "<h1 style='text-align: center;'>DMD Clinical Space</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<h4 style='text-align: center;'>Your Home To Go Diagnose System</h4>",
    unsafe_allow_html=True
)

st.write("---")

# -------------------------------
# DISEASE SELECTION (TABS)
# -------------------------------
tab1, tab2, tab3 = st.tabs(["🩸 Diabetes", "❤️ Heart Disease", "💉 Hypertension"])

# -------------------------------
# DIABETES TAB
# -------------------------------
with tab1:
    st.subheader("Diabetes Risk Assessment")

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", min_value=1, max_value=120)
        glucose = st.number_input("Glucose Level")
        bmi = st.number_input("BMI")

    with col2:
        bp = st.number_input("Blood Pressure")
        activity = st.selectbox("Physical Activity", ["Low", "Medium", "High"])
        gender = st.selectbox("Gender", ["Male", "Female"])

    if st.button("Predict Diabetes"):
        # Replace fake_model with real model
        pred, prob = fake_model([age, glucose, bmi, bp])

        st.write("### Result")
        if pred == 1:
            st.error(f"High Risk ⚠️ ({prob}%)")
        else:
            st.success(f"Low Risk ✅ ({prob}%)")

# -------------------------------
# HEART DISEASE TAB
# -------------------------------
with tab2:
    st.subheader("Heart Disease Assessment")

    col1, col2 = st.columns(2)

    with col1:
        age_h = st.number_input("Age ", key="h_age")
        cholesterol = st.number_input("Cholesterol")
        max_hr = st.number_input("Max Heart Rate")

    with col2:
        bp_h = st.number_input("Blood Pressure ", key="h_bp")
        smoking = st.selectbox("Smoking", ["Yes", "No"])
        exercise = st.selectbox("Exercise Level", ["Low", "Medium", "High"])

    if st.button("Predict Heart Disease"):
        pred, prob = fake_model([age_h, cholesterol, max_hr, bp_h])

        st.write("### Result")
        if pred == 1:
            st.error(f"High Risk ⚠️ ({prob}%)")
        else:
            st.success(f"Low Risk ✅ ({prob}%)")

# -------------------------------
# HYPERTENSION TAB
# -------------------------------
with tab3:
    st.subheader("Hypertension Assessment")

    col1, col2 = st.columns(2)

    with col1:
        age_b = st.number_input("Age  ", key="b_age")
        weight = st.number_input("Weight (kg)")
        height = st.number_input("Height (cm)")

    with col2:
        systolic = st.number_input("Systolic BP")
        diastolic = st.number_input("Diastolic BP")
        salt = st.selectbox("Salt Intake", ["Low", "Medium", "High"])

    if st.button("Predict Hypertension"):
        pred, prob = fake_model([age_b, weight, height, systolic, diastolic])

        st.write("### Result")
        if pred == 1:
            st.error(f"High Risk ⚠️ ({prob}%)")
        else:
            st.success(f"Low Risk ✅ ({prob}%)")

# -------------------------------
# RECOMMENDATION SECTION
# -------------------------------
st.write("---")
st.markdown("## 💡 Health Recommendations")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("🥗 Maintain a healthy diet")

with col2:
    st.info("🏃 Exercise regularly")

with col3:
    st.info("🚭 Avoid smoking & alcohol")



st.markdown("---")
st.caption("© 2026 DMD Clinical Space")

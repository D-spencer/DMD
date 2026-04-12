import streamlit as st
import numpy as np
import pickle

st.set_page_config(page_title="DMD Clinical Space", layout="wide")

# -------------------------------
# LOAD MODELS (Replace later)
# -------------------------------
def fake_model(data):
    return np.random.choice([0, 1]), np.random.randint(60, 95)

# -------------------------------
# HEADER
# -------------------------------
st.markdown("<h1 style='text-align:center;'>DMD Clinical Space</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'>Your Home To Go Diagnose System</h4>", unsafe_allow_html=True)

st.write("---")

# -------------------------------
# DISEASE TABS
# -------------------------------
tab1, tab2, tab3 = st.tabs(["🩸 Diabetes", "❤️ Heart Disease", "💉 Hypertension"])

# =========================================================
# 🩸 DIABETES
# =========================================================
with tab1:
    st.subheader("Diabetes Assessment")

    basic_tab, advanced_tab = st.tabs(["Basic", "Advanced"])

    # -------- BASIC --------
    with basic_tab:
        st.write("### Basic Screening")

        age = st.number_input("Age", key="d_age")
        bmi = st.number_input("BMI", key="d_bmi")
        glucose = st.number_input("Glucose Level", key="d_glucose")

        if st.button("Predict (Basic)", key="d_basic_btn"):
            pred, prob = fake_model([age, bmi, glucose])

            st.write("### Result")
            st.success(f"Risk: {'High ⚠️' if pred else 'Low ✅'} ({prob}%)")

    # -------- ADVANCED --------
    with advanced_tab:
        st.write("### Advanced Assessment")

        col1, col2 = st.columns(2)

        with col1:
            age_a = st.number_input("Age ", key="d_age_a")
            bmi_a = st.number_input("BMI ", key="d_bmi_a")
            glucose_a = st.number_input("Glucose ", key="d_glucose_a")

        with col2:
            bp_a = st.number_input("Blood Pressure", key="d_bp_a")
            insulin = st.number_input("Insulin Level")
            activity = st.selectbox("Physical Activity", ["Low", "Medium", "High"], key="d_act")

        if st.button("Predict (Advanced)", key="d_adv_btn"):
            pred, prob = fake_model([age_a, bmi_a, glucose_a, bp_a, insulin])

            st.write("### Result")
            st.success(f"Risk: {'High ⚠️' if pred else 'Low ✅'} ({prob}%)")

# =========================================================
# ❤️ HEART DISEASE
# =========================================================
with tab2:
    st.subheader("Heart Disease Assessment")

    basic_tab, advanced_tab = st.tabs(["Basic", "Advanced"])

    # -------- BASIC --------
    with basic_tab:
        age = st.number_input("Age", key="h_age")
        cholesterol = st.number_input("Cholesterol")
        bp = st.number_input("Blood Pressure", key="h_bp")

        if st.button("Predict (Basic)", key="h_basic"):
            pred, prob = fake_model([age, cholesterol, bp])
            st.success(f"Risk: {'High ⚠️' if pred else 'Low ✅'} ({prob}%)")

    # -------- ADVANCED --------
    with advanced_tab:
        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input("Age ", key="h_age_a")
            cholesterol = st.number_input("Cholesterol ", key="h_chol")
            max_hr = st.number_input("Max Heart Rate")

        with col2:
            bp = st.number_input("Blood Pressure ", key="h_bp_a")
            smoking = st.selectbox("Smoking", ["Yes", "No"])
            exercise = st.selectbox("Exercise Level", ["Low", "Medium", "High"])

        if st.button("Predict (Advanced)", key="h_adv"):
            pred, prob = fake_model([age, cholesterol, max_hr, bp])
            st.success(f"Risk: {'High ⚠️' if pred else 'Low ✅'} ({prob}%)")

# =========================================================
# 💉 HYPERTENSION
# =========================================================
with tab3:
    st.subheader("Hypertension Assessment")

    basic_tab, advanced_tab = st.tabs(["Basic", "Advanced"])

    # -------- BASIC --------
    with basic_tab:
        age = st.number_input("Age", key="b_age")
        systolic = st.number_input("Systolic BP")
        diastolic = st.number_input("Diastolic BP")

        if st.button("Predict (Basic)", key="b_basic"):
            pred, prob = fake_model([age, systolic, diastolic])
            st.success(f"Risk: {'High ⚠️' if pred else 'Low ✅'} ({prob}%)")

    # -------- ADVANCED --------
    with advanced_tab:
        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input("Age ", key="b_age_a")
            weight = st.number_input("Weight")
            height = st.number_input("Height")

        with col2:
            systolic = st.number_input("Systolic BP ", key="b_sys")
            diastolic = st.number_input("Diastolic BP ", key="b_dia")
            salt = st.selectbox("Salt Intake", ["Low", "Medium", "High"])

        if st.button("Predict (Advanced)", key="b_adv"):
            pred, prob = fake_model([age, weight, height, systolic, diastolic])
            st.success(f"Risk: {'High ⚠️' if pred else 'Low ✅'} ({prob}%)")

# -------------------------------
# RECOMMENDATIONS
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

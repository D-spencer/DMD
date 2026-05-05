import streamlit as st
import numpy as np
import joblib
import os 
import pandas as pd

st.set_page_config(page_title="DMD Clinical Space", layout="wide")

### this class is for basic hypertension, because it was bringing an error , so i had to do this 
class ThresholdClassifier: 
    def __init__(self , model,  threshold):
        self.model = model 
        self.threshold = threshold

    def predict(self ,  x):
        proba = self.model.predict_proba(x)[:,1]
        return (proba >= self.threshold).astype(int)
    
    def predict_proba(self , x):
        return self.model.predict_proba(x)

heart_adv_model = joblib.load("dmd_center/models/heart_advance_model_v1.pkl")
heart_basic_model = joblib.load("dmd_center/models/heart_basic_model_v1.pkl")
hyper_adv_model = joblib.load("dmd_center/models/hyper_adv_model_v1.pkl")
hyper_basic_model = joblib.load("dmd_center/models/hyper_basic_model_v1.pkl")


   # Chest pain mapping
cp_map = {
    "Mild Chest Pain (Angina Type)": "ATA",
    "Non-Anginal Pain": "NAP",
    "No Chest Pain (Asymptomatic)": "ASY",
    "Typical Angina": "TA"
}

# Fasting blood sugar
fbs_map = {
    "No (Normal)": 0,
    "Yes (High Blood Sugar)": 1
}

# Resting ECG
ecg_map = {
    "Normal Heart Rhythm": "Normal",
    "Heart Muscle Thickening": "LVH",
    "Abnormal ST Segment": "ST"
}

# Exercise angina
angina_map = {
    "No": "N",
    "Yes (Pain During Exercise)": "Y"
}

# ST slope
slope_map = {
    "Upward (Normal)": "Up",
    "Flat (Risky)": "Flat",
    "Downward (Abnormal)": "Down"
}


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
tab1, tab2, tab3 , tab4 = st.tabs(["🩸 Diabetes", "❤️ Heart Disease", "💉 Hypertension", "Stroke"])

# =========================================================
# 🩸 DIABETES
# =========================================================
with tab1:
    st.subheader("Diabetes Assessment")

    basic_tab, advanced_tab = st.tabs(["Basic Prediction", "Advanced Prediction"])

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
       col1, col2 = st.columns(2)

       with col1:
           age = st.number_input("Age", min_value=1, max_value=120, key="basic_age")
           sex = st.selectbox("Gender", ["M", "F"], key="basic_gender")
   
           chest_pain = st.selectbox(
               "Chest Pain Type",
               list(cp_map.keys()), key="basic_cp"
           )

       with col2:
           resting_bp = st.number_input("Resting Blood Pressure (Systolic, mmHg e.g.120 from 120/80)", key="basic_rbp")
           use_chol = st.checkbox("I know my cholesterol level" , value = True)
           st.caption("If you don't know your cholesterol, leave it unchecked — the system will estimate it.")

           if use_chol:
               cholesterol = st.number_input(
               "Cholesterol Level",
               key="basic_ch" )
            
           else:
               st.info("We'll estimate your cholesterol using medical averages.")
               cholesterol = None  # ✅ This triggers imputer
   
           exercise_angina = st.selectbox(
               "Chest Pain During Exercise?",
               list(angina_map.keys()), key= "basic_ea"
           )

       if st.button("Predict (Basic)"):
         
           input_data = pd.DataFrame([{
               "age": age,
               "sex": sex ,  
               "chestpaintype": cp_map[chest_pain],
               "restingbp": resting_bp,
               "cholesterol": np.nan if cholesterol is None else cholesterol,
               
               "exercise_angina": angina_map[exercise_angina]
           }])
   
           pred = heart_basic_model.predict(input_data)[0]
           prob = heart_basic_model.predict_proba(input_data)[0][1]
   
           st.write("### Result")
   
           if pred == 1:
               st.error(f"High Risk ⚠️ ({round(prob*100, 2)}%)")
           else:
               st.success(f"Low Risk ✅ ({round(prob*100, 2)}%)")
    # -------- ADVANCED --------
 
    with advanced_tab:
        st.write("### Advanced Heart Disease Assessment")
    
        col1, col2 = st.columns(2)
    
        with col1:
            age = st.number_input("Age", min_value=1, max_value=120 , key="adv_age")
            sex = st.selectbox("Gender", ["M", "F"] , key = "adv_gender")
    
            chest_pain = st.selectbox(
                "Chest Pain Type",
                list(cp_map.keys()), key="adv_cp"
            )
    
            resting_bp = st.number_input("Resting Blood Pressure (mmHg)", key="adv_rbp")
            cholesterol = st.number_input("Cholesterol Level" , key="adv_cho")
    
        with col2:
            fasting_bs = st.selectbox(
                "High Blood Sugar?",
                list(fbs_map.keys()), key="adv_fbs"
            )
    
            resting_ecg = st.selectbox(
                "Resting ECG Result",
                list(ecg_map.keys()), key="adv_recg"
            )
    
            max_hr = st.number_input("Maximum Heart Rate")
    
            exercise_angina = st.selectbox(
                "Chest Pain During Exercise?",
                list(angina_map.keys())
            )
    
            old_peak = st.number_input("ST Depression (Old Peak)")
    
            st_slope = st.selectbox(
                "ST Segment Slope",
                list(slope_map.keys())
            )

    # -------------------------------
    # PREDICTION
    # -------------------------------
        if st.button("Predict (Advanced)"):
            input_data = pd.DataFrame([{
    "age": age,
    "sex": sex,  # ✅ FIXED
    "chestpaintype": cp_map[chest_pain],
    "restingbp": resting_bp,
    "cholesterol": cholesterol,
    "fastingbs": fbs_map[fasting_bs],
    "restingecg": ecg_map[resting_ecg],
    "max_hr": max_hr,
    "exercise_angina": angina_map[exercise_angina],
    "old_peak": old_peak,
    "st_slope": slope_map[st_slope]
}])
            
            pred = heart_adv_model.predict(input_data)[0]
            prob = heart_adv_model.predict_proba(input_data)[0][1]
            
            st.write("### Result")
            
            if pred == 1:
               st.error(f"High Risk ⚠️ ({round(prob*100, 2)}%)")
            else:
               st.success(f"Low Risk ✅ ({round(prob*100, 2)}%)")

# =========================================================
# 💉 HYPERTENSION
# =========================================================
with tab3:
    st.subheader("Hypertension Assessment")

    basic_tab, advanced_tab = st.tabs(["Basic", "Advanced"])

    # -------- BASIC --------
    with basic_tab:

        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input("Age", min_value=1, max_value=120, key="b_age")
    
            gender = st.selectbox(
                "Gender",
                ["M", "F"],
                key="b_gender"
            )
    
            height = st.number_input("Height (cm)", key="b_height")
            weight = st.number_input("Weight (kg)", key="b_weight")
    
        with col2:
            cholesterol = st.selectbox(
                "Cholesterol Level",
                [1, 2, 3],
                format_func=lambda x: ["Normal", "Above Normal", "Well Above Normal"][x-1],
                key="b_chol"
            )
    
            gluc = st.selectbox(
                "Glucose Level",
                [1, 2, 3],
                format_func=lambda x: ["Normal", "Above Normal", "Well Above Normal"][x-1],
                key="b_gluc"
            )
    
            smoke = st.selectbox(
                "Do you smoke?",
                [0, 1],
                format_func=lambda x: "Yes" if x == 1 else "No",
                key="b_smoke"
            )
    
            alco = st.selectbox(
                "Do you consume alcohol?",
                [0, 1],
                format_func=lambda x: "Yes" if x == 1 else "No",
                key="b_alco"
            )
    
            active = st.selectbox(
                "Are you physically active?",
                [0, 1],
                format_func=lambda x: "Yes" if x == 1 else "No",
                key="b_active"
            )
    
    #  Auto BMI calculation
    if height > 0:
        bmi = weight / ((height / 100) ** 2)
        st.info(f"Calculated BMI: {round(bmi, 2)}")
    else:
        bmi = 0
# =======================================
    #  Prediction
    #===================================
    if st.button("Predict (Basic)", key="b_basic"):

        input_data = pd.DataFrame([{
            "age": age,
            "gender": gender,
            "height": height,
            "weight": weight,
            "bmi": bmi,
            "cholesterol": cholesterol,
            "gluc": gluc,
            "smoke": smoke,
            "alco": alco,
            "active": active
        }])

        pred = hyper_basic_model.predict(input_data)[0]
        prob = hyper_basic_model.predict_proba(input_data)[0][1]

        st.write("### Result")

        if pred == 1:
            st.error(f"High Risk ⚠️ ({round(prob*100, 2)}%)")
        else:
            st.success(f"Low Risk ✅ ({round(prob*100, 2)}%)")

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

import streamlit as st
import pandas as pd
import joblib

# --- LOAD MODEL
model = joblib.load('high_usage_predictor.pkl')

# Load label encoders
label_encoders = joblib.load("label_encoders (1).pkl")

 # page config---
st.set_page_config(page_title="Digital Balance", layout="wide")

# --- CUSTOM STYLING ---
st.markdown("""
    <style>
    /* Overall background */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(to right, #dae2f8, #d6a4a4);
        font-family: 'Poppins', sans-serif;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #f8fafc;
        border-right: 2px solid #e5e7eb;
        padding-top: 30px;
    }

    /* Headings */
    h1, h2, h3 {
        color: #1e3a8a;
        font-weight: 700;
    }

    /* Button */
    div.stButton > button {
        background: linear-gradient(to right, #2563eb, #1e40af);
        color: white;
        border-radius: 12px;
        font-size: 17px;
        font-weight: 600;
        padding: 10px 25px;
        transition: 0.3s ease-in-out;
    }
    div.stButton > button:hover {
        background: linear-gradient(to right, #1e40af, #2563eb);
        transform: scale(1.05);
    }

    /* Result box */
    .result-box {
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        font-size: 20px;
        margin-top: 20px;
        font-weight: 600;
    }
    .low {background-color: #e0f7fa; color: #006064;}
    .high {background-color: #ffebee; color: #c62828;}

    /* Info cards */
    .info-card {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR INPUTS ---
st.sidebar.header("📱 Your Digital Lifestyle Snapshot")

age = st.sidebar.number_input("Age", 10, 100, 25)
device_hours_per_day = st.sidebar.slider("Device Hours per Day", 0.0, 24.0, 5.0)
phone_unlocks = st.sidebar.number_input("Phone Unlocks per Day", 0, 200, 60)
notifications_per_day = st.sidebar.number_input("Notifications per Day", 0, 500, 100)
social_media_mins = st.sidebar.number_input("Social Media Minutes", 0, 600, 120)
study_mins = st.sidebar.number_input("Study Minutes", 0, 600, 180)
physical_activity_days = st.sidebar.slider("Physical Activity Days (per week)", 0, 7, 3)
sleep_hours = st.sidebar.slider("Sleep Hours", 0.0, 12.0, 7.0)
sleep_quality = st.sidebar.slider("Sleep Quality (1–10)", 1, 10, 7)
anxiety_score = st.sidebar.slider("Anxiety Score (1–10)", 1, 10, 5)
depression_score = st.sidebar.slider("Depression Score (1–10)", 1, 10, 4)
stress_level = st.sidebar.slider("Stress Level (1–10)", 1, 10, 5)
happiness_score = st.sidebar.slider("Happiness Score (1–10)", 1, 10, 7)
focus_score = st.sidebar.slider("Focus Score (1–10)", 1, 10, 6)
high_risk_flag = st.sidebar.selectbox("High Risk Flag", [0, 1])
productivity_score = st.sidebar.slider("Productivity Score (1–10)", 1, 10, 6)
digital_dependence_score = st.sidebar.slider("Digital Dependence Score (1–10)", 1, 10, 5)
gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])
region = st.sidebar.selectbox("Region", ["Africa", "Asia", "Europe", "North America", "South America", "Middle East"])
income_level = st.sidebar.selectbox("Income Level", ["Low", "Upper-Mid", "High", "Lower-Mid"])
education_level = st.sidebar.selectbox("Education Level", ["High School", "Master", "Bachelor", "PhD"])
daily_role = st.sidebar.selectbox("Daily Role", ["Student", "Part-time/Shift", "Caregiver/Home", "Unemployed", "Full-time Employee"])
device_type = st.sidebar.selectbox("Device Type", ["Android", "Tablet", "Laptop", "iPhone"])

st.title("Digital Balance")
st.write("Track. Predict. Improve. Master your digital balance.")

# --- INPUT DATAFRAME ---
input_data = pd.DataFrame({
    'age': [age],
    'device_hours_per_day': [device_hours_per_day],
    'phone_unlocks': [phone_unlocks],
    'notifications_per_day': [notifications_per_day],
    'social_media_mins': [social_media_mins],
    'study_mins': [study_mins],
    'physical_activity_days': [physical_activity_days],
    'sleep_hours': [sleep_hours],
    'sleep_quality': [sleep_quality],
    'anxiety_score': [anxiety_score],
    'depression_score': [depression_score],
    'stress_level': [stress_level],
    'happiness_score': [happiness_score],
    'focus_score': [focus_score],
    'high_risk_flag': [high_risk_flag],
    'productivity_score': [productivity_score],
    'digital_dependence_score': [digital_dependence_score],
    'gender': [gender],
    'region': [region],
    'income_level': [income_level],
    'education_level': [education_level],
    'daily_role': [daily_role],
    'device_type': [device_type]
})

# --- ENCODE CATEGORICAL VARIABLES ---
for col, le in label_encoders.items():
    if col in input_data.columns:
        input_data[col] = le.transform(input_data[col])

# --- MAIN LAYOUT ---
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("## Snapshot Overview")
    st.dataframe(input_data, use_container_width=True)

with col2:
    st.markdown("## 🔍 Prediction Result")
    if st.button("Reveal My Digital Pattern"):
        prediction = model.predict(input_data)[0]
        if prediction == 1:
            st.markdown('<div class="result-box high">🚨 High Device Usage — Time for a digital reset!</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="result-box low">💙 Low Device Usage — You’re maintaining great balance!</div>', unsafe_allow_html=True)

# --- WHY PREDICTION MATTERS ---
st.markdown("## Why This Prediction Matters")

st.markdown("""
<div class="info-card">
<h4>📵 Overuse Risks</h4>
<p>Excessive device use can increase stress, anxiety, and sleep disruption. 
Maintaining healthy screen habits helps mental focus and emotional wellbeing.</p>
</div>

<div class="info-card">
<h4> Balance Matters</h4>
<p>Healthy habits — such as enough sleep, exercise, and study — counteract high device hours 
and keep your digital lifestyle balanced.</p>
</div>

<div class="info-card">
<h4> Recommendation</h4>
<p>If your digital usage is high, consider setting daily limits, turning off unnecessary notifications, 
and scheduling regular “offline breaks.”</p>
</div>
""", unsafe_allow_html=True)


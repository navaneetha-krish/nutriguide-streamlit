import streamlit as st
import sqlite3
import os
import base64

# ===========================
# DATABASE SETUP
# ===========================
db_path = "nutriguide.db"
conn = sqlite3.connect(db_path, check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    gender TEXT,
    height REAL,
    weight REAL
)
""")
conn.commit()

# ===========================
# BACKGROUND IMAGE
# ===========================
def set_background(image_path):
    if not os.path.exists(image_path):
        return
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            color: black;
        }}
        .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div>div {{
            color: black;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ===========================
# BMI FUNCTION
# ===========================
def calculate_bmi(weight, height):
    return round(weight / ((height / 100) ** 2), 1)

# ===========================
# STREAMLIT APP
# ===========================
set_background("assets/bg.png")  # Make sure bg.png exists in assets folder

st.title("🥗 NutriGuide Health Dashboard")

# --- USER DETAILS ---
st.subheader("Enter Your Details")
with st.form("user_form"):
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, max_value=120)
    gender = st.selectbox("Gender", ["Male", "Female"])
    height = st.number_input("Height (cm)", min_value=50, max_value=250)
    weight = st.number_input("Weight (kg)", min_value=10, max_value=300)
    submitted = st.form_submit_button("OK")

if submitted:
    # Add to DB
    cursor.execute(
        "INSERT INTO users (name, age, gender, height, weight) VALUES (?, ?, ?, ?, ?)",
        (name, age, gender, height, weight)
    )
    conn.commit()
    st.success(f"Welcome, {name} 👋")

    # --- DASHBOARD SELECTION ---
    st.markdown("## 📊 Dashboard")
    main_option = st.selectbox(
        "Choose what to see:",
        ["Professional Diet Plan", "Professional Exercise Plan", "Water Intake", "BMI & Summary", "Health Tips"]
    )

    # --- SUB-DASHBOARD CONTENT ---
    if main_option == "Professional Diet Plan":
        st.subheader("Balanced Diet Recommendation")
        st.write("""
        A balanced diet should include carbohydrates for energy,
        high-quality protein for muscle repair, healthy fats for hormonal balance,
        and sufficient vitamins and minerals. Focus on vegetables, fruits, whole
        grains, lean proteins, and healthy fats. Limit processed foods and added sugars.
        """)

    elif main_option == "Professional Exercise Plan":
        st.subheader("Exercise Recommendation")
        st.write("""
        Include cardiovascular exercises to improve heart health, strength training
        to build muscle, and flexibility exercises to reduce injury risk. 
        Aim for 30–45 minutes of physical activity per day.
        """)

    elif main_option == "Water Intake":
        st.subheader("Water Intake Recommendation")
        water = round(weight * 0.035, 2)
        st.write(f"Based on your weight, your daily water intake should be **{water} liters**.")

    elif main_option == "BMI & Summary":
        st.subheader("BMI & Health Summary")
        bmi = calculate_bmi(weight, height)
        if bmi < 18.5:
            status = "Underweight"
        elif bmi < 25:
            status = "Normal weight"
        elif bmi < 30:
            status = "Overweight"
        else:
            status = "Obese"
        st.write(f"Your BMI is **{bmi}** → **{status}**")
        st.write("""
        Consider a healthy diet, regular exercise, and hydration to maintain optimal health.
        """)

    elif main_option == "Health Tips":
        st.subheader("Professional Health Tips")
        st.write("""
        • Maintain 7–9 hours of sleep per night  
        • Engage in regular physical activity  
        • Eat a balanced and nutritious diet  
        • Stay hydrated throughout the day  
        • Manage stress with meditation or relaxation techniques  
        • Attend regular health check-ups
        """)

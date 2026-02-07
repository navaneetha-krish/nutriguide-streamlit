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

# Create users table if not exists
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
        .stRadio>div>label, .stButton>button {{
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
    # Insert user into database
    cursor.execute(
        "INSERT INTO users (name, age, gender, height, weight) VALUES (?, ?, ?, ?, ?)",
        (name, age, gender, height, weight)
    )
    conn.commit()
    st.success(f"Welcome, {name} 👋")

    # --- DASHBOARD ---
    st.markdown("## 📊 Dashboard")
    dashboard_option = st.radio(
        "Select what you want to see:",
        ["Professional Diet Plan", "Professional Exercise Plan", "Water Intake", "BMI & Summary", "Health Tips"]
    )

    # --- CONTENT BASED ON SELECTION ---
    if dashboard_option == "Professional Diet Plan":
        st.subheader("Balanced Diet Recommendation")
        st.write("""
        A balanced diet provides energy and nutrients for your body. Include:
        - Carbohydrates for energy (rice, oats, bread)  
        - Protein for muscle repair (eggs, chicken, lentils)  
        - Healthy fats (nuts, olive oil)  
        - Vitamins and minerals from fruits and vegetables  

        Limit processed foods, sugary drinks, and snacks. Eat 4–5 small meals daily for consistent energy.
        """)

    elif dashboard_option == "Professional Exercise Plan":
        st.subheader("Exercise Recommendation")
        st.write("""
        For overall fitness, follow this plan:  
        - **Cardio**: 20–30 min of walking, running, cycling daily  
        - **Strength training**: 2–3 sessions/week focusing on major muscles  
        - **Flexibility**: Stretching 5–10 min after workouts  
        - **Rest**: Ensure at least 1 rest day per week  

        Always warm up before exercise and cool down afterward.
        """)

    elif dashboard_option == "Water Intake":
        st.subheader("Daily Water Intake")
        recommended_water = round(weight * 0.035, 2)
        st.write(f"Based on your weight, drink about **{recommended_water} liters** per day.")
        st.write("Tips: Carry a water bottle, drink before meals, and avoid sugary drinks.")

    elif dashboard_option == "BMI & Summary":
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
        st.write(f"Your BMI is **{bmi}**, which indicates **{status}**.")
        st.write("""
        Maintaining a healthy BMI requires a balanced diet, regular exercise, and proper hydration.
        Monitor your weight weekly and adjust your lifestyle for optimal health.
        """)

    elif dashboard_option == "Health Tips":
        st.subheader("Professional Health Tips")
        st.write("""
        • Sleep 7–9 hours per night  
        • Exercise regularly  
        • Eat a nutritious diet  
        • Stay hydrated  
        • Reduce stress through meditation or hobbies  
        • Regular medical check-ups
        """)

st.markdown("---")
st.caption("Database: nutriguide.db (users saved automatically)")

import streamlit as st
import sqlite3
import os
import base64

# ===========================
# DATABASE SETUP
# ===========================
conn = sqlite3.connect("nutriguide.db", check_same_thread=False)
cursor = conn.cursor()

# Create users table
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
# BACKGROUND IMAGE FUNCTION
# ===========================
def set_background(image_path):
    if not os.path.exists(image_path):
        return  # avoid crash if image missing

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
        }}
        .css-18e3th9 {{
            color: brown !important;
        }}
        .css-1d391kg {{
            color: brown !important;
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
set_background("assets/bg.png")  # make sure this path exists

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

if submitted and name != "":
    # Save user to database
    cursor.execute(
        "INSERT INTO users (name, age, gender, height, weight) VALUES (?, ?, ?, ?, ?)",
        (name, age, gender, height, weight)
    )
    conn.commit()
    st.success(f"Welcome, {name} 👋")

    # --- DASHBOARD OPTIONS ---
    st.markdown("## 📊 Dashboard")
    option = st.radio(
        "Select what you want to see:",
        [
            "🥗 Professional Diet Plan",
            "🏃 Professional Exercise Plan",
            "💧 Water Intake Recommendation",
            "📈 BMI & Health Summary",
            "🩺 Professional Health Tips"
        ]
    )

    # --- PROFESSIONAL DIET PLAN ---
    if option == "🥗 Professional Diet Plan":
        st.subheader("Balanced Diet Recommendation")
        st.write("""
        A balanced diet should include adequate carbohydrates for energy,
        high-quality protein for muscle repair, healthy fats for hormonal
        balance, and sufficient vitamins and minerals for overall body
        function. Prioritize whole foods such as vegetables, fruits, whole
        grains, lean proteins, and healthy fats while limiting processed
        foods and added sugars.
        """)

    # --- PROFESSIONAL EXERCISE PLAN ---
    elif option == "🏃 Professional Exercise Plan":
        st.subheader("Exercise Recommendation")
        st.write("""
        **Daily Exercise Routine:**  
        • 20–30 min brisk walking or jogging (Cardio)  
        • 15–20 min strength training (push-ups, squats, lunges)  
        • 10 min stretching/flexibility exercises  
        • 5–10 min core exercises (plank, crunches)  

        Consistency is key. Repeat daily or at least 5 days/week.
        """)

    # --- WATER INTAKE RECOMMENDATION ---
    elif option == "💧 Water Intake Recommendation":
        water = round(weight * 0.035, 2)
        st.subheader("Daily Water Intake")
        st.write(f"Based on your body weight, your recommended daily water intake is **{water} liters per day**. Adequate hydration supports digestion, circulation, and metabolic health.")

    # --- BMI & SUMMARY ---
    elif option == "📈 BMI & Health Summary":
        bmi = calculate_bmi(weight, height)
        st.subheader("BMI Analysis")
        st.write(f"Your Body Mass Index (BMI) is **{bmi}**.")
        if bmi < 18.5:
            status = "Underweight"
        elif bmi < 25:
            status = "Normal weight"
        elif bmi < 30:
            status = "Overweight"
        else:
            status = "Obese"
        st.write(f"This BMI indicates **{status}**. Consider lifestyle, diet, and exercise for optimal health.")
        st.write("""
        **Health Summary:**  
        Maintain a balanced diet, regular exercise, proper hydration, and adequate sleep. Track your weight and BMI regularly to monitor progress.
        """)

    # --- PROFESSIONAL HEALTH TIPS ---
    elif option == "🩺 Professional Health Tips":
        st.subheader("Health Improvement Tips")
        st.write("""
        • Maintain a consistent sleep schedule of 7–9 hours per night  
        • Engage in regular physical activity  
        • Consume a balanced and nutritious diet  
        • Stay adequately hydrated throughout the day  
        • Manage stress through relaxation techniques such as meditation  
        • Attend regular health check-ups  
        • Limit processed foods, sugar, and excessive salt  
        • Maintain a positive mindset and mental well-being
        """)

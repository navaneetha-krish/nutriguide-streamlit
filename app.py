import streamlit as st
import sqlite3
import os
import base64

# ===========================
# DATABASE SETUP
# ===========================
db_path = "nutriguide.db"  # database in same folder
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
# BACKGROUND IMAGE FUNCTION
# ===========================
def set_background(image_path):
    if not os.path.exists(image_path):
        st.warning("Background image not found! Put bg.png in assets folder.")
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
            color: white;
        }}
        .stTextInput>div>div>input,
        .stNumberInput>div>div>input,
        .stSelectbox>div>div>div {{
            color: white !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ===========================
# BMI FUNCTION
# ===========================
def calculate_bmi(weight, height):
    return round(weight / ((height/100) ** 2), 1)

# ===========================
# MAIN APP
# ===========================

# Add background
set_background("assets/bg.png")

st.title("🥗 NutriGuide Health Dashboard")

# --- USER FORM ---
if "submitted" not in st.session_state:
    with st.form("user_form"):
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1, max_value=120)
        gender = st.selectbox("Gender", ["Male", "Female"])
        height = st.number_input("Height (cm)", min_value=50, max_value=250)
        weight = st.number_input("Weight (kg)", min_value=10, max_value=300)
        submit = st.form_submit_button("Submit")

        if submit:
            cursor.execute("INSERT INTO users (name, age, gender, height, weight) VALUES (?, ?, ?, ?, ?)",
                           (name, age, gender, height, weight))
            conn.commit()
            st.success(f"Welcome, {name}! Dashboard is loading...")
            st.session_state.submitted = True
            st.session_state.user_id = cursor.lastrowid
            st.experimental_rerun()

# --- DASHBOARD ---
else:
    user = cursor.execute("SELECT * FROM users WHERE id=?", (st.session_state.user_id,)).fetchone()
    if user:
        st.subheader(f"Welcome, {user[1]} 👋")
        st.markdown("## 📊 Dashboard")

        option = st.selectbox(
            "Select an option:",
            [
                "🥗 Professional Diet Plan",
                "🏃 Professional Exercise Plan",
                "💧 Water Intake Recommendation",
                "📈 BMI & Health Summary",
                "🩺 Professional Health Tips"
            ]
        )

        if option == "🥗 Professional Diet Plan":
            st.subheader("Balanced Diet")
            st.write("""
            Include vegetables, fruits, whole grains, lean proteins, and healthy fats.
            Avoid too much sugar and processed foods.
            """)

        elif option == "🏃 Professional Exercise Plan":
            st.subheader("Exercise Plan")
            st.write("""
            30-45 min daily: cardio, strength, and flexibility exercises.
            """)

        elif option == "💧 Water Intake Recommendation":
            water = round(user[5]*0.035,2)
            st.subheader("Water Intake")
            st.write(f"Recommended daily water intake: **{water} liters**.")

        elif option == "📈 BMI & Health Summary":
            bmi = calculate_bmi(user[5], user[4])
            st.subheader("BMI Analysis")
            st.write(f"Your BMI is **{bmi}**.")
            if bmi < 18.5:
                status = "Underweight"
            elif bmi < 25:
                status = "Normal"
            elif bmi < 30:
                status = "Overweight"
            else:
                status = "Obese"
            st.write(f"This indicates **{status}**.")

        elif option == "🩺 Professional Health Tips":
            st.subheader("Health Tips")
            st.write("""
            • Sleep 7–9 hours  
            • Exercise regularly  
            • Eat a balanced diet  
            • Drink enough water  
            • Manage stress  
            • Regular health check-ups
            """)

        # View database
        if st.checkbox("Show all users in database"):
            users = cursor.execute("SELECT * FROM users").fetchall()
            st.write(users)

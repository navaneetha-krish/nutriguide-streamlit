import streamlit as st
import sqlite3
import os
import base64

# ===========================
# DATABASE SETUP
# ===========================
# DB will be created in same folder as app.py
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
        .stTextInput>div>div>input,
        .stNumberInput>div>div>input,
        .stSelectbox>div>div>div,
        .stButton>button,
        .stMarkdown,
        .stHeader,
        .stSubheader,
        .stRadio>div>label {{
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
# APP
# ===========================
# Set your background image path
set_background("assets/bg.png")  # Make sure this exists

st.title("🥗 NutriGuide Health Dashboard")

# --- USER DETAILS PAGE ---
if "user_submitted" not in st.session_state:
    st.subheader("Enter Your Details")
    with st.form("user_form"):
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1, max_value=120)
        gender = st.selectbox("Gender", ["Male", "Female"])
        height = st.number_input("Height (cm)", min_value=50, max_value=250)
        weight = st.number_input("Weight (kg)", min_value=10, max_value=300)
        submitted = st.form_submit_button("Submit")

    if submitted:
        cursor.execute("INSERT INTO users (name, age, gender, height, weight) VALUES (?, ?, ?, ?, ?)",
                       (name, age, gender, height, weight))
        conn.commit()
        st.success(f"Welcome, {name} 👋")
        st.session_state.user_submitted = True
        st.session_state.user_id = cursor.lastrowid
        st.experimental_rerun()  # Move to dashboard

# --- DASHBOARD PAGE ---
else:
    # Fetch user info from DB
    user = cursor.execute("SELECT * FROM users WHERE id=?", (st.session_state.user_id,)).fetchone()
    if user:
        st.subheader(f"Welcome, {user[1]} 👋")
        st.markdown("## 📊 Dashboard Options")

        # Buttons for selection instead of radio (more reliable)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🥗 Diet Plan"):
                st.subheader("Balanced Diet Recommendation")
                st.write("""
                A balanced diet should include adequate carbohydrates for energy,
                high-quality protein for muscle repair, healthy fats for hormonal
                balance, and sufficient vitamins and minerals for overall body
                function. Prioritize whole foods such as vegetables, fruits, whole
                grains, lean proteins, and healthy fats while limiting processed
                foods and added sugars.
                """)

            if st.button("💧 Water Intake"):
                water = round(user[5] * 0.035, 2)
                st.subheader("Daily Water Intake")
                st.write(f"Recommended daily water intake: **{water} liters**. Adequate hydration supports digestion, circulation, and metabolism.")

        with col2:
            if st.button("🏃 Exercise Plan"):
                st.subheader("Exercise Recommendation")
                st.write("""
                A well-structured fitness routine should include cardiovascular
                exercises, strength training, and flexibility exercises.
                At least 30–45 minutes of daily physical activity is recommended.
                """)

            if st.button("📈 BMI & Summary"):
                bmi = calculate_bmi(user[5], user[4])
                st.subheader("BMI Analysis & Health Summary")
                st.write(f"Your BMI is **{bmi}**.")
                if bmi < 18.5:
                    status = "Underweight"
                elif bmi < 25:
                    status = "Normal weight"
                elif bmi < 30:
                    status = "Overweight"
                else:
                    status = "Obese"
                st.write(f"This BMI indicates **{status}**. Adjust lifestyle, diet, and exercise for optimal health.")

            if st.button("🩺 Health Tips"):
                st.subheader("Professional Health Tips")
                st.write("""
                • Maintain a consistent sleep schedule of 7–9 hours  
                • Engage in regular physical activity  
                • Consume a balanced and nutritious diet  
                • Stay hydrated throughout the day  
                • Manage stress with meditation or relaxation  
                • Attend regular health check-ups
                """)

        # Option to view database (for debugging / checking users)
        if st.checkbox("Show all users in database"):
            users = cursor.execute("SELECT * FROM users").fetchall()
            st.write(users)

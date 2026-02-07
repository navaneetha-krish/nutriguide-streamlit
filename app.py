import streamlit as st
import sqlite3
from datetime import datetime
import base64

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="NutriGuide Health System",
    page_icon="🥗",
    layout="centered"
)

# -------------------- BACKGROUND --------------------
def set_background(image_path):
    with open(image_path, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background("assets/bg.png")

# -------------------- DATABASE --------------------
conn = sqlite3.connect("nutriguide.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    gender TEXT,
    height REAL,
    weight REAL,
    created_at TEXT
)
""")
conn.commit()

# -------------------- HEALTH LOGIC --------------------
def calculate_bmi(weight, height):
    return round(weight / ((height / 100) ** 2), 1)

def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def diet_plan(bmi):
    if bmi < 18.5:
        return (
            "The individual requires a calorie-dense and nutrient-rich diet to support "
            "healthy weight gain. Daily intake should include two glasses of milk, two eggs, "
            "adequate portions of rice or whole grains, healthy fats such as nuts and seeds, "
            "and frequent balanced meals to improve muscle mass and overall strength."
        )
    elif bmi < 25:
        return (
            "A balanced diet is recommended to maintain optimal health. Meals should consist "
            "of whole grains, lean protein sources, fresh vegetables, fruits, and adequate water. "
            "Processed foods and excess sugar should be limited to maintain a stable BMI."
        )
    else:
        return (
            "A controlled calorie diet focusing on vegetables, lean proteins, and whole foods "
            "is advised. Fried foods, sugary beverages, and excessive carbohydrates should be "
            "avoided. Portion control and hydration play a crucial role in gradual weight reduction."
        )

def exercise_plan(bmi):
    if bmi < 18.5:
        return (
            "Light strength-based exercises are recommended to promote muscle growth. "
            "This includes body-weight squats (3 sets of 10), wall push-ups (3 sets of 8), "
            "and a daily 20-minute walk to improve appetite and circulation."
        )
    elif bmi < 25:
        return (
            "A combination of cardiovascular and flexibility exercises is ideal. "
            "Jogging or brisk walking for 20 minutes, yoga for flexibility, "
            "and planks (3 sets of 30 seconds) help maintain physical fitness."
        )
    else:
        return (
            "Low-impact cardiovascular exercises are recommended for safe weight management. "
            "Walking for 30 minutes, cycling for 20 minutes, and daily stretching exercises "
            "help improve metabolism without excessive strain."
        )

# -------------------- USER INPUT PAGE --------------------
st.title("🥗 NutriGuide Health System")
st.subheader("Enter Your Health Details")

with st.form("user_form"):
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, max_value=100)
    gender = st.selectbox("Gender", ["Male", "Female"])
    height = st.number_input("Height (cm)", min_value=100, max_value=250)
    weight = st.number_input("Weight (kg)", min_value=20, max_value=200)
    submit = st.form_submit_button("Proceed to Dashboard")

if submit:
    cursor.execute(
        "INSERT INTO users VALUES (NULL,?,?,?,?,?,?)",
        (name, age, gender, height, weight, datetime.now().strftime("%Y-%m-%d %H:%M"))
    )
    conn.commit()
    st.session_state.user = (name, age, gender, height, weight)

# -------------------- DASHBOARD --------------------
if "user" in st.session_state:
    name, age, gender, height, weight = st.session_state.user
    bmi = calculate_bmi(weight, height)

    st.markdown("---")
    st.header(f"Welcome, {name} 👋")

    st.subheader("📊 BMI Analysis")
    st.write(
        f"Based on the provided height and weight, your Body Mass Index (BMI) is **{bmi}**, "
        f"which falls under the **{bmi_category(bmi)}** category. BMI is a useful indicator "
        f"to assess whether an individual maintains a healthy body weight relative to height."
    )

    st.subheader("🥗 Diet Recommendation")
    st.write(diet_plan(bmi))

    st.subheader("🏋️ Exercise Recommendation")
    st.write(exercise_plan(bmi))

    st.subheader("💧 Water Intake Guidance")
    st.write(
        "It is recommended to consume approximately **2.5 to 3 liters of water per day**. "
        "Adequate hydration supports digestion, circulation, and overall metabolic health."
    )

    st.subheader("🧠 Overall Health Summary")
    st.write(
        "This health assessment provides a structured overview of the user’s physical condition "
        "based on BMI evaluation. By following the recommended diet, exercise routine, and water "
        "intake guidelines, individuals can gradually improve or maintain their overall health. "
        "Consistency, adequate sleep, and stress management are essential components of a healthy lifestyle."
    )

    st.subheader("🗄️ Stored User Records")
    cursor.execute("SELECT name, age, gender, height, weight, created_at FROM users")
    st.table(cursor.fetchall())

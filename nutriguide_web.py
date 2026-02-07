import streamlit as st
import sqlite3
from datetime import datetime

# ===== Database Setup =====
conn = sqlite3.connect("health.db", check_same_thread=False)
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    gender TEXT,
    height REAL,
    weight REAL,
    created_at TEXT
)""")
conn.commit()

# ===== Helper Functions =====
def calculate_bmi(weight, height):
    return round(weight / ((height / 100) ** 2), 1)

def bmi_category(bmi):
    if bmi < 18.5: return "Underweight"
    elif 18.5 <= bmi < 24.9: return "Normal weight"
    elif 25 <= bmi < 29.9: return "Overweight"
    else: return "Obese"

def diet_plan(bmi):
    if bmi < 18.5:
        return ["Breakfast: 2 eggs + 2 slices whole grain bread",
                "Lunch: Chicken 150g + Brown Rice 100g + Vegetables",
                "Snack: Milk 250ml + Nuts 30g"]
    elif bmi < 24.9:
        return ["Balanced meals: Protein, Carbs, Fats",
                "Vegetables + Fruits daily",
                "Avoid junk foods"]
    elif bmi < 29.9:
        return ["Vegetables + Fruits focus",
                "Reduce fried/sugary foods",
                "Moderate protein"]
    else:
        return ["Consult doctor for personalized diet"]

def exercise_plan(bmi):
    if bmi < 18.5:
        return ["Light weights: 3 sets x 12 reps", "Yoga 30 mins", "Walking 30 mins"]
    elif bmi < 24.9:
        return ["Running 20-30 mins", "Bodyweight exercises: 3 sets x 15 reps", "Yoga 20 mins"]
    elif bmi < 29.9:
        return ["Cardio 30 mins", "Strength training 2-3x/week", "Swimming"]
    else:
        return ["Low impact cardio 20 mins", "Walking 30 mins", "Consult trainer"]

# ===== Streamlit App =====
st.set_page_config(page_title="NutriGuide", layout="centered")

# ----- Page 1: User Info -----
st.title("NutriGuide Web App")
if 'user_id' not in st.session_state:
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, max_value=120)
    gender = st.radio("Gender", ("Male", "Female"))
    height = st.number_input("Height (cm)", min_value=50, max_value=250)
    weight = st.number_input("Weight (kg)", min_value=10, max_value=300)
    
    if st.button("OK"):
        c.execute("INSERT INTO users (name, age, gender, height, weight, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                  (name, age, gender, height, weight, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        st.session_state.user_id = c.lastrowid
        st.session_state.name = name
        st.success("✅ Profile created! Go to Dashboard below 👇")

# ----- Page 2: Dashboard -----
if 'user_id' in st.session_state:
    st.header(f"Hello {st.session_state.name}, Your Health Dashboard")
    option = st.selectbox("Select an option", 
                          ["BMI Report", "Diet Recommendation", "Exercise Recommendation", "Water Intake", "Health Tips"])

    # Load user info from DB
    c.execute("SELECT height, weight FROM users WHERE id=?", (st.session_state.user_id,))
    user = c.fetchone()
    height, weight = user
    bmi_val = calculate_bmi(weight, height)
    bmi_cat = bmi_category(bmi_val)

    if option == "BMI Report":
        st.subheader("BMI Report")
        st.write(f"BMI: {bmi_val} ({bmi_cat})")

    elif option == "Diet Recommendation":
        st.subheader("Diet Plan")
        for item in diet_plan(bmi_val):
            st.write(f"🍽️ {item}")

    elif option == "Exercise Recommendation":
        st.subheader("Exercise Plan")
        for ex in exercise_plan(bmi_val):
            st.write(f"🏋️ {ex}")

    elif option == "Water Intake":
        st.subheader("Water Intake")
        st.write(f"💧 Suggested: {round(weight*0.033,1)} L/day")

    elif option == "Health Tips":
        st.subheader("Health Tips")
        st.write("🛌 Sleep 7-9 hours daily")
        st.write("🥦 Eat more vegetables and fruits")
        st.write("🏃 Exercise regularly")
        st.write("💧 Drink water frequently")

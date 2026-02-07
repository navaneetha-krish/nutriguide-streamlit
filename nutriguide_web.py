import streamlit as st
import sqlite3
from datetime import datetime
from PIL import Image

# ===== Database Setup =====
conn = sqlite3.connect("health.db")
c = conn.cursor()

c.execute("""
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

c.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    date TEXT,
    weight REAL,
    calories REAL,
    steps INTEGER,
    water REAL,
    exercise TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")
conn.commit()

# ===== Helper Functions =====

def calculate_bmi(weight, height):
    return round(weight / ((height/100) ** 2), 1)

def bmi_category(bmi):
    if bmi < 18.5: return "Underweight"
    elif bmi < 24.9: return "Normal weight"
    elif bmi < 29.9: return "Overweight"
    else: return "Obese"

def diet_recommendation(bmi):
    if bmi < 18.5:
        return {
            "Breakfast": "2 eggs, 1 glass milk, 1 banana",
            "Lunch": "150g chicken, 100g rice, vegetables",
            "Snack": "Nuts 30g, Yogurt 100g",
            "Dinner": "150g fish, 100g potatoes, salad"
        }
    elif bmi < 24.9:
        return {
            "Breakfast": "Oatmeal 50g, milk 1 glass, fruit",
            "Lunch": "100g chicken, 100g rice, vegetables",
            "Snack": "Fruit or nuts 30g",
            "Dinner": "Grilled fish 100g, vegetables, 50g rice"
        }
    elif bmi < 29.9:
        return {
            "Breakfast": "1 boiled egg, fruit",
            "Lunch": "Vegetables salad, 50g rice, 100g protein",
            "Snack": "Fruit or low-fat yogurt",
            "Dinner": "Vegetables, 100g grilled chicken/fish"
        }
    else:
        return {
            "Breakfast": "Vegetable smoothie",
            "Lunch": "Salad, lean protein 100g",
            "Snack": "Fruits, no sugar",
            "Dinner": "Steamed vegetables, protein 100g"
        }

def exercise_plan(bmi):
    if bmi < 18.5:
        return ["Light weight training: 3 sets x 10 reps", "Yoga: 20 min", "Walking: 30 min"]
    elif bmi < 24.9:
        return ["Running: 20-30 min", "Bodyweight exercises: 3 sets x 15 reps", "Yoga: 20 min"]
    elif bmi < 29.9:
        return ["Cardio: 30 min", "Strength training: 3 sets x 12 reps", "Swimming: 30 min"]
    else:
        return ["Low impact cardio: 30 min", "Walking: 30 min", "Consult trainer"]

def health_tips():
    return [
        "Sleep 7-9 hours per day",
        "Drink enough water daily",
        "Include fruits and vegetables",
        "Exercise regularly",
        "Avoid processed foods"
    ]

def add_user(name, age, gender, height, weight):
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO users (name, age, gender, height, weight, created_at) VALUES (?,?,?,?,?,?)",
              (name, age, gender, height, weight, created_at))
    conn.commit()

def get_user(user_id):
    c.execute("SELECT * FROM users WHERE id=?", (user_id,))
    return c.fetchone()

# ===== Streamlit App =====

st.set_page_config(page_title="NutriGuide Dashboard", layout="wide")

# Load Background
try:
    bg_image = Image.open("background.png")
    st.image(bg_image, use_column_width=True)
except:
    pass

st.title("🥗 NutriGuide Health Dashboard")

# ---- Step 1: Enter User Info ----
if "step" not in st.session_state:
    st.session_state.step = 1

if st.session_state.step == 1:
    st.subheader("Enter Your Details")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=5, max_value=100)
    gender = st.selectbox("Gender", ["Male", "Female"])
    height = st.number_input("Height (cm)", min_value=50, max_value=250)
    weight = st.number_input("Weight (kg)", min_value=10, max_value=200)
    if st.button("Submit"):
        if name != "":
            add_user(name, age, gender, height, weight)
            st.session_state.user_id = c.lastrowid
            st.session_state.step = 2
        else:
            st.error("Please enter your name!")

# ---- Step 2: Dashboard ----
if st.session_state.step == 2:
    st.subheader(f"Welcome, {name} 👋")
    menu = ["BMI Report","Diet Recommendation","Exercise Recommendation","Water Intake","Weekly Summary","Health Tips"]
    choice = st.sidebar.selectbox("Select Option", menu)

    user = get_user(st.session_state.user_id)
    bmi = calculate_bmi(user[5], user[6])
    bmi_cat = bmi_category(bmi)

    if choice == "BMI Report":
        st.markdown(f"**BMI:** {bmi}")
        st.markdown(f"**Category:** {bmi_cat}")
        st.markdown("**Advice:** Follow professional diet and exercise plans for your BMI.")
    
    elif choice == "Diet Recommendation":
        st.markdown("### 🥗 Professional Diet Plan")
        diet = diet_recommendation(bmi)
        for meal, plan in diet.items():
            st.markdown(f"**{meal}:** {plan}")
    
    elif choice == "Exercise Recommendation":
        st.markdown("### 🏋️ Professional Exercise Plan")
        exercises = exercise_plan(bmi)
        try:
            ex_img = Image.open("exercise.png")
            st.image(ex_img, caption="Exercise Examples", use_column_width=True)
        except:
            pass
        for e in exercises:
            st.markdown(f"- {e}")

    elif choice == "Water Intake":
        recommended = 2.5 if gender=="Male" else 2.0
        st.markdown(f"💧 Recommended Water Intake: **{recommended} L/day**")
        st.markdown("- Spread intake through the day")
        st.markdown("- Avoid sugary drinks")

    elif choice == "Weekly Summary":
        st.markdown("### 📊 Weekly Health Summary")
        c.execute("SELECT date, weight FROM logs WHERE user_id=? ORDER BY date DESC LIMIT 7", (user[0],))
        data = c.fetchall()
        if data:
            for row in data:
                st.markdown(f"- {row[0]}: Weight {row[1]} kg")
        else:
            st.info("No weekly logs found.")

    elif choice == "Health Tips":
        st.markdown("### 💡 Health Tips")
        tips = health_tips()
        for t in tips:
            st.markdown(f"- {t}")

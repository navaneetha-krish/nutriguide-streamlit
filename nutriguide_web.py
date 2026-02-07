import streamlit as st
import sqlite3
from datetime import datetime
from PIL import Image

# ===== Database Setup =====
conn = sqlite3.connect("nutriguide.db", check_same_thread=False)
cursor = conn.cursor()

# Create Users table
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

# ===== Helper Functions =====
def calculate_bmi(weight, height):
    return round(weight / ((height / 100) ** 2), 1)

def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 24.9:
        return "Normal weight"
    elif bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

def health_suggestions(bmi, age):
    suggestions = []
    if bmi < 18.5:
        suggestions.append("Increase calorie intake with protein-rich foods like eggs, milk, nuts.")
    elif bmi < 24.9:
        suggestions.append("Maintain a balanced diet and regular exercise.")
    elif bmi < 29.9:
        suggestions.append("Reduce high-calorie foods and do 30 mins of exercise daily.")
    else:
        suggestions.append("Consult a doctor and follow a structured diet and exercise plan.")

    if age < 18:
        suggestions.append("Sleep 8-10 hours for proper growth.")

    return suggestions

def exercise_plan(bmi):
    if bmi < 18.5:
        return ["Light weight training: 3x/week", "Yoga: 20 mins daily", "Walking: 30 mins"]
    elif bmi < 24.9:
        return ["Running: 20-30 mins daily", "Bodyweight exercises: 3x/week", "Yoga: 15 mins"]
    elif bmi < 29.9:
        return ["Cardio: 30 mins daily", "Strength training: 3x/week", "Swimming: 2x/week"]
    else:
        return ["Low impact cardio: 20 mins", "Walking: 30 mins", "Consult a trainer"]

def diet_plan(bmi):
    if bmi < 18.5:
        return ["Breakfast: 2 eggs + milk", "Snack: 1 banana + nuts", "Lunch: Rice + chicken + vegetables", "Dinner: Fish + salad"]
    elif bmi < 24.9:
        return ["Breakfast: Oats + fruits", "Snack: Yogurt + almonds", "Lunch: Brown rice + lean meat + veggies", "Dinner: Salad + soup"]
    elif bmi < 29.9:
        return ["Breakfast: Oats + protein shake", "Snack: Fruits", "Lunch: Grilled chicken + salad", "Dinner: Steamed vegetables + fish"]
    else:
        return ["Consult dietitian for personalized plan"]

# ===== Streamlit App =====
# Set page config
st.set_page_config(page_title="NutriGuide", layout="centered")

# --- Background ---
def add_bg_image(image_file):
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("data:image/png;base64,{st.image_to_bytes(Image.open(image_file))}");
             background-size: cover;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_image("background.png")  # <-- your vertical PNG

# --- Main Page ---
st.title("🥗 NutriGuide Health Dashboard")
st.subheader("Enter Your Details")

# User Input Form
with st.form("user_form"):
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, max_value=120)
    gender = st.selectbox("Gender", ["Male", "Female"])
    height = st.number_input("Height (cm)", min_value=50, max_value=250)
    weight = st.number_input("Weight (kg)", min_value=10, max_value=200)
    submitted = st.form_submit_button("Submit")

if submitted:
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO users (name, age, gender, height, weight, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                   (name, age, gender, height, weight, created_at))
    conn.commit()
    st.success(f"Welcome, {name} 👋")

    # --- Dashboard ---
    st.header("Your Health Dashboard")

    bmi = calculate_bmi(weight, height)
    st.metric("BMI", bmi)
    st.write(f"Category: {bmi_category(bmi)}")

    # Professional Suggestions
    st.subheader("💡 Health Suggestions")
    for s in health_suggestions(bmi, age):
        st.write(f"- {s}")

    # Professional Exercise Plan
    st.subheader("🏋️ Exercise Plan")
    for e in exercise_plan(bmi):
        st.write(f"- {e}")
    st.image("exercise.png", caption="Professional Exercise Illustrations")

    # Professional Diet Plan
    st.subheader("🍎 Diet Plan")
    for d in diet_plan(bmi):
        st.write(f"- {d}")
    st.image("diet.png", caption="Professional Diet Illustrations")

    # Water Intake
    st.subheader("💧 Recommended Water Intake")
    water_intake = round(weight * 0.033, 2)
    st.write(f"Drink approximately {water_intake} liters of water daily.")

    # Health Tips
    st.subheader("📝 Health Tips")
    tips = [
        "Sleep 7-9 hours daily",
        "Avoid sugary drinks",
        "Include fruits and vegetables in every meal",
        "Exercise regularly",
        "Consult professionals if BMI is too high or low"
    ]
    for t in tips:
        st.write(f"- {t}")

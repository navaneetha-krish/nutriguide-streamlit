import streamlit as st
import sqlite3
import base64
import os

# ======================
# PAGE CONFIG
# ======================
st.set_page_config(page_title="NutriGuide", layout="centered")

# ======================
# BACKGROUND + FONT
# ======================
def set_background(image_path):
    if not os.path.exists(image_path):
        return
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            color: white;
        }}
        h1, h2, h3, p, label {{
            color: white !important;
        }}
        </style>
    """, unsafe_allow_html=True)

set_background("assets/bg.jpg")

# ======================
# DATABASE
# ======================
conn = sqlite3.connect("nutriguide.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    gender TEXT,
    height REAL,
    weight REAL
)
""")
conn.commit()

# ======================
# FUNCTIONS
# ======================
def calculate_bmi(weight, height):
    return round(weight / ((height / 100) ** 2), 1)

# ======================
# APP START
# ======================
st.title("🥗 NutriGuide Health Dashboard")

st.subheader("Enter Your Details")

with st.form("user_form"):
    name = st.text_input("Name")
    age = st.number_input("Age", 1, 120)
    gender = st.selectbox("Gender", ["Male", "Female"])
    height = st.number_input("Height (cm)", 100, 250)
    weight = st.number_input("Weight (kg)", 30, 200)
    submit = st.form_submit_button("Proceed")

if submit:
    cursor.execute(
        "INSERT INTO users (name, age, gender, height, weight) VALUES (?, ?, ?, ?, ?)",
        (name, age, gender, height, weight)
    )
    conn.commit()

    st.success(f"Welcome, {name} 👋")

    st.header("📊 Health Dashboard")

    option = st.selectbox(
        "Choose what you want to view",
        [
            "Professional Diet Plan",
            "Professional Exercise Plan",
            "Water Intake & Steps",
            "BMI & Health Summary",
            "Professional Health Tips",
            "Overall Performance Summary"
        ]
    )

    # ======================
    # DIET
    # ======================
    if option == "Professional Diet Plan":
        st.subheader("🥗 Daily Diet Recommendation")
        st.write("""
**Breakfast**
- Rice / Oats: 1 cup  
- Egg: 1–2  
- Fruit: 1 medium  

**Lunch**
- Rice: 1.5 cups  
- Vegetables: 1 cup  
- Fish / Chicken / Dhal: 100–120g  

**Dinner**
- Light meal (vegetables + protein)
- Avoid fried food  

**Why:**  
Provides energy, muscle repair, digestion support, and balanced nutrition.
""")

    # ======================
    # EXERCISE
    # ======================
    elif option == "Professional Exercise Plan":
        st.subheader("🏃 Exercise Routine")
        st.write("""
**Daily Exercises**
- Jumping Jacks: 3 sets × 20 reps  
- Squats: 3 sets × 15 reps  
- Push-ups: 3 sets × 10 reps  
- Plank: 3 × 30 seconds  

**Why:**  
Improves heart health, muscle strength, posture, and metabolism.
""")

    # ======================
    # WATER & STEPS
    # ======================
    elif option == "Water Intake & Steps":
        water = round(weight * 0.035, 2)
        st.subheader("💧 Hydration & Activity")
        st.write(f"""
**Water Intake**
- Recommended: **{water} litres/day**

**Steps**
- Target: **8,000 – 10,000 steps/day**

**Why:**  
Water aids digestion and skin health. Walking improves circulation and heart function.
""")

    # ======================
    # BMI
    # ======================
    elif option == "BMI & Health Summary":
        bmi = calculate_bmi(weight, height)
        st.subheader("📈 BMI Result")
        st.write(f"Your BMI is **{bmi}**")

        if bmi < 18.5:
            status = "Underweight"
        elif bmi < 25:
            status = "Normal"
        elif bmi < 30:
            status = "Overweight"
        else:
            status = "Obese"

        st.write(f"**Health Status:** {status}")

    # ======================
    # HEALTH TIPS
    # ======================
    elif option == "Professional Health Tips":
        st.subheader("🩺 Health Tips")
        st.write("""
• Sleep 7–9 hours daily  
• Eat on time  
• Avoid sugary drinks  
• Exercise regularly  
• Reduce screen time  
• Manage stress  
""")

    # ======================
    # OVERALL SUMMARY
    # ======================
    elif option == "Overall Performance Summary":
        st.subheader("📋 Overall Health Summary")
        st.write("""
Your health performance depends on consistent nutrition, daily physical activity,
proper hydration, and adequate rest. Maintaining a balanced lifestyle improves energy,
mental focus, immunity, and long-term well-being. Small daily habits lead to strong
long-term health outcomes.
""")

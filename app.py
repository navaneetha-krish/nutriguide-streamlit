import streamlit as st
import sqlite3
import os
import base64

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="NutriGuide",
    page_icon="🥗",
    layout="centered"
)

# =====================================
# BACKGROUND FUNCTION (SAFE)
# =====================================
def set_background(image_path):
    if os.path.exists(image_path):
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
                color: white;
            }}
            h1, h2, h3, p, label {{
                color: white !important;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

set_background("assets/bg.png")

# =====================================
# DATABASE SETUP (WORKING)
# =====================================
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

# =====================================
# HELPER FUNCTIONS
# =====================================
def calculate_bmi(weight, height):
    return round(weight / ((height / 100) ** 2), 1)

def bmi_status(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

# =====================================
# APP UI
# =====================================
st.title("🥗 NutriGuide Health Dashboard")
st.write("### Enter Your Health Details")

with st.form("user_form"):
    name = st.text_input("Name")
    age = st.number_input("Age", 1, 120)
    gender = st.selectbox("Gender", ["Male", "Female"])
    height = st.number_input("Height (cm)", 50, 250)
    weight = st.number_input("Weight (kg)", 10, 300)
    submit = st.form_submit_button("Proceed to Dashboard")

if submit:
    cursor.execute(
        "INSERT INTO users (name, age, gender, height, weight) VALUES (?, ?, ?, ?, ?)",
        (name, age, gender, height, weight)
    )
    conn.commit()

    st.success(f"Welcome {name} 👋")

    bmi = calculate_bmi(weight, height)
    status = bmi_status(bmi)
    water = round(weight * 0.035, 2)

    st.markdown("## 📊 Health Dashboard")

    dashboard_option = st.selectbox(
        "Choose a section",
        [
            "Diet Plan",
            "Exercise Plan",
            "Water & Steps",
            "BMI & Health Summary",
            "Professional Health Tips"
        ]
    )

    # ===========================
    # DIET PLAN
    # ===========================
    if dashboard_option == "Diet Plan":
        st.subheader("🥗 Clinical Diet Recommendation")
        st.write("""
**Breakfast**
• Whole grains (oats/rice): 1 cup  
• Eggs or milk/curd: 1–2 servings  
• Fruit: 1 portion  

**Lunch**
• Rice: 1.5 cups  
• Protein (fish/chicken/dhal): 100–120 g  
• Vegetables: 1 cup  

**Dinner**
• Light meal with vegetables and lean protein  

**Why this works:**  
Balances blood sugar, supports muscle health, improves digestion, and
prevents nutritional deficiencies.
""")

    # ===========================
    # EXERCISE PLAN
    # ===========================
    elif dashboard_option == "Exercise Plan":
        st.subheader("🏃 Professional Exercise Prescription")
        st.write("""
**Strength Training (3–4 days/week)**
• Squats: 3 sets × 15 reps  
• Push-ups: 3 × 10  
• Lunges: 3 × 12  

**Cardio**
• Brisk walking / cycling: 30–45 minutes daily  

**Flexibility**
• Stretching: 10 minutes  

**Medical benefit:**  
Improves heart health, muscle tone, bone density, and metabolism.
""")

    # ===========================
    # WATER & STEPS
    # ===========================
    elif dashboard_option == "Water & Steps":
        st.subheader("💧 Hydration & Activity Guidance")
        st.write(f"""
• Recommended water intake: **{water} litres/day**  
• Daily steps target: **8,000 – 10,000 steps**

**Reason:**  
Supports kidney function, circulation, joint health, and weight control.
""")

    # ===========================
    # BMI SUMMARY
    # ===========================
    elif dashboard_option == "BMI & Health Summary":
        st.subheader("📈 BMI & Medical Interpretation")
        st.write(f"""
• Your BMI: **{bmi}**  
• Category: **{status}**

**Clinical note:**  
BMI is a screening indicator of weight-related health risks.
Healthy lifestyle changes are advised for long-term wellness.
""")

    # ===========================
    # HEALTH TIPS
    # ===========================
    elif dashboard_option == "Professional Health Tips":
        st.subheader("🩺 Evidence-Based Health Tips")
        st.write("""
• Sleep 7–9 hours daily  
• Eat meals on time  
• Avoid excess sugar and junk food  
• Exercise consistently  
• Manage stress through breathing or meditation  
• Regular health check-ups  

**Overall Summary:**  
Consistent healthy habits significantly reduce chronic disease risk
and improve quality of life.
""")

import streamlit as st
import sqlite3
import os
import base64

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(page_title="NutriGuide", page_icon="🥗")

# ===============================
# BACKGROUND
# ===============================
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

# ===============================
# DATABASE
# ===============================
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

# ===============================
# FUNCTIONS
# ===============================
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

# ===============================
# SESSION STATE INIT
# ===============================
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# ===============================
# UI
# ===============================
st.title("🥗 NutriGuide Health Dashboard")

# -------- FORM --------
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

    st.session_state.submitted = True
    st.session_state.user = (name, age, gender, height, weight)

# -------- DASHBOARD --------
if st.session_state.submitted:
    name, age, gender, height, weight = st.session_state.user

    bmi = calculate_bmi(weight, height)
    status = bmi_status(bmi)
    water = round(weight * 0.035, 2)

    st.success(f"Welcome {name} 👋")
    st.markdown("## 📊 Health Dashboard")

    option = st.selectbox(
        "Choose what you want to view",
        [
            "Diet Plan",
            "Exercise Plan",
            "Water & Steps",
            "BMI & Health Summary",
            "Professional Health Tips"
        ]
    )

    if option == "Diet Plan":
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

    elif option == "Exercise Plan":
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

    elif option == "Water & Steps":
        st.subheader("💧 Hydration & Activity Guidance")
        st.write(f"""
• Recommended water intake: **{water} litres/day**  
• Daily steps target: **8,000 – 10,000 steps**

**Reason:**  
Supports kidney function, circulation, joint health, and weight control.
""")

    elif option == "BMI & Health Summary":
        st.subheader("📈 BMI & Medical Interpretation")
        st.write(f"""
• Your BMI: **{bmi}**  
• Category: **{status}**

**Clinical note:**  
BMI is a screening indicator of weight-related health risks.
Healthy lifestyle changes are advised for long-term wellness.
""")

    elif option == "Professional Health Tips":
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

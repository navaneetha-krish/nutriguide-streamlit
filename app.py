import streamlit as st
import sqlite3
import os
import base64

# ===========================
# DATABASE SETUP
# ===========================
# Database will be created automatically in same folder as app.py
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
            color: white;
        }}
        .stTextInput>div>div>input,
        .stNumberInput>div>div>input,
        .stSelectbox>div>div>div {{
            color: white;
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

# Add background image
set_background("assets/bg.png")  # make sure this exists in assets/

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

if submitted:
    # Insert user into database
    cursor.execute("INSERT INTO users (name, age, gender, height, weight) VALUES (?, ?, ?, ?, ?)",
                   (name, age, gender, height, weight))
    conn.commit()
    st.success(f"Welcome, {name} 👋")

    # --- DASHBOARD OPTIONS ---
    st.markdown("## 📊 Dashboard")
    option = st.selectbox(
        "Select what you want to see:",
        [
            "Professional Diet Plan",
            "Professional Exercise Plan",
            "Water Intake Recommendation",
            "BMI & Health Summary",
            "Professional Health Tips",
            "Database Preview"
        ]
    )

    # --- PROFESSIONAL DIET PLAN ---
    if option == "Professional Diet Plan":
        st.subheader("🥗 Balanced Diet Recommendation")
        st.write("""
**Breakfast:**  
- 2 boiled eggs or 100g paneer/tofu  
- 1 slice whole-grain toast or 50g oats  
- 1 glass milk or plant-based alternative  

**Lunch:**  
- 150g grilled chicken/fish/tofu  
- 1 cup cooked brown rice/quinoa  
- 1 cup vegetables (broccoli, spinach, carrot)  

**Snacks:**  
- 1 handful nuts (almonds, walnuts)  
- 1 fruit (apple, orange, banana)  

**Dinner:**  
- 100g lean protein (chicken/fish/tofu)  
- 1 cup steamed vegetables  
- 1 small portion complex carbs (sweet potato/rice)  

**Notes:**  
- Drink water between meals  
- Avoid sugary drinks and processed snacks  
- Maintain consistent meal timings for metabolism  
        """)

    # --- PROFESSIONAL EXERCISE PLAN ---
    elif option == "Professional Exercise Plan":
        st.subheader("🏃 Exercise Recommendations")
        st.write("""
**Warm-up:** 5–10 minutes light cardio (jogging, jumping jacks)  

**Strength & Cardio:**  
- Push-ups: 3 sets × 12 reps  
- Squats: 3 sets × 15 reps  
- Plank: 3 × 30 seconds hold  
- Lunges: 3 sets × 12 reps per leg  
- Jog or brisk walk: 20–30 minutes  

**Cool-down & Stretching:**  
- Hamstring stretch: 2 × 30 seconds per leg  
- Shoulder stretch: 2 × 30 seconds  
- Cat-cow yoga stretch: 2 × 10 reps  

**Frequency:** 5–6 days per week for optimal results
        """)

    # --- WATER INTAKE RECOMMENDATION ---
    elif option == "Water Intake Recommendation":
        water = round(weight * 0.035, 2)
        st.subheader("💧 Daily Water Intake")
        st.write(f"Based on your body weight ({weight} kg), your recommended daily water intake is **{water} liters**.")
        st.write("Hydration supports digestion, circulation, and overall metabolic health. Drink small amounts frequently rather than large amounts at once.")

    # --- BMI & HEALTH SUMMARY ---
    elif option == "BMI & Health Summary":
        bmi = calculate_bmi(weight, height)
        st.subheader("📈 BMI & Health Summary")
        st.write(f"Your BMI is **{bmi}**.")
        if bmi < 18.5:
            status = "Underweight"
            advice = "Increase calorie intake with balanced meals and include strength training."
        elif bmi < 25:
            status = "Normal weight"
            advice = "Maintain current lifestyle, balanced diet, and regular exercise."
        elif bmi < 30:
            status = "Overweight"
            advice = "Reduce calorie intake, include cardio and strength training."
        else:
            status = "Obese"
            advice = "Consult a healthcare provider, reduce calorie intake, and start gradual exercise."
        st.write(f"Status: **{status}**")
        st.write(f"Advice: {advice}")

    # --- PROFESSIONAL HEALTH TIPS ---
    elif option == "Professional Health Tips":
        st.subheader("🩺 Health Improvement Tips")
        st.write("""
- Sleep 7–9 hours per night consistently  
- Engage in daily physical activity  
- Follow a balanced, nutrient-rich diet  
- Drink enough water throughout the day  
- Manage stress with meditation or breathing exercises  
- Take regular health check-ups  
- Avoid smoking, excessive alcohol, and junk foods
        """)

    # --- DATABASE PREVIEW ---
    elif option == "Database Preview":
        st.subheader("🔍 Users Stored in Database")
        data = cursor.execute("SELECT * FROM users").fetchall()
        if data:
            st.table(data)
        else:
            st.write("No users found yet.")

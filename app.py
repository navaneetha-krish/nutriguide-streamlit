import streamlit as st
import sqlite3

st.set_page_config(page_title="NutriGuide", page_icon="🥗")

DB = "nutriguide.db"

def get_db():
    return sqlite3.connect(DB)

def calculate_bmi(w, h):
    return round(w / ((h/100)**2), 1)

def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def recommendation(bmi):
    if bmi < 18.5:
        return (
            "🍚 Rice 1.5 cups, 🥚 Eggs 2, 🥛 Milk 1 glass",
            "🏋️ Squats 3×10, Walking 20 min"
        )
    elif bmi < 25:
        return (
            "🍚 Rice 1 cup, 🥗 Veggies, 🐟 Fish",
            "🏃 Jogging 20 min, Plank 3×30 sec"
        )
    else:
        return (
            "🥗 Veggies, 🍎 Fruits, ❌ No junk",
            "🚶 Walking 30 min, Cycling 20 min"
        )

# DB setup
conn = get_db()
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    height REAL,
    weight REAL
)
""")
conn.commit()
conn.close()

st.title("🥗 NutriGuide Health App")

name = st.text_input("Name")
age = st.number_input("Age", min_value=5, max_value=100)
height = st.number_input("Height (cm)")
weight = st.number_input("Weight (kg)")

if st.button("Check Health"):
    bmi = calculate_bmi(weight, height)
    cat = bmi_category(bmi)
    diet, exercise = recommendation(bmi)

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (name, age, height, weight) VALUES (?, ?, ?, ?)",
        (name, age, height, weight)
    )
    conn.commit()
    conn.close()

    st.success(f"BMI: {bmi} ({cat})")
    st.subheader("🍽 Diet Suggestion")
    st.write(diet)
    st.subheader("🏃 Exercise Plan")
    st.write(exercise)

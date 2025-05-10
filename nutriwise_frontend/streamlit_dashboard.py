import streamlit as st
import requests
import datetime
import json
import time
import os

st.set_page_config(page_title="NutriWise AI", layout="wide")
st.title("🌱 NutriWise AI - Smart Meal Planner")

# ✅ Dynamic backend URL: falls back to localhost if not set
base_url = os.environ.get("API_BASE_URL", "http://localhost:5000")

# Feedback UI function moved to top
def evolving_ai_feedback_ui(plan):
    st.subheader("6. Provide Feedback to Improve Future Plans")
    with st.form("meal_feedback_form"):
        skipped = st.text_input("Skipped Items (comma separated)", placeholder="e.g., Tofu, Broccoli")
        disliked = st.text_input("Disliked Ingredients (comma separated)", placeholder="e.g., Banana")
        notes = st.text_area("Any Notes or Suggestions?", placeholder="E.g., too much fiber, prefer Indian breakfast")
        submitted_feedback = st.form_submit_button("Submit Feedback")

    if submitted_feedback:
        payload = {
            "username": st.session_state.username,
            "timestamp": plan["timestamp"],
            "skipped": skipped,
            "disliked": disliked,
            "notes": notes
        }
        res = requests.post(f"{base_url}/meal_feedback", json=payload)
        if res.status_code == 200:
            st.success("✅ Feedback submitted! AI will evolve accordingly.")
        else:
            st.error(f"Failed to submit feedback: {res.text}")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'page' not in st.session_state:
    st.session_state.page = "Register"
if 'meal_plans' not in st.session_state:
    st.session_state.meal_plans = []

# ---------- PAGE NAVIGATION WITHOUT SIDEBAR ----------
if st.session_state.page == "Register":
    st.subheader("Register")
    username = st.text_input("Choose a Username")
    password = st.text_input("Choose a Password", type="password")

    if st.button("Register"):
        try:
            response = requests.post(f"{base_url}/register", json={"username": username, "password": password})
            if response.status_code == 200:
                st.success("Registration successful! Please log in.")
                st.session_state.page = "Login"
                time.sleep(1.5)
                st.rerun()
            elif response.status_code == 409:
                st.warning("Username already exists. Redirecting to login...")
                st.session_state.page = "Login"
                time.sleep(1.5)
                st.rerun()
            else:
                msg = response.json().get('message', 'Unknown error') if response.content else 'Empty server response'
                st.error(f"Registration failed: {msg}")
        except Exception as e:
            st.error(f"Server error: {e}")

elif st.session_state.page == "Login":
    st.subheader("Login")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login"):
        try:
            res = requests.post(f"{base_url}/login", json={"username": username, "password": password})
            if res.status_code == 200:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.token = res.json().get('token')

                prefs = requests.get(f"{base_url}/get_preferences", params={"username": username}).json()
                st.session_state.prefs = prefs

                st.success("Login successful!")
                st.session_state.page = "Meal Planner"
                time.sleep(1.5)
                st.rerun()
            else:
                msg = res.json().get('message', 'Invalid credentials.') if res.content else 'Unknown login error'
                st.error(msg)
        except Exception as e:
            st.error(f"Login failed: {e}")

elif st.session_state.page == "Meal Planner":
    if not st.session_state.logged_in:
        st.warning("Please log in to access the meal planner.")
    else:
        st.success(f"Welcome, {st.session_state.username}!")

        tabs = st.tabs(["🥗 Planner", "🚀 Features", "🧑‍💼 Profile"])

        with tabs[0]:
            st.subheader("1. User Input")
            prefs = st.session_state.get("prefs", {})
            with st.form("user_input_form"):
                age = st.number_input("Age", min_value=10, max_value=100, step=1, value=prefs.get("age", 25))
                weight = st.number_input("Weight (kg)", min_value=30.0, value=prefs.get("weight", 70.0))
                height = st.number_input("Height (cm)", min_value=100.0, value=prefs.get("height", 170.0))
                activity = st.selectbox("Activity Level", ["Sedentary", "Light", "Moderate", "Active", "Very Active"],
                                        index=["Sedentary", "Light", "Moderate", "Active", "Very Active"].index(prefs.get("activity", "Moderate")))
                goal = st.selectbox("Health Goal", ["Weight Loss", "Muscle Gain", "Diabetes"],
                                    index=["Weight Loss", "Muscle Gain", "Diabetes"].index(prefs.get("goal", "Weight Loss")))
                diet_type = st.selectbox("Diet Type", ["Veg", "Vegan", "Keto", "Gluten-Free"],
                                         index=["Veg", "Vegan", "Keto", "Gluten-Free"].index(prefs.get("diet", "Veg")))
                allergies = st.text_area("Allergies or Dislikes (comma separated)", value=prefs.get("allergies", ""))
                submitted = st.form_submit_button("Generate Plan")

            if submitted:
                requests.post(f"{base_url}/save_preferences", json={
                    "username": st.session_state.username,
                    "age": age,
                    "weight": weight,
                    "height": height,
                    "activity": activity,
                    "goal": goal,
                    "diet": diet_type,
                    "allergies": allergies
                })

                plan = {
                    "Breakfast": "Oats with banana",
                    "Lunch": "Grilled tofu salad",
                    "Dinner": "Quinoa with steamed broccoli",
                    "Snacks": "Almonds, Carrot sticks",
                    "Calories": 1900,
                    "Macros": {"Protein": 90, "Carbs": 200, "Fats": 50},
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state.meal_plans.append(plan)

                st.subheader("2. Meal Plan Recommendation")
                st.json(plan)

                st.subheader("3. Smart Grocery List")
                st.markdown("- Oats\n- Banana\n- Tofu\n- Quinoa\n- Broccoli\n- Almonds\n- Carrots")

                st.subheader("4. Analytics Dashboard")
                st.metric("Total Calories", f"{plan['Calories']} kcal")
                st.metric("Protein", f"{plan['Macros']['Protein']}g")
                st.metric("Carbs", f"{plan['Macros']['Carbs']}g")
                st.metric("Fats", f"{plan['Macros']['Fats']}g")

                st.subheader("5. Sustainability Score")
                st.success("Your meal plan saved 2.4kg CO2 this week! 🌱")

            if st.session_state.meal_plans:
                st.subheader("📉 Saved Meal Plan History")
                for plan in st.session_state.meal_plans[::-1]:
                    with st.expander(f"Plan on {plan['timestamp']}"):
                        st.write(plan)

                latest_plan = st.session_state.meal_plans[-1]
                evolving_ai_feedback_ui(latest_plan)

            if st.button("📜 Show My Feedback History"):
                try:
                    res = requests.get(f"{base_url}/get_feedback", params={"username": st.session_state.username})
                    if res.status_code == 200:
                        st.subheader("Your Feedback History")
                        for entry in res.json():
                            with st.expander(f"🕒 {entry['timestamp']}"):
                                st.write(f"**Skipped:** {entry['skipped']}")
                                st.write(f"**Disliked:** {entry['disliked']}")
                                st.write(f"**Notes:** {entry['notes']}")
                    else:
                        st.warning("No feedback history found.")
                except Exception as e:
                    st.error(f"Error fetching feedback history: {e}")

        with tabs[1]:
            st.header("🔄 Evolving AI Recommendations")
            with st.expander("What it does"):
                st.markdown("""
                - Adjusts meals based on skipped meals or changes in input.
                - Remembers disliked ingredients and adapts suggestions.
                - Dynamically recalculates nutrition goals with new weight/activity/goals.
                """)
                st.info("Learns over time using simple logic or ML in future.")

            st.header("🎮 Gamified Health Journey")
            with st.expander("Gamify your nutrition!"):
                st.markdown("""
                - Weekly challenges (hit macros or calorie goal)
                - Streak tracking and milestones (e.g., 10-day streak)
                - Reward store: avatar unlocks, new UI themes
                """)
                st.success("Streak and badge logic coming soon!")

            st.header("🧠 Mindful Eating Coach Mode")
            with st.expander("Coach Mode (Premium Feature)"):
                st.markdown("""
                - Daily educational blurbs: Why protein matters, how sugar affects you, etc.
                - Habits tracker: water intake, screen-free meals
                - Motivational quotes, reminders
                """)
                st.info("Premium toggle will unlock daily prompts.")

            st.header("🧪 Dynamic Recipe Discovery Engine")
            with st.expander("Smart Recommendations"):
                st.markdown("""
                - Suggest new dishes based on your preferences and history
                - Random global cuisine days (Thai Fridays, Indian Mondays)
                - Replace ingredient suggestions: "What if I swap tofu with chickpeas?"
                """)
                st.success("Dynamic NLP and tag-based suggestions in roadmap.")

        with tabs[2]:
            st.header("🧑‍💼 Update Profile Preferences")
            prefs = st.session_state.get("prefs", {})
            with st.form("update_pref_form"):
                age = st.number_input("Age", min_value=10, max_value=100, value=prefs.get("age", 25), key="profile_age")
                weight = st.number_input("Weight (kg)", min_value=30.0, value=prefs.get("weight", 70.0), key="profile_weight")
                height = st.number_input("Height (cm)", min_value=100.0, value=prefs.get("height", 170.0), key="profile_height")
                activity = st.selectbox("Activity Level", ["Sedentary", "Light", "Moderate", "Active", "Very Active"],
                                        index=["Sedentary", "Light", "Moderate", "Active", "Very Active"].index(prefs.get("activity", "Moderate")), key="profile_activity")
                goal = st.selectbox("Health Goal", ["Weight Loss", "Muscle Gain", "Diabetes"],
                                    index=["Weight Loss", "Muscle Gain", "Diabetes"].index(prefs.get("goal", "Weight Loss")), key="profile_goal")
                diet_type = st.selectbox("Diet Type", ["Veg", "Vegan", "Keto", "Gluten-Free"],
                                         index=["Veg", "Vegan", "Keto", "Gluten-Free"].index(prefs.get("diet", "Veg")), key="profile_diet")
                allergies = st.text_area("Allergies or Dislikes (comma separated)", value=prefs.get("allergies", ""), key="profile_allergies")
                update_btn = st.form_submit_button("Update Preferences")

            if update_btn:
                response = requests.put(f"{base_url}/update_preferences", json={
                    "username": st.session_state.username,
                    "age": age,
                    "weight": weight,
                    "height": height,
                    "activity": activity,
                    "goal": goal,
                    "diet": diet_type,
                    "allergies": allergies
                })
                if response.status_code == 200:
                    st.success("Preferences updated successfully!")
                    st.session_state.prefs = {
                        "age": age, "weight": weight, "height": height, "activity": activity,
                        "goal": goal, "diet": diet_type, "allergies": allergies
                    }
                else:
                    st.error("Failed to update preferences.")

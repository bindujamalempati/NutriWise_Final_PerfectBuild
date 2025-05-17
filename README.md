

## 🌱 NutriWise AI – Smart Meal Planner

> Your intelligent meal planning assistant powered by AI and personalized health tracking.




### 📖 Overview

NutriWise AI is a full-stack application that:

* Generates smart, healthy, and sustainable meal plans
* Adapts recommendations based on user input & feedback
* Tracks health goals like weight loss, muscle gain, and diabetes management
* Evolved using simple ML logic, user feedback loops, and gamification

---

### ✨ Features

* 📝 **Registration & Login** with token-based session
* 👤 **Profile-based preferences** (age, weight, diet, allergies)
* 🥗 **AI Meal Plan Generator** with calories & macros
* 🛒 **Smart Grocery List**
* 📊 **Analytics Dashboard** (Calories, Protein, Carbs, Fats)
* 🌍 **Sustainability Score** for eco-conscious users
* 🔁 **Evolving AI** – learns from skipped meals & dislikes
* 🧠 **Mindful Eating Coach Mode** (Premium)
* 🎮 **Gamified Nutrition Journey** with streaks & challenges

---



### 🏗️ Architecture

```
NutriWise_Final_PerfectBuild/
├── nutriwise_api/              # Flask API backend
│   ├── api.py                  # API routes and logic
│   └── database/users.db       # SQLite3 database
├── nutriwise_frontend/        # Streamlit frontend
│   └── streamlit_dashboard.py  # Streamlit app
├── requirements.txt
├── render.yaml                 # Render deployment config
└── README.md
```

---

### 🚀 Deployment (Render)

Frontend (Streamlit):
📍 `streamlit run nutriwise_frontend/streamlit_dashboard.py`

Backend (Flask API):
📍 `gunicorn nutriwise_api.api:app`

### 🌐 Environment Variable

```env
API_BASE_URL=https://nutriwise-final-perfectbuild.onrender.com
```

---

### 🔧 Tech Stack

* **Frontend**: Streamlit
* **Backend**: Flask API
* **Database**: SQLite3
* **Deployment**: Render
* **Extras**: JWT Auth, Feedback Loop, Gamification, Sustainability Score

---

### 💡 Future Enhancements

* Integrate GPT-based dynamic meal suggestions
* Real-time calorie tracking from wearables
* Advanced ML models for adaptive nutrition
* Cloud-based NoSQL storage and analytics

---

### 🤝 Contributors

* 👩‍💻 Binduja Malempati – *Lead Developer & Architect*

---

### 📬 Contact

For queries, feel free to reach out [bindujamalempati@gmail.com](mailto:bindujamalempati@gmail.com)



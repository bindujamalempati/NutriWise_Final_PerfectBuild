Sure! Here's a **concise and stylish `README.md` version** of your NutriWise project with **badges, a short description, features, deployment info, and links** — perfect for quick GitHub display:

---

### 📝 Short Version of `README.md`

````markdown
# 🌱 NutriWise AI – Smart Meal Planner

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-orange?logo=streamlit)](https://streamlit.io/)
[![Render](https://img.shields.io/badge/Backend-Deployed%20on%20Render-8B0000?logo=render)](https://nutriwise-final-perfectbuild.onrender.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🎯 Overview

NutriWise is a full-stack AI-driven app that crafts personalized meal plans, evolves based on user feedback, and promotes sustainable health habits.

---

## ⚙️ Tech Stack
- Frontend: Streamlit  
- Backend: Flask API (JWT-secured)  
- DB: SQLite3  
- Hosted on: [Render](https://render.com)

---

## 🚀 Live App
👉 **[Open NutriWise](https://nutriwise-final-perfectbuild.onrender.com)**

---

## 🔑 Features
- 🍽️ Custom meal plans (age, weight, goal)
- 🔁 Evolving AI with feedback (dislikes/skips)
- 📊 Nutrition dashboard & sustainability score
- 🧠 Coach mode, gamified journey (roadmap)

---

## 📦 Deployment

### Backend:
```bash
gunicorn nutriwise_api.api:app
````

### Frontend:

```bash
streamlit run nutriwise_frontend/streamlit_dashboard.py --server.port=10000 --server.enableCORS=false --server.enableXsrfProtection=false
```

Set `API_BASE_URL` in Render frontend env.

---

## 📧 Contact

**Binduja Malempati** – [LinkedIn](https://www.linkedin.com/in/bindujamalempati)

---

> 💚 MIT Licensed • Feedback welcomed!

```

Let me know if you'd like the GIF version added or auto-generate badges for tools like GitHub Actions or Docker later!
```

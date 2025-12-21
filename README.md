
🧠 SmartQuizzer – Adaptive AI-Based Quiz Generator

An interactive AI-powered quiz application built using Python and Streamlit, designed to evaluate learners through adaptive, difficulty-based quizzes.
Users can upload study material, select quiz difficulty levels, attempt timed questions, and view performance insights.

🎯 Project Objective

The objective of SmartQuizzer is to build an intelligent quiz system that:

Assesses user knowledge using MCQ-based quizzes

Provides difficulty-wise evaluation (Easy, Medium, Difficult)

Enhances learning by giving instant feedback and explanations

Offers a smooth and interactive quiz experience

🚀 Features

📄 Upload study material (PDF / TXT)

👤 User details input (Name & Email)

🎚 Difficulty selection (Easy / Medium / Difficult)

⏱ Time-limited questions

✅ Multiple-choice questions

📊 Scoreboard and performance summary

🤖 AI-based answer explanation (OpenAI API)

🎈 Interactive Streamlit UI

🛠 Technologies Used

Python

Streamlit

OpenAI API

dotenv

Session State Management
## 📁 Project Structure

```text
SmartQuizzer/
├── smartquizzer_streamlit.py   # Main Streamlit application
├── README.md                  # Documentation
├── requirements.txt           # Python dependencies
└── .env                       # API key configuration
```

⚙️ Installation & Setup


##1️⃣ Clone Repository


git clone https://github.com/RoopaPavani/SmartQuizzer.git
cd SmartQuizzer

 ##2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

### Activate the virtual environment

**Windows**
```bash
venv\Scripts\activate
```

**Mac / Linux**
```bash
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Environment Variables

Create a `.env` file in the project root and add:

```env
OPENAI_API_KEY=your_openai_api_key
```

---

## ▶️ Run the Application

```bash
streamlit run smartquizzer_streamlit.py
```

Open in browser:

```
http://localhost:8501
```


🎮 How to Use

Enter Name and Email

Upload study material

Select difficulty level

Answer quiz questions within the given time

View score and explanations

🎥 Demo Video

🔗 https://drive.google.com/file/d/1xc4GlmOcQ6RsPVu0EGVEX-cpMeTheN5e/view?usp=drive_link

📊 Evaluation Highlights

Clean and modular code

Streamlit-based UI

AI integration for explanations

Difficulty-based quiz structure

GitHub-ready documentation

🔮 Future Enhancements

Automatic question generation from uploaded content

Topic-wise analytics

Database integration

Fully adaptive difficulty engine

📄 License

This project is for educational and academic purposes.

🙌 Acknowledgements

Streamlit Documentation

OpenAI API

Infosys Virtual Internship Program

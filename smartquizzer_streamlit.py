
# ================= IMPORTS =================
import os
import time
from dotenv import load_dotenv
import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pdfplumber

# ================= LOAD ENV =================
load_dotenv()

# ================= PAGE CONFIG =================
st.set_page_config(page_title="SmartQuizzer", layout="wide")

# ================= QUESTIONS =================
questions = {
    "Easy": [
        {"q": "🤖 What is Machine Learning?", "opts": ["Subset of AI", "Database", "Hardware", "Web Tool"],
         "ans": "Subset of AI"},
        {"q": "📊 ML works mainly on?", "opts": ["Data", "Hardware", "Cables", "Design"],
         "ans": "Data"},
        {"q": "🐍 Which language is popular for ML?", "opts": ["Python", "HTML", "CSS", "JavaScript"],
         "ans": "Python"},
        {"q": "🧠 ML is part of which field?", "opts": ["AI", "DBMS", "OS", "Networking"],
         "ans": "AI"},
        {"q": "📚 Which is an ML library?", "opts": ["Scikit-learn", "Bootstrap", "React", "Angular"],
         "ans": "Scikit-learn"}
    ],
    "Medium": [
        {"q": "🌳 Which algorithm is used for classification?", "opts": ["Decision Tree", "K-Means", "Apriori", "PCA"],
         "ans": "Decision Tree"},
        {"q": "🏷 What is supervised learning?", "opts": ["Labeled data", "No data", "Random learning", "Unlabeled data"],
         "ans": "Labeled data"},
        {"q": "🔍 Which is an unsupervised algorithm?", "opts": ["K-Means", "SVM", "Naive Bayes", "Decision Tree"],
         "ans": "K-Means"},
        {"q": "✅ Accuracy is used for?", "opts": ["Classification", "Clustering", "Regression", "Cleaning"],
         "ans": "Classification"},
        {"q": "🧪 Train-test split is used for?", "opts": ["Model evaluation", "UI design", "Deployment", "Cleaning"],
         "ans": "Model evaluation"}
    ],
    "Difficult": [
        {"q": "⚠ What is overfitting?",
         "opts": ["Model performs well on training but poorly on new data",
                  "Model trains very fast", "Model has less data",
                  "Model always performs poorly"],
         "ans": "Model performs well on training but poorly on new data"},
        {"q": "🛠 Which technique reduces overfitting?",
         "opts": ["Regularization", "More epochs", "High learning rate", "No validation"],
         "ans": "Regularization"},
        {"q": "⚖ Bias-Variance tradeoff is related to?",
         "opts": ["Model performance", "Hardware", "Database", "Frontend"],
         "ans": "Model performance"},
        {"q": "🌲 Which is an ensemble method?",
         "opts": ["Random Forest", "KNN", "Linear Regression", "K-Means"],
         "ans": "Random Forest"},
        {"q": "🔁 Cross-validation is used for?",
         "opts": ["Reliable evaluation", "Deployment", "Cleaning", "Visualization"],
         "ans": "Reliable evaluation"}
    ]
}

# ================= SESSION STATE =================
if "page" not in st.session_state:
    st.session_state.page = "start"
if "level" not in st.session_state:
    st.session_state.level = None
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "answers" not in st.session_state:
    st.session_state.answers = {"Easy": [], "Medium": [], "Difficult": []}
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

# ================= AI EXPLANATION (SAFE) =================
def llm_explanation(question, correct_answer):
    return f"The correct answer is '{correct_answer}' because it correctly explains the concept asked."

# ================= START PAGE =================
st.title("🧠 SmartQuizzer")

if st.session_state.page == "start":
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")

    uploaded_file = st.file_uploader("Upload study material (TXT or PDF)", type=["txt", "pdf"])

    extracted_text = ""

    if uploaded_file is not None:
        if uploaded_file.type == "text/plain":
            extracted_text = uploaded_file.read().decode("utf-8")

        elif uploaded_file.type == "application/pdf":
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    extracted_text += page.extract_text() or ""

        if extracted_text.strip():
            st.subheader("📄 Uploaded Study Material Preview")
            st.text_area("Content", extracted_text[:2000], height=200)

    if st.button("Start Quiz"):
        if name and email and uploaded_file:
            st.session_state.page = "level_select"
            st.session_state.q_index = 0
            st.session_state.start_time = time.time()
            st.rerun()
        else:
            st.warning("Please enter Name, Email and upload a file.")

# ================= LEVEL SELECTION =================
elif st.session_state.page == "level_select":
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Easy"):
            st.session_state.level = "Easy"
            st.session_state.page = "quiz"
            st.session_state.q_index = 0
            st.session_state.start_time = time.time()
            st.rerun()

    with col2:
        if st.button("Medium"):
            st.session_state.level = "Medium"
            st.session_state.page = "quiz"
            st.session_state.q_index = 0
            st.session_state.start_time = time.time()
            st.rerun()

    with col3:
        if st.button("Difficult"):
            st.session_state.level = "Difficult"
            st.session_state.page = "quiz"
            st.session_state.q_index = 0
            st.session_state.start_time = time.time()
            st.rerun()

# ================= QUIZ PAGE =================
elif st.session_state.page == "quiz":
    level = st.session_state.level
    qlist = questions[level]

    st_autorefresh(interval=1000, key="timer")

    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(0, 20 - elapsed)
    st.info(f"⏱ Time Remaining: {remaining} seconds")

    q = qlist[st.session_state.q_index]
    st.subheader(f"{level} Question {st.session_state.q_index + 1}")
    st.write(q["q"])

    choice = st.radio("Choose your answer", q["opts"])

    if st.button("Submit") or remaining == 0:
        st.session_state.answers[level].append(choice if remaining > 0 else None)
        st.session_state.q_index += 1
        st.session_state.start_time = time.time()

        if st.session_state.q_index >= 5:
            st.session_state.page = "level_select"

        st.rerun()

# ================= RESULT PAGE =================
if all(len(st.session_state.answers[lvl]) == 5 for lvl in ["Easy", "Medium", "Difficult"]):
    st.header("📊 Final Score")

    total = 0
    for lvl in ["Easy", "Medium", "Difficult"]:
        correct = 0
        for i, q in enumerate(questions[lvl]):
            if st.session_state.answers[lvl][i] == q["ans"]:
                correct += 1
            else:
                st.write(f"❌ {q['q']}")
                st.write(f"✔ Correct Answer: {q['ans']}")
                st.write("📘 Explanation:", llm_explanation(q["q"], q["ans"]))

        score = correct * 3
        total += score
        st.success(f"{lvl} Score: {score}")

    st.balloons()
    st.success(f"🏆 Total Score: {total}")

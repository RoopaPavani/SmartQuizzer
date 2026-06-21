# app.py - SmartQuizzer Adaptive AI-Based Quiz Generator
# Complete Enhanced Implementation with Updated Explanation Colors

import streamlit as st
import openai
import PyPDF2
import docx
import json
import re
import time
import random
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import os
from dotenv import load_dotenv
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import base64
from io import BytesIO

# Load environment variables
load_dotenv()

# Configure OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

# Page Configuration
st.set_page_config(
    page_title="SmartQuizzer - AI Quiz Generator",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI with updated explanation colors
st.markdown("""
    <style>
    /* Main Styles */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        animation: fadeIn 0.8s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .score-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(245, 87, 108, 0.3);
        transition: transform 0.3s ease;
    }
    
    .score-card:hover {
        transform: translateY(-5px);
    }
    
    .question-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin: 1rem 0;
        border-left: 5px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .question-card:hover {
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }
    
    .correct-answer {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border-left: 5px solid #28a745;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        animation: slideIn 0.5s ease;
    }
    
    .wrong-answer {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border-left: 5px solid #dc3545;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        animation: slideIn 0.5s ease;
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    /* Updated Explanation Box - New Color Scheme */
    .explanation-box {
        background: linear-gradient(135deg, #fff5e6 0%, #ffe8cc 100%) !important;
        padding: 1.5rem;
        border-radius: 12px;
        margin-top: 1rem;
        border-left: 5px solid #ff8c00;
        box-shadow: 0 4px 15px rgba(255, 140, 0, 0.15);
        transition: all 0.3s ease;
    }
    
    .explanation-box:hover {
        box-shadow: 0 6px 25px rgba(255, 140, 0, 0.25);
        transform: translateX(5px);
    }
    
    .explanation-box h4 {
        color: #cc6b00 !important;
        font-weight: 700;
        margin-bottom: 0.8rem;
        font-size: 1.1rem;
    }
    
    .explanation-box p {
        color: #4a3520 !important;
        line-height: 1.6;
        font-size: 1rem;
    }
    
    .explanation-box strong {
        color: #cc6b00 !important;
    }
    
    /* Alternative Explanation Box - Blue Theme (optional) */
    .explanation-box-blue {
        background: linear-gradient(135deg, #e6f3ff 0%, #cce5ff 100%) !important;
        border-left: 5px solid #0066cc;
        padding: 1.5rem;
        border-radius: 12px;
        margin-top: 1rem;
        box-shadow: 0 4px 15px rgba(0, 102, 204, 0.15);
    }
    
    .explanation-box-blue h4 {
        color: #004d99 !important;
    }
    
    .explanation-box-blue p {
        color: #1a2a3a !important;
    }
    
    /* Alternative Explanation Box - Green Theme */
    .explanation-box-green {
        background: linear-gradient(135deg, #e6ffe6 0%, #ccffcc 100%) !important;
        border-left: 5px solid #00aa00;
        padding: 1.5rem;
        border-radius: 12px;
        margin-top: 1rem;
        box-shadow: 0 4px 15px rgba(0, 170, 0, 0.15);
    }
    
    .explanation-box-green h4 {
        color: #007700 !important;
    }
    
    .explanation-box-green p {
        color: #1a3a1a !important;
    }
    
    /* Alternative Explanation Box - Purple Theme */
    .explanation-box-purple {
        background: linear-gradient(135deg, #f0e6ff 0%, #e0ccff 100%) !important;
        border-left: 5px solid #7b2fbe;
        padding: 1.5rem;
        border-radius: 12px;
        margin-top: 1rem;
        box-shadow: 0 4px 15px rgba(123, 47, 190, 0.15);
    }
    
    .explanation-box-purple h4 {
        color: #5a1f8a !important;
    }
    
    .explanation-box-purple p {
        color: #2a1a3a !important;
    }
    
    .stButton>button {
        border-radius: 25px;
        height: 3em;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    
    .stButton>button:active {
        transform: translateY(0px);
    }
    
    .timer-warning {
        color: #ff6b6b;
        font-weight: bold;
        font-size: 1.3em;
        animation: blink 1s infinite;
    }
    
    @keyframes blink {
        0% { opacity: 1; }
        50% { opacity: 0.4; }
        100% { opacity: 1; }
    }
    
    .difficulty-badge {
        padding: 0.3rem 1.2rem;
        border-radius: 25px;
        font-weight: bold;
        display: inline-block;
        font-size: 0.9em;
        letter-spacing: 0.5px;
    }
    
    .difficulty-easy {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        box-shadow: 0 2px 10px rgba(40,167,69,0.3);
    }
    
    .difficulty-medium {
        background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%);
        color: white;
        box-shadow: 0 2px 10px rgba(255,193,7,0.3);
    }
    
    .difficulty-hard {
        background: linear-gradient(135deg, #dc3545 0%, #e74c3c 100%);
        color: white;
        box-shadow: 0 2px 10px rgba(220,53,69,0.3);
    }
    
    .result-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .result-card:hover {
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }
    
    .badge-container {
        display: flex;
        justify-content: center;
        gap: 1rem;
        flex-wrap: wrap;
        margin: 1.5rem 0;
    }
    
    .badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 50px;
        font-weight: bold;
        font-size: 1.1em;
        box-shadow: 0 4px 15px rgba(102,126,234,0.4);
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .badge-gold {
        background: linear-gradient(135deg, #f7971e 0%, #ffd200 100%);
        box-shadow: 0 4px 15px rgba(247,151,30,0.4);
        color: #333;
    }
    
    .badge-silver {
        background: linear-gradient(135deg, #bdc3c7 0%, #95a5a6 100%);
        box-shadow: 0 4px 15px rgba(189,195,199,0.4);
    }
    
    .badge-bronze {
        background: linear-gradient(135deg, #cd7f32 0%, #b87333 100%);
        box-shadow: 0 4px 15px rgba(205,127,50,0.4);
    }
    
    .option-btn {
        display: block;
        width: 100%;
        padding: 0.8rem 1.5rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        background: white;
        text-align: left;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .option-btn:hover {
        border-color: #667eea;
        background: #f8f9ff;
        transform: translateX(5px);
    }
    
    .option-btn-selected {
        border-color: #667eea;
        background: #e8edff;
        transform: translateX(5px);
    }
    
    .option-btn-correct {
        border-color: #28a745;
        background: #d4edda;
    }
    
    .option-btn-wrong {
        border-color: #dc3545;
        background: #f8d7da;
    }
    
    .progress-ring {
        position: relative;
        display: inline-block;
    }
    
    .floating {
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    .gradient-text {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    
    .confetti-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 9999;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state variables
def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        'quiz_state': 'setup',
        'questions': [],
        'current_question': 0,
        'score': 0,
        'total_questions': 0,
        'user_answers': [],
        'timer_start': None,
        'time_remaining': 30,
        'quiz_completed': False,
        'difficulty': 'medium',
        'user_name': '',
        'user_email': '',
        'question_times': [],
        'topic': '',
        'content': '',
        'show_explanation': False,
        'selected_option': None,
        'answered': False,
        'question_start_time': None,
        'badges_earned': [],
        'perfect_score': False,
        'streak': 0,
        'max_streak': 0
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# Helper Functions
def extract_text_from_pdf(file) -> str:
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return ""

def extract_text_from_txt(file) -> str:
    """Extract text from TXT file"""
    try:
        text = file.read().decode('utf-8')
        return text
    except Exception as e:
        st.error(f"Error reading TXT: {str(e)}")
        return ""

def extract_text_from_docx(file) -> str:
    """Extract text from DOCX file"""
    try:
        doc = docx.Document(file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading DOCX: {str(e)}")
        return ""

def process_uploaded_file(uploaded_file) -> str:
    """Process uploaded file and extract text"""
    file_type = uploaded_file.type
    
    if file_type == "application/pdf":
        return extract_text_from_pdf(uploaded_file)
    elif file_type == "text/plain":
        return extract_text_from_txt(uploaded_file)
    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_text_from_docx(uploaded_file)
    else:
        st.error("Unsupported file format. Please upload PDF, TXT, or DOCX.")
        return ""

def generate_questions_with_openai(content: str, difficulty: str, num_questions: int) -> List[Dict]:
    """Generate questions using OpenAI API"""
    try:
        difficulty_prompts = {
            'easy': "basic, fundamental concepts with simple recall questions",
            'medium': "intermediate level, applied concepts with scenario-based questions",
            'hard': "advanced, complex reasoning, analytical questions requiring deep understanding"
        }
        
        prompt = f"""
        Based on the following content, generate exactly {num_questions} {difficulty} difficulty multiple-choice questions.
        The questions should test {difficulty_prompts[difficulty]} understanding.
        
        Content: {content[:4000]}
        
        Format the response as a JSON array with exactly {num_questions} objects.
        Each object must have:
        - "question": string (the question text, should be clear and concise)
        - "options": array of 4 strings (the answer choices, one should be clearly correct)
        - "correct": integer (0-3 index of correct answer)
        - "explanation": string (detailed explanation of why the answer is correct, include key concepts)
        
        Make sure:
        1. Questions are varied and cover different aspects of the content
        2. Options are plausible but only one is correct
        3. Explanations are educational and detailed
        4. The difficulty level is appropriate for {difficulty}
        
        Ensure the JSON is valid and properly formatted.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert educational quiz generator. Generate high-quality, accurate, and engaging questions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2500
        )
        
        content_response = response.choices[0].message.content
        
        # Extract JSON from response
        try:
            json_match = re.search(r'\[.*\]', content_response, re.DOTALL)
            if json_match:
                questions = json.loads(json_match.group())
            else:
                questions = json.loads(content_response)
        except json.JSONDecodeError:
            st.warning("Failed to parse AI response. Using fallback questions.")
            questions = generate_fallback_questions(content, difficulty, num_questions)
        
        # Validate and format questions
        formatted_questions = []
        for q in questions:
            if all(key in q for key in ['question', 'options', 'correct', 'explanation']):
                formatted_questions.append({
                    'question': q['question'],
                    'options': q['options'][:4],
                    'correct': q['correct'] if q['correct'] < 4 else 0,
                    'explanation': q['explanation'],
                    'difficulty': difficulty
                })
        
        if not formatted_questions:
            formatted_questions = generate_fallback_questions(content, difficulty, num_questions)
        
        return formatted_questions[:num_questions]
        
    except Exception as e:
        st.error(f"Error generating questions: {str(e)}")
        return generate_fallback_questions(content, difficulty, num_questions)

def generate_fallback_questions(content: str, difficulty: str, num_questions: int) -> List[Dict]:
    """Generate fallback questions when API fails"""
    topics = extract_topics(content)
    questions = []
    
    question_templates = [
        {
            'template': "What is the main concept related to '{topic}'?",
            'options': [
                "Understanding the fundamental principles",
                "Application of theoretical knowledge",
                "Practical implementation strategies",
                "Advanced problem-solving techniques"
            ]
        },
        {
            'template': "Which statement best describes '{topic}'?",
            'options': [
                "It is a basic concept in the field",
                "It requires advanced understanding",
                "It is commonly applied in practice",
                "It is a theoretical framework"
            ]
        }
    ]
    
    for i in range(min(num_questions, 15)):
        topic = topics[i % len(topics)] if topics else f"Topic {i+1}"
        template = question_templates[i % len(question_templates)]
        
        correct_index = i % 4
        options = template['options'][:4]
        # Shuffle options and track correct answer
        shuffled_options = options.copy()
        random.shuffle(shuffled_options)
        correct_index = shuffled_options.index(options[correct_index % len(options)])
        
        question = {
            'question': template['template'].format(topic=topic),
            'options': shuffled_options,
            'correct': correct_index,
            'explanation': f"The correct answer is based on the understanding of '{topic}' as discussed in the provided content.",
            'difficulty': difficulty
        }
        questions.append(question)
    
    return questions

def extract_topics(content: str) -> List[str]:
    """Extract potential topics from content"""
    sentences = [s.strip() for s in content.split('.') if len(s.strip()) > 10]
    topics = []
    
    for sentence in sentences[:30]:
        words = sentence.split()
        if len(words) > 3 and len(words) < 20:
            # Extract key phrases
            phrase = ' '.join(words[:4])
            if len(phrase) > 5 and phrase not in topics:
                topics.append(phrase)
    
    return topics[:10]

def get_time_limit(difficulty: str) -> int:
    """Get time limit based on difficulty"""
    time_limits = {
        'easy': 30,
        'medium': 45,
        'hard': 60
    }
    return time_limits.get(difficulty, 30)

def calculate_score(user_answers: List[Dict], questions: List[Dict]) -> Dict:
    """Calculate detailed score metrics"""
    correct = 0
    total = len(questions)
    difficulty_breakdown = {'easy': {'correct': 0, 'total': 0, 'time': []}, 
                           'medium': {'correct': 0, 'total': 0, 'time': []}, 
                           'hard': {'correct': 0, 'total': 0, 'time': []}}
    
    for i, answer in enumerate(user_answers):
        if i < len(questions):
            q = questions[i]
            if answer.get('selected') == q['correct']:
                correct += 1
            diff = q.get('difficulty', 'medium')
            difficulty_breakdown[diff]['total'] += 1
            if answer.get('selected') == q['correct']:
                difficulty_breakdown[diff]['correct'] += 1
            difficulty_breakdown[diff]['time'].append(answer.get('time_taken', 0))
    
    return {
        'total_correct': correct,
        'total_questions': total,
        'percentage': (correct / total * 100) if total > 0 else 0,
        'difficulty_breakdown': difficulty_breakdown,
        'accuracy_by_difficulty': {
            diff: (data['correct'] / data['total'] * 100) if data['total'] > 0 else 0
            for diff, data in difficulty_breakdown.items()
        },
        'avg_time_by_difficulty': {
            diff: sum(data['time']) / len(data['time']) if data['time'] else 0
            for diff, data in difficulty_breakdown.items()
        }
    }

def get_badges(score_percentage: float, streak: int, perfect_score: bool) -> List[str]:
    """Get badges based on performance"""
    badges = []
    
    if perfect_score:
        badges.append({"name": "🏆 Perfect Score", "class": "badge-gold", "description": "Answered all questions correctly!"})
    
    if score_percentage >= 90:
        badges.append({"name": "⭐ Excellence", "class": "badge-gold", "description": "Outstanding performance!"})
    elif score_percentage >= 70:
        badges.append({"name": "🌟 Achiever", "class": "badge-silver", "description": "Great performance!"})
    elif score_percentage >= 50:
        badges.append({"name": "📚 Learner", "class": "badge-bronze", "description": "Good effort, keep learning!"})
    
    if streak >= 5:
        badges.append({"name": "🔥 Streak Master", "class": "badge-gold", "description": f"Got {streak} questions right in a row!"})
    elif streak >= 3:
        badges.append({"name": "💪 Streak Builder", "class": "badge-silver", "description": f"Got {streak} questions right in a row!"})
    
    if len(badges) == 0:
        badges.append({"name": "🎯 Participant", "class": "badge", "description": "Thanks for participating!"})
    
    return badges

def reset_quiz():
    """Reset the quiz state"""
    st.session_state.quiz_state = 'setup'
    st.session_state.questions = []
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.user_answers = []
    st.session_state.quiz_completed = False
    st.session_state.question_times = []
    st.session_state.time_remaining = 30
    st.session_state.show_explanation = False
    st.session_state.selected_option = None
    st.session_state.answered = False
    st.session_state.badges_earned = []
    st.session_state.perfect_score = False
    st.session_state.streak = 0
    st.session_state.max_streak = 0

# UI Components
def header_component():
    """Display the main header"""
    st.markdown("""
    <div class="main-header floating">
        <h1>🧠 SmartQuizzer</h1>
        <h3>Adaptive AI-Based Quiz Generator</h3>
        <p>📚 Upload your study material and test your knowledge with AI-generated questions</p>
        <p style="font-size: 0.9em; opacity: 0.9;">✨ Powered by GPT-3.5 Turbo</p>
    </div>
    """, unsafe_allow_html=True)

def setup_section():
    """Setup section for quiz configuration"""
    st.markdown("### 📚 Quiz Setup")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "📄 Upload Study Material",
            type=['pdf', 'txt', 'docx'],
            help="Upload PDF, TXT, or DOCX files containing your study material"
        )
        
        if uploaded_file:
            with st.spinner("📖 Processing file..."):
                content = process_uploaded_file(uploaded_file)
                if content:
                    st.session_state.content = content
                    st.success(f"✅ File processed successfully! ({len(content)} characters)")
                    
                    with st.expander("📖 Content Preview"):
                        st.text(content[:500] + "...")
                else:
                    st.error("❌ Failed to process file. Please try again.")
    
    with col2:
        st.markdown("#### 👤 User Details")
        name = st.text_input("Name", placeholder="Enter your name", key="setup_name")
        email = st.text_input("Email", placeholder="Enter your email", key="setup_email")
        
        st.markdown("#### ⚙️ Quiz Settings")
        difficulty = st.select_slider(
            "Difficulty Level",
            options=['easy', 'medium', 'hard'],
            value='medium',
            help="Easy: Basic concepts, Medium: Applied knowledge, Hard: Complex reasoning"
        )
        
        num_questions = st.select_slider(
            "Number of Questions",
            options=[5, 10, 15, 20],
            value=10,
            step=5
        )
    
    # Start button
    if st.button("🚀 Start Quiz", type="primary", use_container_width=True):
        if not uploaded_file:
            st.error("⚠️ Please upload study material first!")
        elif not name:
            st.error("⚠️ Please enter your name!")
        elif not email:
            st.error("⚠️ Please enter your email!")
        else:
            with st.spinner("🧠 Generating quiz questions..."):
                st.session_state.user_name = name
                st.session_state.user_email = email
                st.session_state.difficulty = difficulty
                st.session_state.total_questions = num_questions
                
                content = st.session_state.content
                questions = generate_questions_with_openai(content, difficulty, num_questions)
                
                if questions:
                    st.session_state.questions = questions
                    st.session_state.current_question = 0
                    st.session_state.score = 0
                    st.session_state.user_answers = []
                    st.session_state.quiz_state = 'playing'
                    st.session_state.quiz_completed = False
                    st.session_state.question_times = []
                    st.session_state.time_remaining = get_time_limit(difficulty)
                    st.session_state.show_explanation = False
                    st.session_state.selected_option = None
                    st.session_state.answered = False
                    st.session_state.question_start_time = time.time()
                    st.rerun()
                else:
                    st.error("❌ Failed to generate questions. Please try again.")

def display_question_options(question_data: Dict, q_index: int):
    """Display question options with custom styling"""
    options = question_data['options']
    selected = st.session_state.selected_option
    
    # Create columns for options (2x2 grid)
    cols = st.columns(2)
    
    for i, option in enumerate(options):
        col_idx = i % 2
        with cols[col_idx]:
            # Determine button style
            button_type = "option-btn"
            if selected is not None:
                if i == selected and i == question_data['correct']:
                    button_type = "option-btn option-btn-correct"
                elif i == selected and i != question_data['correct']:
                    button_type = "option-btn option-btn-wrong"
                elif i == question_data['correct'] and st.session_state.answered:
                    button_type = "option-btn option-btn-correct"
                elif i == selected:
                    button_type = "option-btn option-btn-selected"
            
            # Use a unique key for each option
            option_key = f"opt_{q_index}_{i}"
            
            # Display option as a button
            if st.button(
                f"{chr(65 + i)}. {option}",
                key=option_key,
                use_container_width=True,
                disabled=st.session_state.answered
            ):
                if not st.session_state.answered:
                    st.session_state.selected_option = i
                    st.rerun()

def quiz_playing_section():
    """Main quiz playing section with enhanced UI"""
    if not st.session_state.questions:
        st.error("No questions available. Please restart the quiz.")
        if st.button("🔄 Restart Setup"):
            reset_quiz()
            st.rerun()
        return
    
    questions = st.session_state.questions
    current_q = st.session_state.current_question
    total_q = len(questions)
    question_data = questions[current_q]
    
    # Progress header with enhanced styling
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        st.markdown(f"### 📝 Question {current_q + 1} of {total_q}")
        progress = (current_q) / total_q
        st.progress(progress, text=f"{int(progress * 100)}% Complete")
    
    with col2:
        difficulty_colors = {
            'easy': '🟢',
            'medium': '🟡',
            'hard': '🔴'
        }
        diff = question_data.get('difficulty', 'medium')
        badge_class = f"difficulty-{diff}"
        st.markdown(f"""
        <div class="difficulty-badge {badge_class}">
            {difficulty_colors.get(diff, '')} {diff.title()}
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Timer with enhanced styling
        if st.session_state.timer_start is None:
            st.session_state.timer_start = time.time()
            st.session_state.time_remaining = get_time_limit(st.session_state.difficulty)
        
        elapsed = time.time() - st.session_state.timer_start
        time_limit = get_time_limit(st.session_state.difficulty)
        remaining = max(0, time_limit - elapsed)
        st.session_state.time_remaining = remaining
        
        timer_color = "normal"
        if remaining < 10:
            timer_color = "timer-warning"
        
        st.markdown(f"""
        <div class='{timer_color}' style='text-align: center;'>
            ⏱️ {int(remaining)}s
        </div>
        """, unsafe_allow_html=True)
        
        if remaining <= 0 and not st.session_state.answered:
            st.warning("⏰ Time's up!")
            handle_time_up()
            return
    
    with col4:
        st.markdown(f"""
        <div style='text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 0.5rem; border-radius: 10px; color: white;'>
            <strong>Score: {st.session_state.score}/{total_q}</strong>
        </div>
        """, unsafe_allow_html=True)
    
    # Display question with enhanced styling
    st.markdown(f"""
    <div class="question-card">
        <h4 style='color: #333; margin-bottom: 1rem;'>📖 {question_data['question']}</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Display options
    display_question_options(question_data, current_q)
    
    # Submit and feedback section
    if st.session_state.selected_option is not None and not st.session_state.answered:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("✅ Submit Answer", type="primary", use_container_width=True):
                process_answer(current_q)
    
    # Show explanation after answering
    if st.session_state.answered:
        show_answer_feedback(current_q, question_data)
        
        # Next question button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if current_q + 1 < total_q:
                if st.button("➡️ Next Question", type="primary", use_container_width=True):
                    move_to_next_question()
            else:
                if st.button("🏆 View Results", type="primary", use_container_width=True):
                    st.session_state.quiz_state = 'results'
                    st.session_state.quiz_completed = True
                    st.rerun()

def process_answer(current_q: int):
    """Process the user's answer"""
    question_data = st.session_state.questions[current_q]
    selected = st.session_state.selected_option
    correct_index = question_data['correct']
    is_correct = selected == correct_index
    
    # Calculate time taken
    time_taken = get_time_limit(st.session_state.difficulty) - st.session_state.time_remaining
    
    # Update score and streak
    if is_correct:
        st.session_state.score += 1
        st.session_state.streak += 1
        if st.session_state.streak > st.session_state.max_streak:
            st.session_state.max_streak = st.session_state.streak
    else:
        st.session_state.streak = 0
    
    # Store answer
    st.session_state.user_answers.append({
        'question': current_q,
        'selected': selected,
        'correct': correct_index,
        'is_correct': is_correct,
        'time_taken': time_taken
    })
    
    st.session_state.question_times.append(time_taken)
    st.session_state.answered = True
    st.session_state.show_explanation = True
    st.rerun()

def show_answer_feedback(current_q: int, question_data: Dict):
    """Show feedback for the current question"""
    user_answer = st.session_state.user_answers[-1] if st.session_state.user_answers else None
    
    if user_answer:
        is_correct = user_answer['is_correct']
        correct_index = question_data['correct']
        options = question_data['options']
        
        if is_correct:
            st.markdown("""
            <div class="correct-answer">
                <h4>✅ Correct! 🎉</h4>
                <p style='margin: 0;'>Great job! You selected the right answer.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="wrong-answer">
                <h4>❌ Incorrect</h4>
                <p style='margin: 0;'>The correct answer was: <strong>{options[correct_index]}</strong></p>
            </div>
            """, unsafe_allow_html=True)
        
        # Show time taken
        st.info(f"⏱️ Time taken: {user_answer['time_taken']:.1f}s")
        
        # Show explanation with updated color scheme
        st.markdown(f"""
        <div class="explanation-box">
            <h4>💡 Explanation</h4>
            <p style='margin: 0;'>{question_data['explanation']}</p>
        </div>
        """, unsafe_allow_html=True)

def move_to_next_question():
    """Move to the next question"""
    st.session_state.current_question += 1
    st.session_state.timer_start = time.time()
    st.session_state.time_remaining = get_time_limit(st.session_state.difficulty)
    st.session_state.show_explanation = False
    st.session_state.selected_option = None
    st.session_state.answered = False
    st.session_state.question_start_time = time.time()
    st.rerun()

def handle_time_up():
    """Handle when time runs out"""
    if not st.session_state.answered:
        current_q = st.session_state.current_question
        question_data = st.session_state.questions[current_q]
        
        # Record as wrong answer
        st.session_state.user_answers.append({
            'question': current_q,
            'selected': None,
            'correct': question_data['correct'],
            'is_correct': False,
            'time_taken': get_time_limit(st.session_state.difficulty)
        })
        
        st.session_state.question_times.append(get_time_limit(st.session_state.difficulty))
        st.session_state.answered = True
        st.session_state.show_explanation = True
        st.session_state.streak = 0
        st.rerun()

def results_section():
    """Display comprehensive quiz results with badges"""
    st.markdown("### 🏆 Quiz Results")
    
    questions = st.session_state.questions
    user_answers = st.session_state.user_answers
    total_q = len(questions)
    
    # Calculate scores
    score_data = calculate_score(user_answers, questions)
    percentage = score_data['percentage']
    is_perfect = percentage == 100
    
    # Check for perfect score
    if is_perfect and not st.session_state.perfect_score:
        st.session_state.perfect_score = True
    
    # Get badges
    badges = get_badges(percentage, st.session_state.max_streak, is_perfect)
    st.session_state.badges_earned = badges
    
    # Display badges
    st.markdown("### 🎖️ Badges Earned")
    badge_html = '<div class="badge-container">'
    for badge in badges:
        badge_html += f"""
        <div class="badge {badge['class']}" title="{badge['description']}">
            {badge['name']}
        </div>
        """
    badge_html += '</div>'
    st.markdown(badge_html, unsafe_allow_html=True)
    
    # Score summary cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="score-card">
            <h2 style='font-size: 2.5rem;'>{percentage:.1f}%</h2>
            <p>Overall Score</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); 
                    padding: 1.5rem; border-radius: 15px; color: white; text-align: center;
                    box-shadow: 0 4px 15px rgba(76,175,80,0.3);">
            <h2 style='font-size: 2.5rem;'>{score_data['total_correct']}</h2>
            <p>Correct Answers</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        incorrect = score_data['total_questions'] - score_data['total_correct']
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f44336 0%, #e53935 100%); 
                    padding: 1.5rem; border-radius: 15px; color: white; text-align: center;
                    box-shadow: 0 4px 15px rgba(244,67,54,0.3);">
            <h2 style='font-size: 2.5rem;'>{incorrect}</h2>
            <p>Incorrect Answers</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_time = sum(st.session_state.question_times) / len(st.session_state.question_times) if st.session_state.question_times else 0
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%); 
                    padding: 1.5rem; border-radius: 15px; color: white; text-align: center;
                    box-shadow: 0 4px 15px rgba(33,150,243,0.3);">
            <h2 style='font-size: 2.5rem;'>{avg_time:.1f}s</h2>
            <p>Avg. Time/Question</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Performance charts
    st.markdown("### 📊 Performance Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Accuracy by difficulty
        diff_data = score_data['accuracy_by_difficulty']
        if diff_data:
            diff_df = pd.DataFrame([
                {'Difficulty': diff.title(), 'Accuracy': value}
                for diff, value in diff_data.items()
                if value > 0 or score_data['difficulty_breakdown'][diff]['total'] > 0
            ])
            
            if not diff_df.empty:
                fig = px.bar(
                    diff_df,
                    x='Difficulty',
                    y='Accuracy',
                    color='Difficulty',
                    title='Accuracy by Difficulty Level',
                    labels={'Accuracy': 'Accuracy (%)'},
                    range_y=[0, 100],
                    color_discrete_map={
                        'Easy': '#28a745',
                        'Medium': '#ffc107',
                        'Hard': '#dc3545'
                    }
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12)
                )
                st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Time by difficulty
        time_data = score_data['avg_time_by_difficulty']
        if time_data:
            time_df = pd.DataFrame([
                {'Difficulty': diff.title(), 'Average Time (s)': value}
                for diff, value in time_data.items()
                if value > 0
            ])
            
            if not time_df.empty:
                fig = px.bar(
                    time_df,
                    x='Difficulty',
                    y='Average Time (s)',
                    color='Difficulty',
                    title='Average Time by Difficulty',
                    color_discrete_map={
                        'Easy': '#28a745',
                        'Medium': '#ffc107',
                        'Hard': '#dc3545'
                    }
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12)
                )
                st.plotly_chart(fig, use_container_width=True)
    
    # Question review
    st.markdown("### 📝 Question Review")
    
    for i, q in enumerate(questions):
        with st.expander(f"Question {i+1}: {q['question'][:100]}..."):
            st.markdown(f"**Question:** {q['question']}")
            
            for j, option in enumerate(q['options']):
                if j == q['correct']:
                    prefix = "✅ "
                    color = "green"
                elif j == user_answers[i]['selected'] and user_answers[i]['selected'] != q['correct']:
                    prefix = "❌ "
                    color = "red"
                else:
                    prefix = "   "
                    color = "black"
                
                st.markdown(f"<span style='color: {color};'>{prefix}{option}</span>", unsafe_allow_html=True)
            
            if user_answers[i]['selected'] is None:
                st.warning("⏰ Time's up! No answer provided.")
            elif user_answers[i]['selected'] == q['correct']:
                st.success("✅ Correct!")
            else:
                st.error(f"❌ Your answer: {q['options'][user_answers[i]['selected']]}")
            
            st.markdown(f"""
            <div class="explanation-box">
                <strong>💡 Explanation:</strong> {q['explanation']}
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"⏱️ Time taken: {user_answers[i]['time_taken']:.1f}s")
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Download results
        results_data = {
            'user_name': st.session_state.user_name,
            'user_email': st.session_state.user_email,
            'difficulty': st.session_state.difficulty,
            'score': score_data['total_correct'],
            'total_questions': score_data['total_questions'],
            'percentage': percentage,
            'avg_time': avg_time,
            'badges': [b['name'] for b in badges],
            'questions': questions,
            'answers': user_answers
        }
        
        json_str = json.dumps(results_data, indent=2)
        st.download_button(
            label="📥 Download Results",
            data=json_str,
            file_name=f"quiz_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col2:
        if st.button("📊 View Detailed Analysis", use_container_width=True):
            # Show additional statistics
            st.info("Check the charts above for detailed performance analysis!")
    
    with col3:
        if st.button("🔄 Start New Quiz", type="primary", use_container_width=True):
            reset_quiz()
            st.rerun()

# Main Application
def main():
    """Main application flow"""
    header_component()
    
    # Sidebar information
    with st.sidebar:
        st.markdown("### ℹ️ About SmartQuizzer")
        st.markdown("""
        SmartQuizzer is an adaptive AI-powered quiz generator that:
        
        - 📄 Creates questions from your study material
        - 🎯 Adapts difficulty to your level
        - ⏱️ Challenges you with timed questions
        - 📊 Provides detailed performance insights
        - 💡 Gives AI-generated explanations
        - 🏆 Awards badges for achievements
        """)
        
        st.markdown("---")
        
        if st.session_state.quiz_state != 'setup':
            st.markdown("### 📊 Current Session")
            st.markdown(f"**User:** {st.session_state.user_name}")
            st.markdown(f"**Difficulty:** {st.session_state.difficulty.title()}")
            st.markdown(f"**Questions:** {len(st.session_state.questions)}")
            st.markdown(f"**Score:** {st.session_state.score}/{len(st.session_state.questions)}")
            
            if st.session_state.max_streak > 0:
                st.markdown(f"**🔥 Best Streak:** {st.session_state.max_streak}")
            
            if st.button("🔄 Reset Session", use_container_width=True):
                reset_quiz()
                st.rerun()
        
        st.markdown("---")
        st.markdown("### 🔧 Technical Details")
        st.markdown("""
        - **AI Model:** GPT-3.5-Turbo
        - **Framework:** Streamlit
        - **Language:** Python
        - **Version:** 2.0
        """)
    
    # Main content based on state
    if st.session_state.quiz_state == 'setup':
        setup_section()
    elif st.session_state.quiz_state == 'playing':
        if not st.session_state.quiz_completed:
            quiz_playing_section()
        else:
            results_section()
    elif st.session_state.quiz_state == 'results':
        results_section()

if __name__ == "__main__":
    main()

from dotenv import load_dotenv
import os

load_dotenv()
import os
import json
from datetime import date, timedelta
from typing import List

import streamlit as st
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

# -------------------------------
# Page config
# -------------------------------
st.set_page_config(
    page_title="AI Study Plan Generator",
    page_icon="📚",
    layout="wide"
)

# -------------------------------
# Pydantic schema for structured output
# -------------------------------
class StudyDay(BaseModel):
    day: int = Field(description="Day number in the study plan")
    date: str = Field(description="Date in YYYY-MM-DD format")
    session_1: str = Field(description="First study session task")
    session_2: str = Field(description="Second study session task")
    session_3: str = Field(description="Third study session task")
    focus: str = Field(description="Main focus area for the day")
    daily_goal: str = Field(description="Daily target")
    extra: str = Field(description="Extra advice or task")

class StudyPlan(BaseModel):
    student_name: str
    exam_date: str
    study_level: str
    subjects: List[str]
    total_days: int
    motivation: str
    tips: List[str]
    plan: List[StudyDay]

# -------------------------------
# Helper functions
# -------------------------------
def get_days_left(exam_date: date) -> int:
    days = (exam_date - date.today()).days
    return max(days, 1)

def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")
    return genai.Client(api_key=api_key)

def generate_ai_study_plan(
    student_name: str,
    subjects_raw: str,
    exam_date: date,
    daily_hours: int,
    study_level: str,
    weak_topics: str,
    strong_topics: str,
) -> StudyPlan:
    client = get_gemini_client()

    subjects = [s.strip() for s in subjects_raw.split(",") if s.strip()]
    days_left = get_days_left(exam_date)

    prompt = f"""
Create a personalized, realistic, exam-focused study plan for a student.

Student name: {student_name}
Subjects: {", ".join(subjects)}
Exam date: {exam_date.isoformat()}
Days left: {days_left}
Available study hours per day: {daily_hours}
Current level: {study_level}
Weak topics: {weak_topics if weak_topics.strip() else "Not provided"}
Strong topics: {strong_topics if strong_topics.strip() else "Not provided"}

Instructions:
1. Generate a day-wise study plan for exactly {days_left} day(s).
2. Keep the plan practical and balanced.
3. Prioritize weak topics more.
4. Include revision, practice, and mock/self-test suggestions.
5. Make each session short, specific, and student-friendly.
6. Keep the language clear and simple.
7. Return the result in the required JSON structure only.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=(
                "You are an expert academic planning assistant. "
                "Generate precise, useful study plans for students."
            ),
            response_mime_type="application/json",
            response_schema=StudyPlan,
            temperature=0.7,
        ),
    )

    # SDK structured output helper
    if hasattr(response, "parsed") and response.parsed:
        return response.parsed

    # Fallback if parsed isn't populated for any reason
    text = response.text.strip()
    data = json.loads(text)
    return StudyPlan.model_validate(data)

def build_download_text(study_plan: StudyPlan) -> str:
    lines = []
    lines.append("PERSONALIZED AI STUDY PLAN")
    lines.append("=" * 50)
    lines.append(f"Student Name: {study_plan.student_name}")
    lines.append(f"Exam Date: {study_plan.exam_date}")
    lines.append(f"Study Level: {study_plan.study_level}")
    lines.append(f"Subjects: {', '.join(study_plan.subjects)}")
    lines.append(f"Total Days: {study_plan.total_days}")
    lines.append("")
    lines.append(f"Motivation: {study_plan.motivation}")
    lines.append("")
    lines.append("GENERAL TIPS:")
    for tip in study_plan.tips:
        lines.append(f"- {tip}")
    lines.append("")
    lines.append("=" * 50)

    for item in study_plan.plan:
        lines.append(f"Day {item.day} - {item.date}")
        lines.append(f"  Session 1: {item.session_1}")
        lines.append(f"  Session 2: {item.session_2}")
        lines.append(f"  Session 3: {item.session_3}")
        lines.append(f"  Focus: {item.focus}")
        lines.append(f"  Daily Goal: {item.daily_goal}")
        lines.append(f"  Extra: {item.extra}")
        lines.append("-" * 50)

    return "\n".join(lines)

# -------------------------------
# Styling
# -------------------------------
st.markdown(
    """
    <style>
        .main-title {
            font-size: 38px;
            font-weight: 700;
            text-align: center;
            margin-bottom: 8px;
        }
        .subtitle {
            text-align: center;
            color: #9aa4b2;
            margin-bottom: 24px;
        }
        .plan-card {
            padding: 18px;
            border-radius: 14px;
            background: #f8fafc;
            border: 1px solid #dbe4ee;
            margin-bottom: 14px;
            color: #111827;
        }
        .plan-card h4 {
            color: #111827;
            margin-bottom: 10px;
        }
        .plan-card p {
            color: #111827;
            margin: 6px 0;
        }
        .small-note {
            font-size: 14px;
            color: #94a3b8;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="main-title">📚 AI Personalized Study Plan Generator</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Built with Streamlit + Google Gemini API</div>',
    unsafe_allow_html=True
)

# -------------------------------
# Sidebar
# -------------------------------
st.sidebar.header("About Project")
st.sidebar.write(
    "This project uses Google Gemini API to generate a personalized day-wise study plan "
    "based on subjects, exam date, level, and weak/strong topics."
)
st.sidebar.info("Gen AI Project • LLM-based • Viva-ready")

with st.sidebar.expander("How to set API key"):
    st.code(
        'Windows PowerShell:\n$env:GEMINI_API_KEY="your_api_key_here"\n\n'
        'Command Prompt:\nset GEMINI_API_KEY=your_api_key_here',
        language="bash"
    )

# -------------------------------
# Main form
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    student_name = st.text_input("Student Name", placeholder="Enter your name")
    subjects = st.text_area(
        "Subjects (comma separated)",
        placeholder="Example: DBMS, Python, Operating System, AI"
    )
    exam_date = st.date_input("Exam Date", min_value=date.today())

with col2:
    daily_hours = st.slider("Daily Study Hours", 1, 12, 4)
    study_level = st.selectbox("Current Preparation Level", ["Beginner", "Intermediate", "Advanced"])
    weak_topics = st.text_input("Weak Topics (comma separated)", placeholder="Example: Joins, OOP, Recursion")
    strong_topics = st.text_input("Strong Topics (comma separated)", placeholder="Example: Basics, Theory")

generate_btn = st.button("Generate AI Study Plan", use_container_width=True)

if generate_btn:
    if not student_name.strip():
        st.warning("Please enter your name.")
    elif not subjects.strip():
        st.warning("Please enter at least one subject.")
    else:
        try:
            with st.spinner("Generating your AI study plan..."):
                study_plan = generate_ai_study_plan(
                    student_name=student_name,
                    subjects_raw=subjects,
                    exam_date=exam_date,
                    daily_hours=daily_hours,
                    study_level=study_level,
                    weak_topics=weak_topics,
                    strong_topics=strong_topics,
                )

            st.success("Your AI study plan is ready.")

            m1, m2, m3 = st.columns(3)
            m1.metric("Days Left", study_plan.total_days)
            m2.metric("Study Hours/Day", daily_hours)
            m3.metric("Subjects", len(study_plan.subjects))

            st.markdown("### Motivation")
            st.info(study_plan.motivation)

            st.markdown("### Smart Tips")
            for tip in study_plan.tips:
                st.write(f"- {tip}")

            st.markdown("### Generated Plan")
            for item in study_plan.plan:
                st.markdown(
                    f"""
                    <div class="plan-card">
                        <h4>Day {item.day} - {item.date}</h4>
                        <p><b>Session 1:</b> {item.session_1}</p>
                        <p><b>Session 2:</b> {item.session_2}</p>
                        <p><b>Session 3:</b> {item.session_3}</p>
                        <p><b>Focus:</b> {item.focus}</p>
                        <p><b>Daily Goal:</b> {item.daily_goal}</p>
                        <p><b>Extra:</b> {item.extra}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            download_text = build_download_text(study_plan)

            st.download_button(
                label="Download Study Plan",
                data=download_text,
                file_name="ai_study_plan.txt",
                mime="text/plain",
                use_container_width=True,
            )

            with st.expander("Show raw JSON output"):
                st.json(study_plan.model_dump())

        except Exception as e:
            st.error(f"Error: {e}")
            st.caption(
                "Check that your GEMINI_API_KEY is set correctly and your internet connection is working."
            )

st.markdown("---")
st.markdown(
    '<div class="small-note">Official Gemini setup uses the Google GenAI SDK (`google-genai`) '
    'with an API key via `GEMINI_API_KEY`. Structured JSON output is supported in the SDK. </div>',
    unsafe_allow_html=True
)
# Gen-ai-project
# AI-Powered Personalized Study Plan Generator

## Project Title

AI-Powered Personalized Study Plan Generator using Google Gemini API

## Brief One Line Summary

A Generative AI-based web application that creates personalized study schedules based on user inputs such as subjects, exam date, weak topics, and study hours.

## Overview

This project is designed to help students generate a customized study plan using Generative AI. The system takes user inputs such as subjects, exam date, preparation level, and weak topics, then sends them to a Large Language Model. The AI dynamically generates a structured day-wise study schedule along with smart tips and motivational guidance. The application is built using Streamlit for the frontend and integrates with the Google Gemini API for AI-based content generation.

## Problem Statement

Students often struggle to create effective study schedules tailored to their learning needs. Manual planning does not consider weak topics, available study hours, or exam deadlines. This leads to inefficient preparation and poor time management. Therefore, there is a need for an intelligent AI-based system that can automatically generate personalized study plans.

## Dataset

This project does not require a predefined dataset. The study plan is generated dynamically using Generative AI based on user inputs provided at runtime. The input fields act as real-time data for the model.

## Tools and Technologies

* Python
* Streamlit
* Google Gemini API
* Generative AI / Large Language Model
* python-dotenv (.env for API key)
* Pydantic (structured output validation)

## Methods

* Prompt Engineering for structured AI responses
* Generative AI using Gemini LLM
* JSON structured output parsing
* Dynamic UI generation using Streamlit
* User input-driven personalization

## Key Insights

* Generative AI can be used for educational productivity tools
* Personalized planning improves study efficiency
* AI can adapt to weak and strong topics dynamically
* LLM-based systems eliminate manual scheduling

## Dashboard / Model / Output

The application generates:

* Day-wise personalized study plan
* Session-wise study breakdown
* Smart study tips
* Motivation message
* Focus areas
* Downloadable study plan

The output is displayed in an interactive Streamlit dashboard.

## Project Structure

```bash
ai-study-plan-generator/
│── app.py
│── requirements.txt
│── README.md
│── .gitignore
│── .env (not uploaded)
│── images/
│    └── ui.png
```

## How to Run this project?

### Step 1: Clone Repository

```bash
git clone https://github.com/your-username/ai-study-plan-generator.git
cd ai-study-plan-generator
```

### Step 2: Install Requirements

```bash
pip install -r requirements.txt
```

### Step 3: Create .env file

```bash
GEMINI_API_KEY=your_api_key_here
```

### Step 4: Run Application

```bash
streamlit run app.py
```

## Results & Conclusion

The system successfully generates personalized study plans using Generative AI. It improves student productivity by focusing on weak topics and optimizing study time. The project demonstrates the practical use of LLMs in education and planning applications.

## Future Work

* Add login system
* Add progress tracking
* Add PDF export option
* Add performance analytics
* Deploy as web application
* Mobile app integration

## Author & Contact

**Name:** Arpit Singh

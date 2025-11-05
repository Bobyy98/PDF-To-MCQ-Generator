# mcq.py

import os
import json
import streamlit as st
from dotenv import load_dotenv
from text import select_text_from_pdf
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_mcq_questions_and_answers_from_pdf(pdf_file_path, difficulty, num_questions):
    try:
        pdf_text = select_text_from_pdf(pdf_file_path)
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return None, None, None

    prompt = f"""
You are an MCQ generator. Based ONLY on the text below, create {num_questions} {difficulty.lower()} level multiple-choice questions.

Return output in EXACT JSON LIST format ONLY:

[
  {{
    "question": "Question text?",
    "options": ["a) Option A", "b) Option B", "c) Option C", "d) Option D"],
    "answer": "b"
  }}
]

Text:
{pdf_text}
"""

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)

    output_text = response.text.strip()
    output_text = output_text.replace("```json", "").replace("```", "").strip()

    try:
        mcqs = json.loads(output_text)
    except json.JSONDecodeError:
        import re
        output_text = re.sub(r",\s*]", "]", output_text)
        output_text = re.sub(r",\s*}", "}", output_text)
        mcqs = json.loads(output_text)

    questions = [q["question"] for q in mcqs]
    options = [q["options"] for q in mcqs]
    answers = [q["answer"] for q in mcqs]

    return questions, options, answers

#app.py

import streamlit as st
import os
from dotenv import load_dotenv
from mcq import generate_mcq_questions_and_answers_from_pdf

load_dotenv()

def main():
    st.set_page_config(page_title="MCQ Generator", page_icon="📝", layout="wide")

    if "questions" not in st.session_state:
        st.title("🔖 PDF to MCQ Generator: Transforming PDFs into Interactive Quizzes")

        pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])
        num_questions = st.number_input("Enter the number of questions", min_value=1)
        difficulty_level = st.selectbox("Select difficulty level", ["Easy", "Medium", "Hard"])

        if st.button("Start Quiz 🚀"):
            if pdf_file:
                pdf_file_path = pdf_file.name
                with open(pdf_file_path, "wb") as f:
                    f.write(pdf_file.getbuffer())

                questions, options, answers = generate_mcq_questions_and_answers_from_pdf(
                    pdf_file_path, difficulty_level, num_questions)

                if questions is not None:
                    st.session_state["questions"] = questions
                    st.session_state["options"] = options
                    st.session_state["key_answers"] = answers
                    st.session_state["user_answers"] = [None] * len(questions)
                    st.session_state["attempted_questions"] = [False] * len(questions)

                    st.rerun()

    else:
        st.title("📝 MCQ Questions")

        for i, question in enumerate(st.session_state["questions"], start=1):
            choices = st.session_state["options"][i-1]
            st.markdown(f"**Q{i}. {question}**")
            user_answer = st.radio("Select an answer:", choices, key=f"q{i}")
            st.session_state["user_answers"][i-1] = user_answer[0].lower()
            st.session_state["attempted_questions"][i-1] = True
            st.write("---")

        attempted_count = sum(st.session_state["attempted_questions"])
        st.write(f"Attempted {attempted_count}/{len(st.session_state['attempted_questions'])} questions.")

        if st.button("Submit"):
            st.session_state["submitted"] = True

        if st.session_state.get("submitted", False):
            score = 0
            st.write("**Results:**")

            for i, (user_ans, correct_ans, attempted) in enumerate(
                zip(st.session_state["user_answers"], st.session_state["key_answers"], st.session_state["attempted_questions"]), start=1):

                if not attempted:
                    st.write(f"Question {i}: Not Attempted 🚫")
                else:
                    if user_ans.lower() == correct_ans.lower():
                        score += 1
                        st.write(f"Question {i}: ✅ Correct")
                    else:
                        st.write(f"Question {i}: ❌ Incorrect")

            st.write(f"### 🎉 Total Score: {score}/{len(st.session_state['questions'])}")

            st.subheader("✅ Answer Key:")
            for i, ans in enumerate(st.session_state["key_answers"], start=1):
                st.write(f"Q{i}: **{ans.upper()}**")

            if st.button("Back to Home"):
                st.session_state.clear()
                st.rerun()


if __name__ == "__main__":
    main()

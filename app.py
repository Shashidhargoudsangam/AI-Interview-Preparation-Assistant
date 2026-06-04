import streamlit as st
import requests

st.set_page_config(page_title="AI Interview Preparation Assistant")

st.title("AI Interview Preparation Assistant")

roles = [
    "Software Engineer",
    "Python Developer",
    "Java Developer",
    "Full Stack Developer",
    "Frontend Developer",
    "Backend Developer",
    "Data Analyst",
    "Data Scientist",
    "Machine Learning Engineer",
    "AI Engineer",
    "Cloud Engineer",
    "DevOps Engineer",
    "Cybersecurity Analyst",
    "UI/UX Designer",
    "Product Manager",
    "Business Analyst",
    "QA/Test Engineer",
    "Android Developer",
    "iOS Developer",
    "System Administrator"
]

if "question" not in st.session_state:
    st.session_state.question = ""

if "feedback" not in st.session_state:
    st.session_state.feedback = ""

if "roadmap" not in st.session_state:
    st.session_state.roadmap = ""

if "hr_question" not in st.session_state:
    st.session_state.hr_question = ""

role = st.selectbox("Select Career Role", roles)

difficulty = st.selectbox(
    "Select Difficulty Level",
    ["Beginner", "Intermediate", "Advanced"]
)

st.write(f"Selected Role: {role}")

if st.button("Generate Interview Question"):
    try:
        prompt = f"""
Generate one {difficulty} level interview question for a {role}.

Return only the question.
"""

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen3",
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        if response.status_code == 200:
            result = response.json()
            st.session_state.question = result["response"]
        else:
            st.error(f"Error: Status Code {response.status_code}")

    except Exception as e:
        st.error(f"Connection Error: {str(e)}")

if st.session_state.question:
    st.subheader("Interview Question")
    st.success(st.session_state.question)

    answer = st.text_area("Enter Your Answer")

    if st.button("Evaluate My Answer"):
        if answer.strip() == "":
            st.warning("Please enter an answer first.")
        else:
            try:
                eval_prompt = f"""
Interview Question:
{st.session_state.question}

Candidate Answer:
{answer}

Evaluate the answer and provide:

Score: X/10

Strengths:
- Point 1
- Point 2

Improvements:
- Point 1
- Point 2
"""

                eval_response = requests.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": "qwen3",
                        "prompt": eval_prompt,
                        "stream": False
                    },
                    timeout=120
                )

                if eval_response.status_code == 200:
                    eval_result = eval_response.json()
                    st.session_state.feedback = eval_result["response"]
                else:
                    st.error("Evaluation failed.")

            except Exception as e:
                st.error(f"Error: {str(e)}")

if st.session_state.feedback:
    st.subheader("AI Feedback")
    st.write(st.session_state.feedback)

st.divider()

if st.button("Generate Learning Roadmap"):
    try:
        roadmap_prompt = f"""
Give a short roadmap for becoming a {role}.

Include:
- 5 skills
- 3 projects
- 3 interview tips.

"""

        roadmap_response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen3",
                "prompt": roadmap_prompt,
                "stream": False
            },
            timeout=300
        )

        if roadmap_response.status_code == 200:
            roadmap_result = roadmap_response.json()
            st.session_state.roadmap = roadmap_result["response"]

    except Exception as e:
        st.error(str(e))

if st.session_state.roadmap:
    st.subheader("Learning Roadmap")
    st.write(st.session_state.roadmap)

st.divider()

if st.button("Generate HR Question"):
    try:
        hr_prompt = """
Generate one common HR interview question.

Return only the question.
"""

        hr_response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen3",
                "prompt": hr_prompt,
                "stream": False
            },
            timeout=120
        )

        if hr_response.status_code == 200:
            hr_result = hr_response.json()
            st.session_state.hr_question = hr_result["response"]

    except Exception as e:
        st.error(str(e))

if st.session_state.hr_question:
    st.subheader("HR Interview Question")
    st.success(st.session_state.hr_question)

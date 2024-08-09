import streamlit as st

# Define the quiz questions and choices
questions = [
    {
        "question": "What is the capital of France?",
        "choices": ["Paris", "London", "Rome", "Berlin"],
        "answer": "Paris"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "choices": ["Earth", "Mars", "Jupiter", "Saturn"],
        "answer": "Mars"
    },
    {
        "question": "What is the largest ocean on Earth?",
        "choices": ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"],
        "answer": "Pacific Ocean"
    }
]

# Function to display the quiz
def display_quiz():
    st.title("Simple Quiz App")

    # Initialize the session state
    if 'score' not in st.session_state:
        st.session_state.score = 0
        st.session_state.current_question = 0
        st.session_state.answers = []

    # Show the current question
    if st.session_state.current_question < len(questions):
        q = questions[st.session_state.current_question]
        st.write(q["question"])

        # Radio buttons for choices
        user_answer = st.radio(
            "Choose your answer:",
            q["choices"],
            key=st.session_state.current_question
        )

        if st.button("Submit"):
            # Check the answer
            if user_answer == q["answer"]:
                st.session_state.score += 1
            st.session_state.answers.append(user_answer)
            st.session_state.current_question += 1

            # Show the next question or finish
            if st.session_state.current_question < len(questions):
                st.experimental_rerun()
            else:
                st.write(f"Quiz completed! Your score is {st.session_state.score}/{len(questions)}.")
                st.write("Answers:")
                for i, ans in enumerate(st.session_state.answers):
                    st.write(f"Q{i+1}: {questions[i]['question']}")
                    st.write(f"Your answer: {ans}")
                    st.write(f"Correct answer: {questions[i]['answer']}")
                st.button("Restart Quiz", on_click=reset_quiz)

    else:
        st.write(f"Quiz completed! Your score is {st.session_state.score}/{len(questions)}.")
        st.write("Answers:")
        for i, ans in enumerate(st.session_state.answers):
            st.write(f"Q{i+1}: {questions[i]['question']}")
            st.write(f"Your answer: {ans}")
            st.write(f"Correct answer: {questions[i]['answer']}")
        st.button("Restart Quiz", on_click=reset_quiz)

def reset_quiz():
    st.session_state.score = 0
    st.session_state.current_question = 0
    st.session_state.answers = []
    st.experimental_rerun()

# Run the quiz app
if __name__ == "__main__":
    display_quiz()


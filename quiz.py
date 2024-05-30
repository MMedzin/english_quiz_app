import streamlit as st
import json
import random
from pathlib import Path


@st.cache_data
def get_questions():
    with open(Path(st.session_state["question_source"]), "r") as f:
        questions = json.load(f)
    return questions


st.set_page_config(layout="wide")

st.title("English Quiz")

question_sources = ["questions_set1.json", "questions_set2.json"]
question_source = st.selectbox("Select question source", question_sources, index=1, key="question_source")

questions = get_questions()


if ("quiz_on" not in st.session_state or not st.session_state.quiz_on) and (
    "quiz_end" not in st.session_state or not st.session_state.quiz_end
):
    number_of_words = st.number_input("Number of words to practice", min_value=1, max_value=len(questions), value=10)
    st.session_state.words = random.sample(list(questions.keys()), number_of_words)
    start_quiz = st.button("Start quiz")
else:
    start_quiz = False

if start_quiz:
    st.write("Quiz started")
    st.session_state.quiz_on = True
    st.session_state.repeat_phase = False
    st.session_state.words_to_repeat = []
    st.session_state.current_word_idx = 0
    st.session_state.new_word = True
    st.session_state.evaluation = False
    st.rerun()

if "quiz_on" in st.session_state and st.session_state.quiz_on:
    if not st.session_state.repeat_phase:
        word = st.session_state.words[st.session_state.current_word_idx]
        if st.session_state.new_word:
            st.session_state.question, st.session_state.answer = random.choice(questions[word])
        st.write(st.session_state.question)
        if st.session_state.new_word:
            st.session_state.evaluation = True
            st.session_state.new_word = False
            st.text_input("Your answer (click enter to submit)", key="user_answer")
        else:
            if st.session_state.evaluation:
                st.session_state.correct = (
                    st.session_state.user_answer.lower().strip() == st.session_state.answer.lower().strip()
                )
                if not st.session_state.correct:
                    st.session_state.words_to_repeat.append(word)
                st.session_state.evaluation = False
                st.rerun()
            else:
                if st.session_state.correct:
                    st.write("It's correct. Well done!")
                else:
                    st.write("Good try, but it's not the one. Keep going!")
                    st.write(f"Correct answer: {st.session_state.answer}")
                next_question = st.button(
                    "Next question"
                    if st.session_state.current_word_idx < len(st.session_state.words) - 1
                    or st.session_state.words_to_repeat
                    else "Finish quiz"
                )
                if next_question:
                    st.session_state.current_word_idx += 1
                    st.session_state.new_word = True
                    if st.session_state.current_word_idx == len(st.session_state.words):
                        st.session_state.repeat_phase = True
                        st.session_state.current_word_idx = 0
                    st.rerun()
    else:
        if st.session_state.words_to_repeat:
            word = st.session_state.words_to_repeat[st.session_state.current_word_idx]
            if st.session_state.new_word:
                st.session_state.question, st.session_state.answer = random.choice(questions[word])
            st.write(st.session_state.question)
            if st.session_state.new_word:
                st.session_state.evaluation = True
                st.session_state.new_word = False
                st.text_input("Your answer (click enter to submit)", key="user_answer")
            else:
                if st.session_state.evaluation:
                    st.session_state.correct = (
                        st.session_state.user_answer.lower().strip() == st.session_state.answer.lower().strip()
                    )
                    st.session_state.evaluation = False
                    st.rerun()
                else:
                    if st.session_state.correct:
                        st.write("It's correct. Well done!")
                    else:
                        st.write("Good try, but it's not the one. Keep going!")
                        st.write(f"Correct answer: {st.session_state.answer}")
                    next_question = st.button(
                        "Next question"
                        if st.session_state.current_word_idx < len(st.session_state.words_to_repeat) - 1
                        else "Finish quiz"
                    )
                    if next_question:
                        st.session_state.current_word_idx += 1
                        st.session_state.new_word = True
                        if st.session_state.current_word_idx == len(st.session_state.words_to_repeat):
                            st.write("Quiz finished")
                            st.balloons()
                            st.session_state.repeat_phase = False
                            st.session_state.quiz_on = False
                            st.session_state.quiz_end = True
                            st.session_state.current_word_idx = 0
                            st.session_state.new_word = True
                            st.session_state.evaluation = False
                            st.session_state.words_to_repeat = []
                            st.session_state.words = []
                        st.rerun()
        else:
            st.write("Quiz finished")
            st.balloons()
            st.session_state.repeat_phase = False
            st.session_state.quiz_on = False
            st.session_state.quiz_end = True
            st.session_state.current_word_idx = 0
            st.session_state.new_word = True
            st.session_state.evaluation = False
            st.session_state.words_to_repeat = []
            st.session_state.words = []
            st.rerun()

if "quiz_end" in st.session_state and st.session_state.quiz_end:
    st.write("Quiz finished")
    st.balloons()
    st.session_state.quiz_end = False
    st.button("Start again")

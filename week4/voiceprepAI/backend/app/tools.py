# app/tools.py

from datetime import datetime
import json
import os

# JSON file to store interview scores

BASE_DIR = os.path.dirname(__file__)

SCORES_FILE = os.path.join(
    BASE_DIR,
    "interview_scores.json",
)


def get_current_time():
    """
    Returns the current local time.
    """
    return {
        "current_time": datetime.now().strftime("%I:%M:%S %p")
    }


def get_interview_question(topic="Python"):
    """
    Returns a mock interview question based on the topic.
    """

    questions = {
        "Python": "Explain the difference between a list and a tuple in Python.",
        "DBMS": "What is normalization? Why is it used?",
        "OOP": "What is polymorphism? Give a real-world example.",
        "DSA": "What is the difference between BFS and DFS?",
        "OS": "What is a deadlock and how can it be prevented?"
    }

    question = questions.get(
        topic,
        "Tell me about yourself."
    )

    return {
        "topic": topic,
        "question": question
    }


def save_interview_score(score, topic):
    """
    Saves an interview score locally.
    """

    data = []

    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []

    data.append({
        "topic": topic,
        "score": score,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    with open(SCORES_FILE, "w") as f:
        json.dump(data, f, indent=4)

    return {
        "message": "Interview score saved successfully."
    }
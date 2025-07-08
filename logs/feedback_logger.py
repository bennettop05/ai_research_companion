import json
from datetime import datetime

def log_feedback(question, answer, feedback):
    log = {
        "question": question,
        "answer": answer,
        "feedback": feedback,
        "timestamp": str(datetime.now())
    }
    try:
        with open("logs/feedback_log.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data.append(log)

    with open("logs/feedback_log.json", "w") as f:
        json.dump(data, f, indent=4)

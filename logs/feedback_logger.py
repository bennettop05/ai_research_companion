import json
import os

LOG_FILE = "logs/feedback_log.json"

def log_feedback(question, answer, feedback):
    os.makedirs("logs", exist_ok=True)
    log_entry = {"question": question, "answer": answer, "feedback": feedback}
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []
    data.append(log_entry)
    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)

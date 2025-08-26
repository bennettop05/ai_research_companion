import json
import os
from datetime import datetime

TRACE_FILE = "logs/trace_log.json"

def log_trace(query, step, context, output):
    os.makedirs("logs", exist_ok=True)
    entry = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "step": step,
        "context": context,
        "output": output
    }
    if os.path.exists(TRACE_FILE):
        with open(TRACE_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []
    data.append(entry)
    with open(TRACE_FILE, "w") as f:
        json.dump(data, f, indent=2)

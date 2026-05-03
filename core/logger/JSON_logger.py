import json
from dataclasses import asdict
from datetime import datetime

def log_snapshot(snapshot, filepath = "logs/system.jsonl"):

    data = asdict(snapshot)
    data["timestamp_iso"] = datetime.fromtimestamp(snapshot.timestamp).isoformat()

    with open(filepath, "a") as f:
        f.write(json.dumps(data) + "\n")
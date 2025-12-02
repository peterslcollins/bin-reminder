import os
from datetime import datetime


def append_log(file_path, message):
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().isoformat()} - {message}\n")


def was_notified_today(log_file):
    """Check if notification was sent today (based on log)."""
    if not os.path.exists(log_file):
        return False

    today_str = datetime.now().date().isoformat()
    with open(log_file, "r", encoding="utf-8") as f:
        for line in reversed(f.readlines()):
            if today_str in line:
                return True
    return False

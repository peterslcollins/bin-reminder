import json
import os

NOTIFY_LOG = "logs/sent_notifications.log"
ERROR_LOG = "logs/error.log"

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.json")


def load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

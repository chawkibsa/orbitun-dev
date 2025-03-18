import json
import os

CONFIG_FILE = "/etc/edr-agent.conf"

def load_config():
    """ Load configuration file. """
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_config(data):
    """ Save configuration file. """
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

import logging
from datetime import datetime

LOG_FILE = "/var/log/edr-agent.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def log_message(message, level="info"):
    """ Log messages with different levels. """
    getattr(logging, level)(message)

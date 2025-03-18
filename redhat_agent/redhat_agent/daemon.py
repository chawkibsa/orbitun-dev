import signal
import sys
from daemon import DaemonContext
from .main import run_agent
from .logger import log_message

def signal_handler(signum, frame):
    """ Handle termination signals. """
    log_message("Agent shutting down")
    sys.exit(0)

def start_daemon():
    """ Run the agent as a daemon. """
    with DaemonContext():
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)
        run_agent()

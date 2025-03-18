from .registration import register_agent
from .heartbeat import send_heartbeat
from .policy import apply_policies
from .logger import log_message

def run_agent():
    """ Run the EDR agent process. """
    log_message("Starting EDR Agent...")
    agent_id = register_agent()
    if agent_id:
        send_heartbeat()
        apply_policies()

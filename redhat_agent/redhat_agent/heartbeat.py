import time
import requests
from .config import load_config
from .logger import log_message
from .utils import get_system_info

EDR_SERVER = "https://edr.example.com/api"

def send_heartbeat():
    """ Send a periodic heartbeat to the EDR server. """
    agent_id = load_config().get("agent_id")
    if not agent_id:
        log_message("Agent not registered, exiting...", "error")
        return

    while True:
        system_info = get_system_info()
        payload = {
            "agent_id": agent_id,
            "cpu_usage": subprocess.getoutput("top -bn1 | grep 'Cpu' | awk '{print $2}'"),
            "ram_usage": subprocess.getoutput("free -m | awk 'NR==2{print $3}'"),
            "running_processes": subprocess.getoutput("ps -e -o comm=").split("\n"),
        }

        try:
            response = requests.post(f"{EDR_SERVER}/heartbeat", json=payload)
            log_message(f"Heartbeat sent: {response.status_code}")
        except Exception as e:
            log_message(f"Failed to send heartbeat: {str(e)}", "error")

        time.sleep(60)

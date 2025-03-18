import requests
from .config import load_config, save_config
from .utils import get_system_info, generate_fingerprint
from .logger import log_message

EDR_SERVER = "http://127.0.0.1:8000/api"

def register_agent():
    """ Register the agent with the EDR server. """
    info = get_system_info()
    fingerprint = generate_fingerprint(info)

    config = load_config()
    if "agent_id" in config:
        return config["agent_id"]

    #payload = {
    #    "fingerprint": fingerprint,
    #    "hostname": info["hostname"],
    #    "mac_address": info["mac_address"],
    #    "os": info["os"],
    #    "public_ip": info["public_ip"]
    #}

    payload = {
    "is_persistent": True,
    "status": "offline",
    "last_heartbeat": "12-01-2025",
    "created_at": "12-01-2025",
    "updated_at": "12-01-2025"
    }

    #response = requests.post(f"{EDR_SERVER}/register", json=payload).json()
    print("payload sent")
    print(payload)
    
    if response.get("status") == "registered":
        config["agent_id"] = response["agent_id"]
        save_config(config)
        log_message(f"Agent registered with ID: {config['agent_id']}")
        return response["agent_id"]
    
    log_message("Registration failed", "error")
    return None

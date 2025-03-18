import subprocess
import hashlib
from uuid import getnode
import requests

def get_system_info():
    """ Collect system information for fingerprinting. """
    return {
    "is_persistent": True,
    "status": "offline",
    "last_heartbeat": "12-01-2025",
    "created_at": "12-01-2025",
    "updated_at": "12-01-2025"
    }

def generate_fingerprint(info):
    """ Generate a unique fingerprint for the system. """
    #unique_string = f"{info['cpu_id']}-{info['motherboard_serial']}-{info['bios_uuid']}"
    unique_string = "Random-text"
    return hashlib.sha256(unique_string.encode()).hexdigest()

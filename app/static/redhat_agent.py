import os
#import uuid
import requests
import time
import psutil
import socket
#from datetime import datetime

# Configuration
BACKEND_URL = "http://localhost:8000/api"
#AGENT_ID = str(uuid.uuid4())  # Unique ID for the agent
HEARTBEAT_INTERVAL = 60  # Seconds

def get_network_interfaces():
    ipv4_addresses = []
    ipv6_addresses = []
    mac_addresses = []
    address_schema = {"address":""}

    # Get network interface details
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET:  # IPv4
                address_schema["address"] = addr.address
                ipv4_addresses.append(address_schema)
            elif addr.family == socket.AF_INET6:  # IPv6
                address_schema["address"] = addr.address.split('%')[0]
                ipv6_addresses.append(address_schema)  # Remove scope ID if present
            elif addr.family == psutil.AF_LINK:  # MAC Address
                address_schema["address"] = addr.address
                mac_addresses.append(address_schema)

    return ipv4_addresses, ipv6_addresses, mac_addresses
'''
def get_system_info():
    """Collect system information for endpoint registration."""
    return {
        "name": "My Endpoint",
        "description": "User-friendly description",
        "hostname": os.uname().nodename,
        "device_type": "Workstation",  # or "Server"
        "os_type": os.uname().sysname,
        "os_version": os.uname().release,
        "ipv4": ["192.168.1.100"],  # Replace with actual IPs
        "ipv6": [],  # Replace with actual IPs
        "mac": ["00:1A:2B:3C:4D:5E"]  # Replace with actual MACs
    }
'''

def register_agent():
    payload = {
    "is_persistent": True,
    "status": "offline",
    "last_heartbeat": "12-01-2025",
    "created_at": "12-01-2025",
    "updated_at": "12-01-2025"
    }

    try:
        response = requests.post(f"{BACKEND_URL}/agents/register", json=payload)
        response.raise_for_status()
        print("Agent registered successfully")
    except Exception as e:
        print(f"Failed to register agent: {str(e)}")
        raise

def register_endpoint():
    """Register the agent with the backend server."""
    #system_info = get_system_info()

    ipv4_list, ipv6_list, mac_list = get_network_interfaces()
    
    payload = {
    "name": "My Endpoint",
    "description": "User-friendly description",
    "hostname": os.uname().nodename,
    "device_type": "Workstation",
    "os_type": os.uname().sysname, 
    "os_version": os.uname().release, 
    "ipv4": ipv4_list, 
    "ipv6": ipv6_list,
    "mac": mac_list,
    "created_at": "12-01-2025",
    "updated_at": "12-01-2025"
    } 
    try:
        response = requests.post(f"{BACKEND_URL}/endpoints/register", json=payload)
        response.raise_for_status()
        print("Endpoint registered successfully")
    except Exception as e:
        print(f"Failed to register agent: {str(e)}")
        raise

def send_heartbeat():
    """Send a heartbeat to the backend server."""
    try:
        response = requests.post(
            f"{BACKEND_URL}/heartbeat",
            json={"agent_id": AGENT_ID, "status": "online"},
        )
        response.raise_for_status()
        print("Heartbeat sent successfully")
    except Exception as e:
        print(f"Failed to send heartbeat: {str(e)}")
        raise

def main():
    # Register the agent
    register_agent()

    
    register_endpoint()

    # Start the heartbeat loop
    #while True:
    #    try:
    #        print("send heartbeat")
    #        #send_heartbeat()
    #    except Exception as e:
    #        print(f"Heartbeat failed, retrying...: {str(e)}")
    #    time.sleep(HEARTBEAT_INTERVAL)

if __name__ == "__main__":
    main()
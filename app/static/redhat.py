import json
import subprocess
import os
import psutil
import datetime

def get_system_uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
    return str(datetime.timedelta(seconds=uptime_seconds))

def get_logged_in_users():
    users = []
    for user in psutil.users():
        users.append({
            "name": user.name,
            "terminal": user.terminal,
            "host": user.host,
            "started": datetime.datetime.fromtimestamp(user.started).strftime('%Y-%m-%d %H:%M:%S')
        })
    return users

def get_running_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_info']):
        try:
            process_info = proc.info
            processes.append({
                "pid": process_info['pid'],
                "name": process_info['name'],
                "username": process_info['username'],
                "cpu_percent": process_info['cpu_percent'],
                "memory_rss": process_info['memory_info'].rss,
                "memory_vms": process_info['memory_info'].vms
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return processes

def networks_network_interfaces():
    ipv4_addresses = []
    ipv6_addresses = []
    mac_addresses = []

    # Get network interface details
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET:  # IPv4
                ipv4_addresses.append(addr.address)
            elif addr.family == socket.AF_INET6:  # IPv6
                ipv6_addresses.append(addr.address.split('%')[0])  # Remove scope ID if present
            elif addr.family == psutil.AF_LINK:  # MAC Address
                mac_addresses.append(addr.address)

    return ipv4_addresses, ipv6_addresses, mac_addresses

def get_network_connections():
    connections = []
    for conn in psutil.net_connections(kind='inet'):
        connections.append({
            "fd": conn.fd,
            "family": conn.family,
            "type": conn.type,
            "local_address": conn.laddr,
            "remote_address": conn.raddr,
            "status": conn.status,
            "pid": conn.pid
        })
    return connections

def get_open_files():
    open_files = []
    for proc in psutil.process_iter(['pid', 'open_files']):
        try:
            process_info = proc.info
            if process_info['open_files']:
                for file in process_info['open_files']:
                    open_files.append({
                        "pid": process_info['pid'],
                        "path": file.path,
                        "fd": file.fd
                    })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return open_files

def collect_telemetry():
    # Calling the function
    ipv4_list, ipv6_list, mac_list = get_ip_and_mac_addresses()
    telemetry_data = {
        "system_uptime": get_system_uptime(),
        "logged_in_users": get_logged_in_users(),
        "running_processes": get_running_processes(),
        "network_connections": get_network_connections(),
        "ipv4_network_interfaces": ipv4_list,
        "ipv6_network_interfaces": ipv6_list,
        "mac_interfaces": mac_list,
        "open_files": get_open_files()
    }
    return telemetry_data

if __name__ == "__main__":
    telemetry = collect_telemetry()
    print(json.dumps(telemetry, indent=4))
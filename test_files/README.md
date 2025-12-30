# Test Files for Automata Malware Detector

This directory contains test files for demonstrating the malware detection system.

## Test Files Overview

| File | Description | Expected Detections |
|------|-------------|---------------------|
| `suspicious_python_script.py` | General malicious Python code | High (8-10 matches) |
| `backdoor_script.py` | Reverse shell backdoor simulation | High (6-8 matches) |
| `shell_injection.sh` | Shell script with malicious commands | High (10+ matches) |
| `data_exfiltration.py` | Data theft and exfiltration patterns | Medium-High (6-8 matches) |
| `clean_script.py` | Legitimate code with NO malware | Zero or very low |
| `ransomware_simulator.py` | Ransomware behavior patterns | Very High (12+ matches) |
| `mixed_content.py` | Mix of legitimate and suspicious code | Medium (4-6 matches) |

## How to Use These Files

### Step 1: Run the Application
```bash
cd "c:/Users/IBBI/Desktop/automata project/automata_malware_detector"
python main.py
```

### Step 2: Scan a Test File
1. Click **Browse** button in the GUI
2. Navigate to `test_files/` directory
3. Select any test file (e.g., `suspicious_python_script.py`)
4. Click **Scan** button
5. Review the detection results in the table

### Step 3: Compare Results

**High Detection Files** (Good for demonstrating detection capabilities):
- `ransomware_simulator.py` - Most detections
- `shell_injection.sh` - Many shell-based patterns
- `suspicious_python_script.py` - Various Python malware patterns

**Low Detection Files** (Good for showing false positive control):
- `clean_script.py` - Should have zero or minimal detections

**Mixed Detection Files** (Good for realistic scenarios):
- `mixed_content.py` - Shows selective detection
- `data_exfiltration.py` - Moderate detections

## Expected Signatures to Detect

Based on the default `signatures.py`:

- ✅ `eval\(` - Dynamic code execution
- ✅ `exec\(` - Code execution
- ✅ `base64\.b64decode\(` - Decoding (often used for obfuscation)
- ✅ `rm -rf` - Destructive file deletion
- ✅ `powershell` - PowerShell execution
- ✅ `http://` - HTTP URLs (potential C&C communication)

## Customization

You can create your own test files by:

1. Creating a new `.py`, `.sh`, or `.txt` file
2. Adding patterns from `signatures.py`
3. Scanning the file to see detections

## Safety Note

⚠️ **IMPORTANT**: All files in this directory are **SIMULATIONS** for educational purposes. They do not contain actual malware and will not harm your system. However, some contain code patterns that antivirus software might flag.

## Example Scan Output

When scanning `suspicious_python_script.py`, you should see results like:

| SIGNATURE | REGEX | LINE | START | END | SNIPPET |
|-----------|-------|------|-------|-----|---------|
| base64_decode | base64\.b64decode\( | 12 | 18 | 36 | base64.b64decode( |
| eval_call | eval\( | 16 | 0 | 5 | eval( |
| exec_call | exec\( | 20 | 0 | 5 | exec( |
| http | http:// | 23 | 15 | 22 | http:// |
| powershell | powershell | 26 | 21 | 31 | powershell |
| rm_rf | rm -rf | 29 | 11 | 17 | rm -rf |

## Troubleshooting

**No detections found?**
- Verify `signatures.py` contains the patterns
- Check that signatures compiled successfully (look at terminal output)
- Ensure you selected the correct file

**Too many/few detections?**
- Adjust patterns in `signatures.py` to be more/less specific
- Add new signatures for additional patterns

## Next Steps

After testing with these files:
1. Create your own test files with specific patterns
2. Modify `signatures.py` to detect custom patterns
3. Test with real code files (be careful with production code)

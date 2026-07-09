
# Malware Detection Tool

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Cybersecurity](https://img.shields.io/badge/Cybersecurity-FF6F00?style=for-the-badge&logo=hackaday&logoColor=white)
![Automata Theory](https://img.shields.io/badge/Automata%20Theory-8B5CF6?style=for-the-badge&logo=quantum&logoColor=white)

**An educational malware detection tool that applies automata theory concepts — regex pattern matching, NFA construction, DFA conversion, Thompson's construction, and the subset construction algorithm — to detect known malware signatures.**

---

## Features

- **Regex-Based Signature Matching** — Scan files against a library of malware signatures defined as regular expressions
- **NFA Construction** — Build Nondeterministic Finite Automata from regex patterns using Thompson's construction algorithm
- **DFA Conversion** — Convert NFAs to deterministic finite automata via the subset construction (powerset) algorithm
- **Django REST API** — Expose detection capabilities over HTTP with a full RESTful interface
- **Web Frontend** — Upload and scan files through a browser-based UI
- **Tkinter GUI** — Cross-platform desktop interface for offline scanning
- **Extensible Signature Library** — Easily add new malware signatures in `signatures.py`

## Concepts

| Concept | Description |
|---|---|
| **Regex** | Malware signatures are expressed as regular expressions, providing a human-readable and mathematically rigorous pattern language |
| **NFA** | A Nondeterministic Finite Automaton (NFA) is constructed from each regex using Thompson's construction — an NFA can be in multiple states at once, making it compact but harder to simulate directly |
| **DFA** | A Deterministic Finite Automaton (DFA) is derived from the NFA via the subset construction algorithm — a DFA is in exactly one state at any time, enabling efficient O(n) scanning |
| **Thompson Construction** | A recursive algorithm that builds an NFA from a regular expression by composing smaller automata for sub-expressions using ε-transitions |
| **Subset Construction** | Also called the powerset construction — converts an NFA into an equivalent DFA where each DFA state represents a set of NFA states reachable on a given input |

## Tech Stack

- **Language:** Python 3.10+
- **Web Framework:** Django 5 + Django REST Framework
- **Frontend:** HTML, CSS, JavaScript (static files)
- **Desktop GUI:** Tkinter
- **Automata Core:** Pure Python (no external dependencies for automata algorithms)

## Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/malware-detection-tool.git
cd malware-detection-tool

# Install dependencies
pip install -r requirements.txt

# Run the CLI scanner
python main.py

# Or start the web server
python manage.py runserver

# Or launch the desktop GUI
python gui/app.py
```

## Project Structure

```
malware-detection-tool/
├── automata/                  # Core automata algorithms
│   ├── __init__.py
│   ├── regex_parser.py        # Regex to NFA via Thompson's construction
│   ├── nfa.py                 # NFA data structure and simulation
│   ├── dfa.py                 # DFA data structure (subset construction)
│   └── engine.py              # Scanning engine (orchestrates NFA/DFA)
├── api/                       # Django REST API
│   ├── __init__.py
│   ├── apps.py
│   ├── urls.py
│   └── views.py
├── backend/                   # Django project configuration
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── frontend/                  # Web frontend
│   ├── index.html
│   └── static/
├── gui/                       # Tkinter desktop GUI
│   ├── __init__.py
│   └── app.py
├── test_files/                # Sample files for testing
├── main.py                    # CLI entry point
├── manage.py                  # Django management script
├── signatures.py              # Malware signature definitions (regex)
├── requirements.txt           # Python dependencies
├── start_server.bat           # Windows batch launcher
└── README.md                  # This file
```

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

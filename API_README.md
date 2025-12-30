# Automata-Based Malware Detector - Django REST API

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Django Server**
   ```bash
   python manage.py runserver 8000
   ```

3. **Open Your Browser**
   Navigate to: `http://localhost:8000`

That's it! The application should now be running.

---

## 📁 Project Structure

```
automata_malware_detector/
│
├── backend/                    # Django configuration
│   ├── __init__.py
│   ├── settings.py            # Django settings
│   ├── urls.py                # URL routing
│   └── wsgi.py                # WSGI configuration
│
├── api/                        # REST API application
│   ├── __init__.py
│   ├── apps.py                # App configuration
│   ├── urls.py                # API endpoints
│   └── views.py               # API views (preserves automata logic)
│
├── automata/                   # Core automata logic (UNCHANGED)
│   ├── regex_parser.py        # Regex tokenization
│   ├── nfa.py                 # Thompson's Construction
│   ├── dfa.py                 # Subset Construction & Simulation
│   └── engine.py              # Scanning engine
│
├── frontend/                   # Web frontend
│   ├── index.html             # Main HTML page
│   └── static/
│       ├── css/
│       │   └── style.css      # Modern styling
│       └── js/
│           └── app.js         # Frontend logic
│
├── gui/                        # Old Tkinter GUI (deprecated)
├── test_files/                 # Test malware samples
├── signatures.py               # Malware signature database
├── manage.py                   # Django management script
└── requirements.txt            # Python dependencies
```

---

## 🔌 API Endpoints

### Health Check
```
GET /api/health/
```
Response:
```json
{
  "status": "healthy",
  "signatures_loaded": 6,
  "version": "1.0.0"
}
```

### Get Signatures
```
GET /api/signatures/
```
Response:
```json
{
  "success": true,
  "count": 6,
  "signatures": [
    {
      "name": "eval_call",
      "regex": "eval\\(",
      "description": "Detects eval() function calls (dynamic code execution)"
    }
  ]
}
```

### Scan Text
```
POST /api/scan/text/
Content-Type: application/json

{
  "text": "eval(user_input)"
}
```
Response:
```json
{
  "success": true,
  "matches_found": 1,
  "matches": [
    {
      "signature_name": "eval_call",
      "regex": "eval\\(",
      "line_no": 1,
      "start_idx": 0,
      "end_idx": 5,
      "snippet": "eval(",
      "description": "Detects eval() function calls"
    }
  ],
  "total_lines": 1,
  "risk_level": "low"
}
```

### Scan File
```
POST /api/scan/file/
Content-Type: multipart/form-data

file: <binary file data>
```
Response:
```json
{
  "success": true,
  "filename": "malware.py",
  "matches_found": 3,
  "matches": [...],
  "total_lines": 50,
  "preview": ["line 1", "line 2", ...],
  "risk_level": "high"
}
```

### Get Statistics
```
GET /api/stats/
```
Response:
```json
{
  "success": true,
  "stats": {
    "total_signatures": 6,
    "compiled_signatures": 6,
    "supported_file_types": ["txt", "py", "sh", "js", ...],
    "max_file_size_mb": 16
  }
}
```

---

## 🎨 Frontend Features

### Modern Design
- ✨ Glassmorphism UI
- 🌈 Gradient backgrounds
- 🎭 Smooth animations
- 📱 Fully responsive
- 🌙 Dark theme

### Functionality
- 📤 Drag & drop file upload
- 🔍 Real-time scanning
- 📊 Visual risk indicators
- 📋 Detailed match results
- 🏷️ Signature viewer

---

## 🧪 Testing

### Test with Clean Files
```bash
# Navigate to test_files directory
cd test_files

# These files should return 0 matches:
- clean_calculator.py
- clean_data_processor.py
- clean_web_server.py
- clean_file_organizer.py
- clean_student_manager.py
- clean_text_analyzer.py
```

### Test with Malicious Files
```bash
# These files should detect threats:
- suspicious_python_script.py (3+ matches)
- backdoor_script.py (2+ matches)
- ransomware_simulator.py (4+ matches)
- shell_injection.sh (3+ matches)
```

---

## 🔧 Configuration

### Adding New Signatures

Edit `signatures.py`:
```python
SIGNATURES = {
    # Existing signatures...
    
    # Add your new signature:
    "os_system": "os\\.system\\(",
    "subprocess": "subprocess\\.",
}
```

Restart the server to load new signatures.

### Adjusting File Upload Limits

Edit `backend/settings.py`:
```python
FILE_UPLOAD_MAX_MEMORY_SIZE = 16 * 1024 * 1024  # Change to desired size
ALLOWED_FILE_EXTENSIONS = ['txt', 'py', ...]  # Add/remove extensions
```

---

## 🐛 Troubleshooting

### Server Won't Start
```bash
# Check if port 8000 is already in use
netstat -ano | findstr :8000

# Use a different port
python manage.py runserver 8080
```

### API Connection Failed
- Ensure the Django server is running
- Check that you're accessing `http://localhost:8000`
- Verify no firewall is blocking the connection

### File Upload Fails
- Check file size (max 16MB)
- Verify file extension is allowed
- Check console for error messages

---

## 📚 Architecture

### Backend (Django REST Framework)
- **No changes to automata logic** - All existing NFA/DFA code preserved
- RESTful API endpoints
- File upload handling
- CORS enabled for frontend

### Frontend (Vanilla JavaScript)
- Modern ES6+ JavaScript
- Fetch API for HTTP requests
- No frameworks required
- Responsive design

### Automata Engine (Unchanged)
- Regex tokenization
- Thompson's Construction (Regex → NFA)
- Subset Construction (NFA → DFA)
- DFA simulation for pattern matching

---

## 🎓 Educational Value

This project demonstrates:
1. **Automata Theory** - RE, NFA, DFA in practice
2. **Web Development** - Django REST API + Modern Frontend
3. **Software Architecture** - Clean separation of concerns
4. **Cybersecurity** - Pattern-based malware detection

---

## 📝 License

Educational use only. Not for production malware detection.

---

## 👥 Contributors

- **Sheikh Muhammad Ahmed** (65877) - Backend logic & file handling
- **Muhammad Ibtisam** (65857) - Core automata & full integration

**Course:** Theory of Automata  
**Institution:** KIET (Karachi Institute of Economics and Technology)  
**Instructor:** Miss Misbah Anwar

---

## 🌟 Features Comparison

| Feature | Old (Tkinter) | New (Django + Web) |
|---------|---------------|-------------------|
| Interface | Desktop GUI | Modern Web UI |
| Accessibility | Local only | Network accessible |
| Design | Basic | Glassmorphism, animations |
| API | None | RESTful API |
| Mobile Support | No | Yes (responsive) |
| File Upload | Browse only | Drag & drop + browse |
| Results Display | Table | Interactive cards |
| Extensibility | Limited | API-first architecture |

---

**Built with ❤️ using Automata Theory + Django REST Framework**

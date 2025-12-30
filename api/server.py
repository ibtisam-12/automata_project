# api/server.py

"""
Flask REST API Server for Automata-Based Malware Detector
Provides API endpoints for the web frontend while preserving all automata logic.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import tempfile
from typing import Dict, List

# Import existing automata modules (no changes to logic)
from automata.engine import compile_signatures, scan_file, scan_text_lines
from signatures import SIGNATURES

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'txt', 'py', 'sh', 'js', 'java', 'cpp', 'c', 'html', 'css', 'php', 'rb'}

# Compile signatures on startup
try:
    COMPILED_SIGNATURES = compile_signatures(SIGNATURES)
    print(f"✓ Compiled {len(COMPILED_SIGNATURES)} signatures successfully")
except Exception as e:
    print(f"✗ Error compiling signatures: {e}")
    COMPILED_SIGNATURES = []


def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'signatures_loaded': len(COMPILED_SIGNATURES),
        'version': '1.0.0'
    })


@app.route('/api/signatures', methods=['GET'])
def get_signatures():
    """Get all loaded malware signatures."""
    signature_list = [
        {
            'name': name,
            'regex': regex,
            'description': get_signature_description(name)
        }
        for name, regex in SIGNATURES.items()
    ]
    
    return jsonify({
        'success': True,
        'count': len(signature_list),
        'signatures': signature_list
    })


def get_signature_description(name: str) -> str:
    """Get human-readable description for a signature."""
    descriptions = {
        'eval_call': 'Detects eval() function calls (dynamic code execution)',
        'exec_call': 'Detects exec() function calls (dynamic code execution)',
        'base64_decode': 'Detects base64 decoding (potential obfuscation)',
        'rm_rf': 'Detects destructive file deletion commands',
        'powershell': 'Detects PowerShell execution',
        'http': 'Detects HTTP URLs (potential C&C communication)'
    }
    return descriptions.get(name, 'Custom malware signature')


@app.route('/api/scan/text', methods=['POST'])
def scan_text():
    """Scan text content for malware signatures."""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'success': False,
                'error': 'No text provided'
            }), 400
        
        text = data['text']
        lines = text.split('\n')
        
        # Scan using existing automata logic
        matches = scan_text_lines(COMPILED_SIGNATURES, lines)
        
        # Format matches for frontend
        formatted_matches = [
            {
                'signature_name': m.signature_name,
                'regex': m.regex,
                'line_no': m.line_no,
                'start_idx': m.start_idx,
                'end_idx': m.end_idx,
                'snippet': m.snippet,
                'description': get_signature_description(m.signature_name)
            }
            for m in matches
        ]
        
        return jsonify({
            'success': True,
            'matches_found': len(formatted_matches),
            'matches': formatted_matches,
            'total_lines': len(lines)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/scan/file', methods=['POST'])
def scan_file_upload():
    """Scan uploaded file for malware signatures."""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file provided'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': f'File type not allowed. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'
            }), 400
        
        # Save file temporarily
        filename = secure_filename(file.filename)
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, filename)
        
        file.save(temp_path)
        
        try:
            # Scan using existing automata logic
            lines, matches = scan_file(COMPILED_SIGNATURES, temp_path)
            
            # Format matches for frontend
            formatted_matches = [
                {
                    'signature_name': m.signature_name,
                    'regex': m.regex,
                    'line_no': m.line_no,
                    'start_idx': m.start_idx,
                    'end_idx': m.end_idx,
                    'snippet': m.snippet,
                    'description': get_signature_description(m.signature_name)
                }
                for m in matches
            ]
            
            # Get file preview (first 20 lines)
            preview_lines = lines[:20]
            
            return jsonify({
                'success': True,
                'filename': filename,
                'matches_found': len(formatted_matches),
                'matches': formatted_matches,
                'total_lines': len(lines),
                'preview': preview_lines,
                'risk_level': calculate_risk_level(len(formatted_matches))
            })
        
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


def calculate_risk_level(match_count: int) -> str:
    """Calculate risk level based on number of matches."""
    if match_count == 0:
        return 'safe'
    elif match_count <= 2:
        return 'low'
    elif match_count <= 5:
        return 'medium'
    elif match_count <= 10:
        return 'high'
    else:
        return 'critical'


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get system statistics."""
    return jsonify({
        'success': True,
        'stats': {
            'total_signatures': len(SIGNATURES),
            'compiled_signatures': len(COMPILED_SIGNATURES),
            'supported_file_types': list(ALLOWED_EXTENSIONS),
            'max_file_size_mb': app.config['MAX_CONTENT_LENGTH'] / (1024 * 1024)
        }
    })


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error."""
    return jsonify({
        'success': False,
        'error': 'File too large. Maximum size is 16MB.'
    }), 413


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    print("=" * 60)
    print("Automata-Based Malware Detector - REST API Server")
    print("=" * 60)
    print(f"Loaded {len(SIGNATURES)} malware signatures")
    print(f"Compiled {len(COMPILED_SIGNATURES)} DFAs")
    print("\nAPI Endpoints:")
    print("  GET  /api/health       - Health check")
    print("  GET  /api/signatures   - List all signatures")
    print("  POST /api/scan/text    - Scan text content")
    print("  POST /api/scan/file    - Scan uploaded file")
    print("  GET  /api/stats        - System statistics")
    print("\nStarting server on http://localhost:5000")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)

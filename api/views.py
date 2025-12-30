# api/views.py

"""
Django REST API Views for Automata-Based Malware Detector
Provides API endpoints while preserving all existing automata logic.
"""

from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import os
import tempfile

# Import existing automata modules (no changes to logic)
from automata.engine import compile_signatures, scan_file, scan_text_lines
from signatures import SIGNATURES

# Compile signatures on module load
try:
    COMPILED_SIGNATURES = compile_signatures(SIGNATURES)
    print(f"✓ Compiled {len(COMPILED_SIGNATURES)} signatures successfully")
except Exception as e:
    print(f"✗ Error compiling signatures: {e}")
    COMPILED_SIGNATURES = []


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


def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed."""
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    return ext in settings.ALLOWED_FILE_EXTENSIONS


@api_view(['GET'])
def health_check(request):
    """Health check endpoint."""
    return Response({
        'status': 'healthy',
        'signatures_loaded': len(COMPILED_SIGNATURES),
        'version': '1.0.0'
    })


@api_view(['GET'])
def get_signatures(request):
    """Get all loaded malware signatures."""
    signature_list = [
        {
            'name': name,
            'regex': regex,
            'description': get_signature_description(name)
        }
        for name, regex in SIGNATURES.items()
    ]
    
    return Response({
        'success': True,
        'count': len(signature_list),
        'signatures': signature_list
    })


@api_view(['POST'])
@parser_classes([JSONParser])
def scan_text(request):
    """Scan text content for malware signatures."""
    try:
        text = request.data.get('text')
        
        if not text:
            return Response({
                'success': False,
                'error': 'No text provided'
            }, status=status.HTTP_400_BAD_REQUEST)
        
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
        
        return Response({
            'success': True,
            'matches_found': len(formatted_matches),
            'matches': formatted_matches,
            'total_lines': len(lines),
            'risk_level': calculate_risk_level(len(formatted_matches))
        })
    
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def scan_file_upload(request):
    """Scan uploaded file for malware signatures."""
    try:
        # Check if file is present
        if 'file' not in request.FILES:
            return Response({
                'success': False,
                'error': 'No file provided'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        uploaded_file = request.FILES['file']
        
        if not uploaded_file.name:
            return Response({
                'success': False,
                'error': 'No file selected'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not allowed_file(uploaded_file.name):
            return Response({
                'success': False,
                'error': f'File type not allowed. Allowed types: {", ".join(settings.ALLOWED_FILE_EXTENSIONS)}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Save file temporarily
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, uploaded_file.name)
        
        with open(temp_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        
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
            
            return Response({
                'success': True,
                'filename': uploaded_file.name,
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
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_stats(request):
    """Get system statistics."""
    return Response({
        'success': True,
        'stats': {
            'total_signatures': len(SIGNATURES),
            'compiled_signatures': len(COMPILED_SIGNATURES),
            'supported_file_types': settings.ALLOWED_FILE_EXTENSIONS,
            'max_file_size_mb': settings.FILE_UPLOAD_MAX_MEMORY_SIZE / (1024 * 1024)
        }
    })

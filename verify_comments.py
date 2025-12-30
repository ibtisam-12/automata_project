import os
import sys

# Add project root to path
sys.path.append(os.getcwd())

from automata.engine import compile_signatures, scan_file
from signatures import SIGNATURES

def test_comment_scanning():
    print("Compiling signatures...")
    compiled = compile_signatures(SIGNATURES)
    
    test_file = "test_files/comment_test.py"
    print(f"Scanning {test_file}...")
    
    lines, matches = scan_file(compiled, test_file)
    
    print(f"Matches found: {len(matches)}")
    for m in matches:
        print(f" - Found {m.signature_name} at line {m.line_no}: {m.snippet}")

if __name__ == "__main__":
    test_comment_scanning()

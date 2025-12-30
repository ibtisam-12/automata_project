from automata.engine import compile_signatures
from automata.regex_parser import tokenize, EscapedChar

# Test tokenizer directly
print("Testing tokenizer...")
tokens = tokenize(r"a\(b")
print(f"Tokens for 'a\\(b': {tokens}")
assert len(tokens) == 3
assert tokens[0] == "a"
assert isinstance(tokens[1], EscapedChar)
assert tokens[1] == "("
assert tokens[2] == "b"
print("Tokenizer test passed.")

# Test full compilation of escaped chars
signatures = {
    "escaped_paren": r"eval\(",
    "escaped_dot": r"base64\.decode"
}

try:
    print("Compiling signatures...")
    compiled = compile_signatures(signatures)
    print("Compilation successful.")
    for sig in compiled:
        num_states = len(sig.dfa.transitions)
        print(f"Compiled {sig.name}: regex '{sig.regex}' -> DFA with {num_states} states")
except Exception as e:
    print(f"FAILED: {e}")
    exit(1)

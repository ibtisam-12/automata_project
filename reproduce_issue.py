from automata.engine import compile_signatures, CompiledSignature

signatures = {
    "good": "a.b",
    "bad": "a(b"
}

try:
    print("Compiling signatures...")
    compile_signatures(signatures)
    print("Compilation successful.")
except ValueError as e:
    print(f"Caught expected error: {e}")
except Exception as e:
    print(f"Caught unexpected error: {e}")

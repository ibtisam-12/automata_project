# This file contains malicious signatures ONLY in comments
# The scanner should IGNORE these if the feature is working.

# malicious: eval(bad_input)
# malicious: exec(bad_code)
# malicious: rm -rf /

print("Hello World")

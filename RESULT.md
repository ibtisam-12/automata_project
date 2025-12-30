# Project Results & Capabilities

## 1. System Overview
The Automata-Based Malware Detector successfully implements a scanning engine capable of identifying malicious patterns in code and text files. The system exposes its functionality via a stateless REST API, making it suitable for integration into larger security pipelines.

## 2. Detection Capabilities
The system is currently configured to detect the following classes of malicious patterns:

| Signature Type | Description | Risk Level |
| :--- | :--- | :--- |
| **Dynamic Execution** | Detects usage of `eval()` and `exec()` which are common vectors for code injection. | High |
| **Obfuscation** | Identifies Base64 decoding patterns often used to hide payloads. | Medium |
| **Destructive Commands** | Flags dangerous shell commands like `rm -rf`. | Critical |
| **Scripting Attacks** | Detects PowerShell script execution markers. | High |
| **Network Indicators** | Scans for HTTP/HTTPS URLs which may indicate C&C (Command & Control) communication. | Low/Medium |

*Note: Signatures are defined in `signatures.py` and are extensible.*

## 3. Performance Results
*   **Initialization**: The system performs a one-time compilation of all regex signatures into DFAs upon server startup.
*   **Scan Speed**: Due to the DFA implementation, the scanning complexity is **linear $O(N)$** with respect to the input size, regardless of the complexity of the regular expression (excluding the constant factor of the number of signatures).
*   **Memory Efficiency**: By converting to DFA, the system avoids the backtracking overhead typical of NFA-based or backtracking regex engines.

## 4. API Specification & Output

### 4.1 Endpoints
*   `GET /api/signatures/`: Returns a list of active detection rules.
*   `POST /api/scan/text/`: Scans raw text content.
*   `POST /api/scan/file/`: Scans uploaded files (supports `.py`, `.txt`, `.js`, `.log`, `.sh`).

### 4.2 Sample Output
When a threat is detected, the API returns a structured JSON response:

```json
{
    "success": true,
    "matches_found": 1,
    "matches": [
        {
            "signature_name": "eval_call",
            "regex": "eval\\s*\\(",
            "line_no": 15,
            "start_idx": 4,
            "end_idx": 9,
            "snippet": "eval(",
            "description": "Detects eval() function calls (dynamic code execution)"
        }
    ],
    "risk_level": "medium"
}
```

### 4.3 Risk Assessment
The system automatically calculates a risk score based on the volume of findings:
*   **Safe**: 0 matches
*   **Low**: 1-2 matches
*   **Medium**: 3-5 matches
*   **High**: 6-10 matches
*   **Critical**: >10 matches

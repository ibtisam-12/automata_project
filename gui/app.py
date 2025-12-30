# gui/app.py

from __future__ import annotations

import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from automata.engine import compile_signatures, scan_file
from signatures import SIGNATURES


class MalwareDetectorApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Automata-Based Malware Signature Detector (Regex→NFA→DFA)")
        self.geometry("1000x650")

        self.compiled = None

        self._build_ui()
        self._compile()

    def _build_ui(self) -> None:
        top = ttk.Frame(self, padding=10)
        top.pack(fill="x")

        self.file_var = tk.StringVar(value="")
        ttk.Label(top, text="Target file:").pack(side="left")
        ttk.Entry(top, textvariable=self.file_var, width=80).pack(side="left", padx=8)

        ttk.Button(top, text="Browse", command=self.browse).pack(side="left")
        ttk.Button(top, text="Scan", command=self.scan).pack(side="left", padx=8)

        mid = ttk.Frame(self, padding=10)
        mid.pack(fill="both", expand=True)

        # Results table
        cols = ("signature", "regex", "line", "start", "end", "snippet")
        self.tree = ttk.Treeview(mid, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c.upper())
            self.tree.column(c, width=120 if c != "snippet" else 360, anchor="w")

        vsb = ttk.Scrollbar(mid, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        bottom = ttk.Frame(self, padding=10)
        bottom.pack(fill="x")

        self.status = tk.StringVar(value="Ready.")
        ttk.Label(bottom, textvariable=self.status).pack(side="left")

        # Signatures panel
        sig_frame = ttk.LabelFrame(self, text="Loaded signatures (name → regex)", padding=10)
        sig_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.sig_text = tk.Text(sig_frame, height=6)
        self.sig_text.pack(fill="x")
        self.sig_text.insert("1.0", "\n".join([f"{k}: {v}" for k, v in SIGNATURES.items()]))
        self.sig_text.configure(state="disabled")

    def _compile(self) -> None:
        try:
            self.compiled = compile_signatures(SIGNATURES)
            self.status.set(f"Compiled {len(SIGNATURES)} signatures into DFAs.")
        except Exception as e:
            print(f"Compilation Error: {e}")
            messagebox.showerror("Compile error", str(e))
            self.status.set("Compilation failed. Check signatures.")

    def browse(self) -> None:
        path = filedialog.askopenfilename(title="Select a text/code file")
        if path:
            self.file_var.set(path)

    def scan(self) -> None:
        path = self.file_var.get().strip()
        if not path:
            messagebox.showwarning("No file", "Please select a file to scan.")
            return
        if self.compiled is None:
            messagebox.showerror("Not ready", "Signatures not compiled.")
            return

        # Clear existing
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            _, matches = scan_file(self.compiled, path)
        except Exception as e:
            messagebox.showerror("Scan error", str(e))
            return

        for m in matches:
            self.tree.insert("", "end", values=(m.signature_name, m.regex, m.line_no, m.start_idx, m.end_idx, m.snippet))

        self.status.set(f"Scan complete. Matches found: {len(matches)}")

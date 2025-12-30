# automata/engine.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

from .nfa import regex_to_nfa
from .dfa import nfa_to_dfa, dfa_find_all, Match, DFA


@dataclass
class CompiledSignature:
    name: str
    regex: str
    dfa: DFA


def compile_signatures(sig_map: Dict[str, str]) -> List[CompiledSignature]:
    compiled: List[CompiledSignature] = []
    for name, regex in sig_map.items():
        try:
            nfa = regex_to_nfa(regex)
            dfa = nfa_to_dfa(nfa)
            compiled.append(CompiledSignature(name=name, regex=regex, dfa=dfa))
        except Exception as e:
            raise ValueError(f"Error compiling signature '{name}' (regex: '{regex}'): {e}") from e
    return compiled


def scan_text_lines(compiled: List[CompiledSignature], lines: List[str]) -> List[Match]:
    findings: List[Match] = []
    for idx, line in enumerate(lines, start=1):
        line = line.rstrip("\n")
        for sig in compiled:
            findings.extend(dfa_find_all(sig.dfa, line, sig.name, sig.regex, idx))
    return findings


def scan_file(compiled: List[CompiledSignature], path: str, encoding: str = "utf-8") -> Tuple[List[str], List[Match]]:
    with open(path, "r", encoding=encoding, errors="replace") as f:
        lines = f.readlines()
    matches = scan_text_lines(compiled, lines)
    return lines, matches

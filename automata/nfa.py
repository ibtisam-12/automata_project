# automata/nfa.py

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Set, List, Optional, Tuple
from .regex_parser import to_postfix, is_literal


EPS = "ε"


@dataclass(frozen=True)
class State:
    id: int


@dataclass
class NFA:
    start: State
    accept: State
    transitions: Dict[State, Dict[str, Set[State]]] = field(default_factory=dict)

    def add_transition(self, src: State, sym: str, dst: State) -> None:
        self.transitions.setdefault(src, {}).setdefault(sym, set()).add(dst)

    def get_transitions(self, src: State, sym: str) -> Set[State]:
        return self.transitions.get(src, {}).get(sym, set())

    def alphabet(self) -> Set[str]:
        syms: Set[str] = set()
        for _, mp in self.transitions.items():
            for sym in mp.keys():
                if sym != EPS:
                    syms.add(sym)
        return syms


class _IdGen:
    def __init__(self) -> None:
        self._i = 0

    def new(self) -> State:
        s = State(self._i)
        self._i += 1
        return s


@dataclass
class _Frag:
    start: State
    accept: State


def regex_to_nfa(regex: str) -> NFA:
    """
    Convert regex to NFA using Thompson's construction.
    Operators in postfix: literal, '.', '|', '*'
    """
    postfix = to_postfix(regex)
    gen = _IdGen()
    transitions: Dict[State, Dict[str, Set[State]]] = {}

    def add(src: State, sym: str, dst: State) -> None:
        transitions.setdefault(src, {}).setdefault(sym, set()).add(dst)

    stack: List[_Frag] = []

    for tok in postfix:
        if is_literal(tok) or tok not in {".", "|", "*"}:
            s = gen.new()
            a = gen.new()
            add(s, tok, a)
            stack.append(_Frag(s, a))
        elif tok == ".":
            # concat: frag1 then frag2
            if len(stack) < 2:
                raise ValueError("Invalid regex (concat).")
            f2 = stack.pop()
            f1 = stack.pop()
            add(f1.accept, EPS, f2.start)
            stack.append(_Frag(f1.start, f2.accept))
        elif tok == "|":
            if len(stack) < 2:
                raise ValueError("Invalid regex (union).")
            f2 = stack.pop()
            f1 = stack.pop()
            s = gen.new()
            a = gen.new()
            add(s, EPS, f1.start)
            add(s, EPS, f2.start)
            add(f1.accept, EPS, a)
            add(f2.accept, EPS, a)
            stack.append(_Frag(s, a))
        elif tok == "*":
            if not stack:
                raise ValueError("Invalid regex (kleene star).")
            f = stack.pop()
            s = gen.new()
            a = gen.new()
            add(s, EPS, f.start)
            add(s, EPS, a)
            add(f.accept, EPS, f.start)
            add(f.accept, EPS, a)
            stack.append(_Frag(s, a))
        else:
            raise ValueError(f"Unknown token {tok}")

    if len(stack) != 1:
        raise ValueError("Invalid regex; could not reduce to single NFA.")
    frag = stack.pop()
    return NFA(start=frag.start, accept=frag.accept, transitions=transitions)

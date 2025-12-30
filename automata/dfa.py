# automata/dfa.py

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Set, FrozenSet, Tuple, List, Optional

from .nfa import NFA, EPS, State


def epsilon_closure(nfa: NFA, states: Set[State]) -> Set[State]:
    stack = list(states)
    closure = set(states)
    while stack:
        s = stack.pop()
        for nxt in nfa.get_transitions(s, EPS):
            if nxt not in closure:
                closure.add(nxt)
                stack.append(nxt)
    return closure


def move(nfa: NFA, states: Set[State], sym: str) -> Set[State]:
    out: Set[State] = set()
    for s in states:
        out |= nfa.get_transitions(s, sym)
    return out


@dataclass(frozen=True)
class DFAState:
    nfa_subset: FrozenSet[State]


@dataclass
class DFA:
    start: DFAState
    accepts: Set[DFAState]
    transitions: Dict[DFAState, Dict[str, DFAState]] = field(default_factory=dict)
    alphabet: Set[str] = field(default_factory=set)

    def step(self, state: DFAState, sym: str) -> Optional[DFAState]:
        return self.transitions.get(state, {}).get(sym)

    def is_accept(self, state: DFAState) -> bool:
        return state in self.accepts


def nfa_to_dfa(nfa: NFA) -> DFA:
    alphabet = nfa.alphabet()

    start_set = epsilon_closure(nfa, {nfa.start})
    start = DFAState(frozenset(start_set))

    unmarked: List[DFAState] = [start]
    dfa_states: Set[DFAState] = {start}
    transitions: Dict[DFAState, Dict[str, DFAState]] = {}

    accepts: Set[DFAState] = set()
    if nfa.accept in start_set:
        accepts.add(start)

    while unmarked:
        d = unmarked.pop()
        transitions.setdefault(d, {})
        dset = set(d.nfa_subset)

        for sym in alphabet:
            u = epsilon_closure(nfa, move(nfa, dset, sym))
            if not u:
                continue
            ustate = DFAState(frozenset(u))
            if ustate not in dfa_states:
                dfa_states.add(ustate)
                unmarked.append(ustate)
                if nfa.accept in u:
                    accepts.add(ustate)
            transitions[d][sym] = ustate

    return DFA(start=start, accepts=accepts, transitions=transitions, alphabet=alphabet)


@dataclass
class Match:
    signature_name: str
    regex: str
    line_no: int
    start_idx: int
    end_idx: int
    snippet: str


def dfa_find_all(dfa: DFA, text: str, signature_name: str, regex: str, line_no: int) -> List[Match]:
    """
    Finds all matches in a single line using DFA simulation.
    We attempt matches starting at each position.
    """
    matches: List[Match] = []
    n = len(text)

    for i in range(n):
        state = dfa.start
        last_accept_j: Optional[int] = None

        for j in range(i, n):
            sym = text[j]
            nxt = dfa.step(state, sym)
            if nxt is None:
                break
            state = nxt
            if dfa.is_accept(state):
                last_accept_j = j

        if last_accept_j is not None:
            start_idx = i
            end_idx = last_accept_j + 1
            snippet = text[start_idx:end_idx]
            matches.append(
                Match(
                    signature_name=signature_name,
                    regex=regex,
                    line_no=line_no,
                    start_idx=start_idx,
                    end_idx=end_idx,
                    snippet=snippet,
                )
            )

    # Optional: de-duplicate overlaps (keep maximal per start)
    # Keep the longest match for each start index:
    best_by_start: Dict[int, Match] = {}
    for m in matches:
        cur = best_by_start.get(m.start_idx)
        if cur is None or (m.end_idx - m.start_idx) > (cur.end_idx - cur.start_idx):
            best_by_start[m.start_idx] = m

    # Return in order
    return [best_by_start[k] for k in sorted(best_by_start.keys())]

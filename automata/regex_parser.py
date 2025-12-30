# automata/regex_parser.py

from __future__ import annotations

from dataclasses import dataclass
from typing import List


OPS = {"|", ".", "*", "(", ")"}


class EscapedChar(str):
    """Wrapper to mark a character as escaped (treated as literal)."""
    pass


def is_literal(ch: str) -> bool:
    if isinstance(ch, EscapedChar):
        return True
    return ch not in OPS


def tokenize(regex: str) -> List[str]:
    """
    Converts a regex string into tokens.
    Supported:
      - literals: any non-operator char
      - operators: |  .  *  (  )
      - escapes: \\x treated as literal x
    """
    if not regex:
        raise ValueError("Empty regex is not allowed.")
    
    tokens = []
    i = 0
    n = len(regex)
    while i < n:
        ch = regex[i]
        if ch == "\\":
            if i + 1 < n:
                tokens.append(EscapedChar(regex[i + 1]))
                i += 2
            else:
                raise ValueError("Trailing backslash in regex.")
        else:
            tokens.append(ch)
            i += 1
    return tokens


def add_explicit_concat(tokens: List[str]) -> List[str]:
    """
    Insert '.' between tokens where concatenation is implied.
    Example: ab -> a.b, a(b|c) -> a.(b|c), (a|b)c -> (a|b).c, a* b -> a*.b
    """
    out: List[str] = []
    for i, t in enumerate(tokens):
        out.append(t)
        if i == len(tokens) - 1:
            break

        t1 = t
        t2 = tokens[i + 1]

        left_can_end = (is_literal(t1) or t1 == ")" or t1 == "*")
        right_can_start = (is_literal(t2) or t2 == "(")

        if left_can_end and right_can_start:
            out.append(".")
    return out


def precedence(op: str) -> int:
    # Highest: * (unary postfix)
    # Next: . (concat)
    # Lowest: | (union)
    if op == "*":
        return 3
    if op == ".":
        return 2
    if op == "|":
        return 1
    return 0


def to_postfix(regex: str) -> List[str]:
    """
    Shunting-yard algorithm to convert regex to postfix for Thompson's construction.
    """
    tokens = add_explicit_concat(tokenize(regex))
    output: List[str] = []
    stack: List[str] = []

    for t in tokens:
        if is_literal(t):
            output.append(t)
        elif t == "(":
            stack.append(t)
        elif t == ")":
            while stack and stack[-1] != "(":
                output.append(stack.pop())
            if not stack:
                raise ValueError("Mismatched parentheses in regex.")
            stack.pop()  # pop "("
        else:
            # operator: | or . or *
            if t == "*":
                # unary postfix: directly push with high precedence
                # but still pop any higher/equal precedence ops except '('
                while stack and stack[-1] != "(" and precedence(stack[-1]) >= precedence(t):
                    output.append(stack.pop())
                stack.append(t)
            else:
                while stack and stack[-1] != "(" and precedence(stack[-1]) >= precedence(t):
                    output.append(stack.pop())
                stack.append(t)

    while stack:
        if stack[-1] in {"(", ")"}:
            raise ValueError("Mismatched parentheses in regex.")
        output.append(stack.pop())

    return output

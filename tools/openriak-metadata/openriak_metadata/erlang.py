"""Erlang terms used by Cuttlefish, parsed statically and never evaluated."""
from __future__ import annotations

import re

from . import _erlang_impl as _implementation
from ._erlang_impl import *
from ._erlang_impl import TermParser as _TermParser

_original_tokenize = _implementation.tokenize
_original_raw_erlang = _implementation.raw_erlang
_BLOCK_OPENERS = {"begin", "case", "if", "receive", "try", "maybe"}


def tokenize(text: str):
    text = re.sub(r"\bfun\s+([a-zA-Z_][\w@]*(?::[a-zA-Z_][\w@]*)?/\d+)", r"'fun \1'", text)
    return _original_tokenize(text)


class TermParser(_TermParser):
    def __init__(self, text: str) -> None:
        raw_tokens = [token for token in tokenize(text) if token.kind != "comment"]
        self.tokens = []
        for token in raw_tokens:
            if self.tokens and token.kind == "string" and self.tokens[-1].kind == "string":
                previous = self.tokens[-1]
                previous.value = previous.value[:-1] + token.value[1:]
            else:
                self.tokens.append(token)
        self.index = 0

    def parse_term(self):
        if self._peek("("):
            return self._opaque_parenthesized()
        if (self.index < len(self.tokens) and self.tokens[self.index].kind == "atom"
                and self.tokens[self.index].value in _BLOCK_OPENERS):
            return self._opaque_block()
        value = super().parse_term()
        if self._peek("("):
            expression = self._opaque_parenthesized()["$erlang_expression"]
            return {"$erlang_expression": raw_erlang(value) + expression}
        return value

    def _opaque_parenthesized(self):
        pieces, depth = [], 0
        while self.index < len(self.tokens):
            token = self.tokens[self.index]; self.index += 1
            pieces.append(token.value)
            if token.kind == "(": depth += 1
            elif token.kind == ")":
                depth -= 1
                if depth == 0: break
        return {"$erlang_expression": " ".join(pieces)}

    def _opaque_block(self):
        pieces, depth = [], 0
        while self.index < len(self.tokens):
            token = self.tokens[self.index]; self.index += 1
            pieces.append(token.value)
            if token.kind == "atom" and token.value in _BLOCK_OPENERS: depth += 1
            elif token.kind == "atom" and token.value == "end":
                depth -= 1
                if depth == 0: break
        return {"$erlang_expression": " ".join(pieces)}


def raw_erlang(value) -> str:
    if isinstance(value, dict) and "$erlang_expression" in value:
        return value["$erlang_expression"]
    return _original_raw_erlang(value)


_implementation.tokenize = tokenize

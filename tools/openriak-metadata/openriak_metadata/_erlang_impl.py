from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class Token:
    kind: str
    value: str
    line: int


class ErlangParseError(ValueError):
    pass


def tokenize(text: str) -> list[Token]:
    tokens: list[Token] = []
    i, line = 0, 1
    punctuation = set("{}[](),.=|;")
    while i < len(text):
        char = text[i]
        if char.isspace():
            line += char == "\n"
            i += 1
            continue
        if char == "%":
            end = text.find("\n", i)
            if end < 0:
                end = len(text)
            tokens.append(Token("comment", text[i:end], line))
            i = end
            continue
        if text.startswith("{{", i):
            end = text.find("}}", i + 2)
            if end < 0:
                raise ErlangParseError(f"unterminated template at line {line}")
            tokens.append(Token("template", text[i:end + 2], line))
            i = end + 2
            continue
        if char in ('"', "'"):
            quote_char, start, start_line = char, i, line
            i += 1
            escaped = False
            while i < len(text):
                if text[i] == "\n":
                    line += 1
                if text[i] == quote_char and not escaped:
                    i += 1
                    break
                escaped = text[i] == "\\" and not escaped
                if text[i] != "\\":
                    escaped = False
                i += 1
            tokens.append(Token("string" if quote_char == '"' else "atom", text[start:i], start_line))
            continue
        if char in punctuation:
            tokens.append(Token(char, char, line)); i += 1; continue
        number = re.match(r"-?\d+(?:\.\d+)?", text[i:])
        if number:
            value = number.group(0); tokens.append(Token("number", value, line)); i += len(value); continue
        word = re.match(r"[A-Za-z_$][A-Za-z0-9_@$:-]*", text[i:])
        if word:
            value = word.group(0)
            if value == "fun":
                raw, consumed, added_lines = _opaque_fun(text[i:])
                tokens.append(Token("fun", raw, line)); i += consumed; line += added_lines; continue
            tokens.append(Token("atom", value, line)); i += len(value); continue
        # Keep unfamiliar Erlang operators/expressions parseable as atoms.
        end = i + 1
        while end < len(text) and not text[end].isspace() and text[end] not in punctuation:
            end += 1
        tokens.append(Token("atom", text[i:end], line)); i = end
    return tokens


def _opaque_fun(text: str) -> tuple[str, int, int]:
    depth, i = 0, 0
    pattern = re.compile(r"\b(fun|case|if|receive|try|begin|maybe|end)\b|\"(?:\\.|[^\"])*\"|'(?:\\.|[^'])*'|%[^\n]*")
    for match in pattern.finditer(text):
        token = match.group(0)
        if token.startswith(("\"", "'", "%")):
            continue
        if token in ("fun", "case", "if", "receive", "try", "begin", "maybe"):
            depth += 1
        elif token == "end":
            depth -= 1
            if depth == 0:
                i = match.end()
                return text[:i].strip(), i, text[:i].count("\n")
    raise ErlangParseError("unterminated fun expression")


class TermParser:
    def __init__(self, text: str) -> None:
        self.tokens = [t for t in tokenize(text) if t.kind != "comment"]
        self.index = 0

    def parse_all(self) -> list[tuple[object, int]]:
        result = []
        while self.index < len(self.tokens):
            if self._peek("."):
                self.index += 1; continue
            line = self.tokens[self.index].line
            result.append((self.parse_term(), line))
            if self._peek("."):
                self.index += 1
        return result

    def parse_term(self):
        if self.index >= len(self.tokens):
            raise ErlangParseError("unexpected end of input")
        token = self.tokens[self.index]; self.index += 1
        if token.kind == "{":
            return {"$erlang_tuple": self._sequence("}")}
        if token.kind == "[":
            return self._sequence("]")
        if token.kind == "string":
            return bytes(token.value[1:-1], "utf-8").decode("unicode_escape")
        if token.kind == "number":
            return float(token.value) if "." in token.value else int(token.value)
        if token.kind == "fun":
            return {"$erlang_fun": token.value}
        if token.kind == "template":
            return {"$template": token.value}
        if token.kind == "atom":
            value = token.value[1:-1] if token.value.startswith("'") else token.value
            if value == "true": return True
            if value == "false": return False
            if value in ("undefined", "null"): return {"$erlang_atom": value}
            return value
        raise ErlangParseError(f"unexpected token {token.value!r} at line {token.line}")

    def _sequence(self, closing: str) -> list:
        values = []
        if self._peek(closing):
            self.index += 1; return values
        while True:
            values.append(self.parse_term())
            if self._peek(closing):
                self.index += 1; return values
            if not self._peek(","):
                token = self.tokens[self.index] if self.index < len(self.tokens) else None
                raise ErlangParseError(f"expected comma or {closing}, got {token}")
            self.index += 1

    def _peek(self, kind: str) -> bool:
        return self.index < len(self.tokens) and self.tokens[self.index].kind == kind


def tuple_values(value) -> list | None:
    return value.get("$erlang_tuple") if isinstance(value, dict) else None


def raw_erlang(value) -> str:
    if isinstance(value, dict) and "$erlang_fun" in value:
        return value["$erlang_fun"]
    if isinstance(value, dict) and "$template" in value:
        return value["$template"]
    if isinstance(value, dict) and "$erlang_tuple" in value:
        return "{" + ", ".join(raw_erlang(v) for v in value["$erlang_tuple"]) + "}"
    if isinstance(value, list):
        return "[" + ", ".join(raw_erlang(v) for v in value) + "]"
    if isinstance(value, str):
        return value
    if value is True: return "true"
    if value is False: return "false"
    return str(value)


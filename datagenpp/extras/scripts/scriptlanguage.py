"""
ScriptLanguage: DSL that compiles a text block into python-datagen API calls.

Supported syntax
----------------
// single-line comment

%require(module.ClassName)              import class into scope

using namespace NAME {
    fn NAME(param, ...) {               function declaration
        say "message $(macro)";
        effect give @target effect_id [secs [amp [hide]]];
        if (CONDITION) { body } [else { body }]
        wait (Nt) then { body }
        $obj:holder OP value;           score operation (= += -= *= /= %=)
        &ns:storage.key = value;        storage assign
        raw command;                    anything else
    } [inside #TAG_ID;]                 auto-add to tag after declaration

    tag NAME { ns:id, ns:id, ... }      ItemTag

    #NS:PATH << fn_name;                add function to tag

    recipe NAME { ...json... }          Recipe

    Module.method(arg, ...);            call imported module method

    $OBJ_NAME = new("criterion", "Display Name");    create objective
}
"""
from __future__ import annotations

import importlib
import json as _json
import re
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any

from datagen.datapack.namespace import Namespace
from datagen.function.commands._data.datastorage import DataStorage
from datagen.function.commands.customcommand import CustomCommand
from datagen.function.commands.execute import Execute
from datagen.function.commands.say import Say
from datagen.function.commands.schedule import Schedule
from datagen.function.commands.scoreboard import Scoreboard
from datagen.function.function import Function
from datagen.recipes.recipe import Recipe
from datagen.tag.functiontag import FunctionTag
from datagen.tag.itemtag import ItemTag
from datagen.tag.tag import Tag
from datagen.types.util.counter import Counter
from datagen.types.util.min import Range
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.minecraft.text import Text
from datagen.utils.repr.item import Item
from datagen.utils.scoreboard.criterion import ObjectiveCriterion
from datagen.utils.scoreboard.objective import ScoreboardObjective


# ===========================================================================
# Tokenizer
# ===========================================================================

class TT(Enum):
    DIRECTIVE  = auto()   # %require(...)
    SCORE      = auto()   # $obj:holder  — value excludes leading $
    STORAGE    = auto()   # &ns:path     — value excludes leading &
    TAG_REF    = auto()   # #ns:path     — value excludes leading #
    TARGET_SEL = auto()   # @s  @a  @e[...]  (full, brackets included)
    STRING     = auto()   # "..."
    NUMBER     = auto()   # 42  3.14
    TICK_DUR   = auto()   # 20t  5s
    IDENT      = auto()
    LBRACE     = auto()
    RBRACE     = auto()
    LPAREN     = auto()
    RPAREN     = auto()
    LBRACKET   = auto()
    RBRACKET   = auto()
    COMMA      = auto()
    SEMICOLON  = auto()
    COLON      = auto()
    DOT        = auto()
    EQ         = auto()   # =
    NEQ        = auto()   # !=
    LT         = auto()   # <
    GT         = auto()   # >
    LTEQ       = auto()   # <=
    GTEQ       = auto()   # >=
    LSHIFT     = auto()   # <<
    PLUS       = auto()
    MINUS      = auto()
    STAR       = auto()
    SLASH      = auto()
    NULLCOAL   = auto()   # ??
    PLUS_EQ    = auto()   # +=
    MINUS_EQ   = auto()   # -=
    STAR_EQ    = auto()   # *=
    SLASH_EQ   = auto()   # /=
    PERCENT_EQ = auto()   # %=
    DOTDOT     = auto()   # ..
    BLOCK_POS  = auto()   # &(x y z)
    EOF        = auto()


@dataclass
class Token:
    type: TT
    value: str
    line: int = 0


_SINGLE: dict[str, TT] = {
    '{': TT.LBRACE,  '}': TT.RBRACE,
    '(': TT.LPAREN,  ')': TT.RPAREN,
    '[': TT.LBRACKET,']': TT.RBRACKET,
    ',': TT.COMMA,   ';': TT.SEMICOLON,
    '.': TT.DOT,
    '+': TT.PLUS,    '-': TT.MINUS,
    '*': TT.STAR,
}

_TWO: dict[str, TT] = {
    '<=': TT.LTEQ, '>=': TT.GTEQ, '!=': TT.NEQ,
    '<<': TT.LSHIFT, '??': TT.NULLCOAL,
    '+=': TT.PLUS_EQ, '-=': TT.MINUS_EQ,
    '*=': TT.STAR_EQ, '/=': TT.SLASH_EQ, '%=': TT.PERCENT_EQ,
    '..': TT.DOTDOT,
}


class Tokenizer:
    def __init__(self, src: str) -> None:
        self._src = src
        self._i = 0
        self._line = 1

    def _c(self, off: int = 0) -> str:
        p = self._i + off
        return self._src[p] if p < len(self._src) else ''

    def _two(self) -> str:
        return self._src[self._i: self._i + 2]

    def _skip_ws(self) -> None:
        while self._i < len(self._src) and self._src[self._i] in ' \t\r\n':
            if self._src[self._i] == '\n':
                self._line += 1
            self._i += 1

    def _tok(self, tt: TT, v: str) -> Token:
        return Token(tt, v, self._line)

    # ---- public ----

    def tokenize(self) -> list[Token]:
        tokens: list[Token] = []
        while self._i < len(self._src):
            self._skip_ws()
            if self._i >= len(self._src):
                break
            ch = self._c()

            # comment
            if ch == '/' and self._c(1) == '/':
                while self._i < len(self._src) and self._c() != '\n':
                    self._i += 1
                continue

            if ch == '"':
                tokens.append(self._string()); continue
            if ch == '%':
                tokens.append(self._directive()); continue
            if ch == '$':
                self._i += 1
                tokens.append(self._tok(TT.SCORE, self._namespaced_id())); continue
            if ch == '&':
                if self._c(1) == '(':
                    tokens.append(self._block_pos()); continue
                self._i += 1
                tokens.append(self._tok(TT.STORAGE, self._namespaced_id())); continue
            if ch == '#':
                self._i += 1
                tokens.append(self._tok(TT.TAG_REF, self._namespaced_id())); continue
            if ch == '@':
                tokens.append(self._target_sel()); continue
            if ch.isdigit():
                tokens.append(self._number()); continue
            if ch.isalpha() or ch == '_':
                tokens.append(self._ident()); continue

            # two-char operators (check before single-char)
            two = self._two()
            if two in _TWO:
                tokens.append(self._tok(_TWO[two], two))
                self._i += 2; continue

            # single-char operators
            if ch == '=':
                tokens.append(self._tok(TT.EQ, '=')); self._i += 1; continue
            if ch == '<':
                tokens.append(self._tok(TT.LT, '<')); self._i += 1; continue
            if ch == '>':
                tokens.append(self._tok(TT.GT, '>')); self._i += 1; continue
            if ch == ':':
                tokens.append(self._tok(TT.COLON, ':')); self._i += 1; continue
            if ch == '/':
                tokens.append(self._tok(TT.SLASH, '/')); self._i += 1; continue
            if ch in _SINGLE:
                tokens.append(self._tok(_SINGLE[ch], ch)); self._i += 1; continue

            self._i += 1  # skip unknown

        tokens.append(Token(TT.EOF, '', self._line))
        return tokens

    # ---- helpers ----

    def _string(self) -> Token:
        line = self._line
        self._i += 1
        buf: list[str] = []
        while self._i < len(self._src) and self._c() != '"':
            if self._c() == '\\' and self._c(1) == '"':
                buf.append('"'); self._i += 2; continue
            if self._c() == '\n':
                self._line += 1
            buf.append(self._c()); self._i += 1
        self._i += 1
        return Token(TT.STRING, ''.join(buf), line)

    def _directive(self) -> Token:
        line = self._line
        self._i += 1   # skip %
        start = self._i
        while self._i < len(self._src) and self._c() not in '\n;':
            self._i += 1
        return Token(TT.DIRECTIVE, self._src[start:self._i].strip(), line)

    def _namespaced_id(self) -> str:
        """Read chars valid in $score, &storage, #tag tokens (includes : and .)."""
        start = self._i
        while self._i < len(self._src) and (self._c().isalnum() or self._c() in '_:./-'):
            self._i += 1
        return self._src[start:self._i]

    def _target_sel(self) -> Token:
        line = self._line
        start = self._i
        self._i += 1   # @
        if self._i < len(self._src) and self._c().isalpha():
            self._i += 1
        if self._i < len(self._src) and self._c() == '[':
            depth = 0
            while self._i < len(self._src):
                c = self._c()
                if c == '[':
                    depth += 1
                elif c == ']':
                    depth -= 1
                    self._i += 1
                    if depth == 0:
                        break
                    continue
                elif c == '\n':
                    self._line += 1
                self._i += 1
        return Token(TT.TARGET_SEL, self._src[start:self._i], line)

    def _number(self) -> Token:
        line = self._line
        start = self._i
        while self._i < len(self._src) and (self._c().isdigit() or self._c() == '.'):
            self._i += 1
        if self._i < len(self._src) and self._c() in 'tsd':
            self._i += 1
            return Token(TT.TICK_DUR, self._src[start:self._i], line)
        return Token(TT.NUMBER, self._src[start:self._i], line)

    def _ident(self) -> Token:
        line = self._line
        start = self._i
        while self._i < len(self._src) and (self._c().isalnum() or self._c() == '_'):
            self._i += 1
        return Token(TT.IDENT, self._src[start:self._i], line)

    def _block_pos(self) -> Token:
        line = self._line
        self._i += 1  # skip &
        self._i += 1  # skip (
        start = self._i
        depth = 1
        while self._i < len(self._src) and depth > 0:
            c = self._c()
            if c == '(':
                depth += 1
            elif c == ')':
                depth -= 1
                if depth == 0:
                    break
            elif c == '\n':
                self._line += 1
            self._i += 1
        pos = self._src[start:self._i].strip()
        self._i += 1  # skip closing )
        return Token(TT.BLOCK_POS, pos, line)


# ===========================================================================
# AST Nodes
# ===========================================================================

@dataclass
class Node: pass

@dataclass
class Program(Node):
    body: list[Node]

@dataclass
class Directive(Node):
    text: str

@dataclass
class NamespaceDecl(Node):
    name: str
    body: list[Node]

@dataclass
class FnDecl(Node):
    name: str
    params: list[str]
    body: list[Node]
    inside_tag: str | None   # raw tag ref value (without #)

@dataclass
class TagDecl(Node):
    name: str
    values: list[str]

@dataclass
class TagAddition(Node):
    tag_ref: str   # e.g. "minecraft:load"
    fn_name: str

@dataclass
class RecipeDecl(Node):
    name: str
    data: dict

@dataclass
class ModuleCall(Node):
    module: str
    method: str
    args: list[Any]

@dataclass
class ScoreNewDecl(Node):
    obj_name: str
    criterion: str
    display: str

# --- statements inside functions ---

@dataclass
class SayStmt(Node):
    message: str

@dataclass
class EffectStmt(Node):
    sub: str             # "give" | "clear"
    target: str
    effect_id: str
    seconds: int | None
    amplifier: int | None
    hide: bool | None

@dataclass
class ScoreMatchesCond(Node):
    score: str
    range_str: str

@dataclass
class ScoreCompareCond(Node):
    left: str
    op: str
    right: str

@dataclass
class AndCond(Node):
    left: Any
    right: Any

@dataclass
class OrCond(Node):
    left: Any
    right: Any

@dataclass
class RawCond(Node):
    tokens: list[Token]

@dataclass
class IfStmt(Node):
    condition: Any
    body: list[Node]
    else_body: list[Node]

@dataclass
class WaitStmt(Node):
    ticks: int
    unit: str
    body: list[Node]

@dataclass
class ScoreAssignStmt(Node):
    target: str   # "obj:holder"
    op: str       # "=" | "+=" | ...
    rhs: Any      # int | ("score","obj:h") | ("entity","@s","Path",fallback) | ("arith",l,op,r)

@dataclass
class StorageAssignStmt(Node):
    target: str   # "ns:storagename.key.path"
    rhs: Any      # dict | int | str | bool | ("score","obj:h") | ("entity","@s","Path")

@dataclass
class RawCmd(Node):
    text: str


# ===========================================================================
# Parser
# ===========================================================================

class ParseError(Exception):
    pass


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self._toks = tokens
        self._i = 0

    # ---- primitives ----

    def _peek(self, off: int = 0) -> Token:
        p = self._i + off
        return self._toks[p] if p < len(self._toks) else Token(TT.EOF, '', 0)

    def _adv(self) -> Token:
        t = self._toks[self._i]; self._i += 1; return t

    def _eat(self, tt: TT) -> Token:
        t = self._adv()
        if t.type != tt:
            raise ParseError(f"Line {t.line}: expected {tt.name}, got {t.type.name} ({t.value!r})")
        return t

    def _match(self, *types: TT) -> bool:
        return self._peek().type in types

    def _eat_if(self, tt: TT) -> Token | None:
        if self._match(tt):
            return self._adv()
        return None

    # ---- top level ----

    def parse(self) -> Program:
        body: list[Node] = []
        while not self._match(TT.EOF):
            n = self._top()
            if n:
                body.append(n)
        return Program(body)

    def _top(self) -> Node | None:
        t = self._peek()
        if t.type == TT.DIRECTIVE:
            return Directive(self._adv().value)
        if t.type == TT.IDENT and t.value == 'using':
            return self._namespace()
        if t.type == TT.SCORE:
            return self._score_stmt()
        if t.type == TT.STORAGE:
            return self._storage_stmt()
        self._adv()
        return None

    def _namespace(self) -> NamespaceDecl:
        self._eat(TT.IDENT)   # using
        self._eat(TT.IDENT)   # namespace
        name = self._eat(TT.IDENT).value
        self._eat(TT.LBRACE)
        body: list[Node] = []
        while not self._match(TT.RBRACE, TT.EOF):
            n = self._ns_stmt()
            if n:
                body.append(n)
        self._eat(TT.RBRACE)
        return NamespaceDecl(name, body)

    def _ns_stmt(self) -> Node | None:
        t = self._peek()
        if t.type == TT.IDENT and t.value == 'fn':
            return self._fn_decl()
        if t.type == TT.IDENT and t.value == 'tag':
            return self._tag_decl()
        if t.type == TT.IDENT and t.value == 'recipe':
            return self._recipe_decl()
        if t.type == TT.TAG_REF:
            return self._tag_addition()
        if t.type == TT.SCORE:
            return self._score_stmt()
        if t.type == TT.STORAGE:
            return self._storage_stmt()
        if t.type == TT.IDENT and self._peek(1).type == TT.DOT:
            return self._module_call()
        self._adv()
        return None

    # ---- function ----

    def _fn_decl(self) -> FnDecl:
        self._eat(TT.IDENT)   # fn
        name = self._eat(TT.IDENT).value
        self._eat(TT.LPAREN)
        params: list[str] = []
        while not self._match(TT.RPAREN, TT.EOF):
            if self._match(TT.IDENT):
                params.append(self._adv().value)
            self._eat_if(TT.COMMA)
        self._eat(TT.RPAREN)
        self._eat(TT.LBRACE)
        body = self._fn_body()
        self._eat(TT.RBRACE)
        inside: str | None = None
        if self._peek().type == TT.IDENT and self._peek().value == 'inside':
            self._adv()
            inside = self._eat(TT.TAG_REF).value
            self._eat_if(TT.SEMICOLON)
        return FnDecl(name, params, body, inside)

    def _fn_body(self) -> list[Node]:
        stmts: list[Node] = []
        while not self._match(TT.RBRACE, TT.EOF):
            s = self._fn_stmt()
            if s:
                stmts.append(s)
        return stmts

    def _fn_stmt(self) -> Node | None:
        t = self._peek()
        if t.type == TT.IDENT and t.value == 'say':
            self._adv()
            msg = self._eat(TT.STRING).value
            self._eat_if(TT.SEMICOLON)
            return SayStmt(msg)
        if t.type == TT.IDENT and t.value == 'effect':
            return self._effect_stmt()
        if t.type == TT.IDENT and t.value == 'if':
            return self._if_stmt()
        if t.type == TT.IDENT and t.value == 'wait':
            return self._wait_stmt()
        if t.type == TT.SCORE:
            return self._score_stmt()
        if t.type == TT.STORAGE:
            return self._storage_stmt()
        return self._raw_cmd()

    def _effect_stmt(self) -> EffectStmt:
        self._adv()  # effect
        sub = self._eat(TT.IDENT).value
        target = self._eat(TT.TARGET_SEL).value
        eff_id = self._eat(TT.IDENT).value
        secs = amp = hide = None
        if self._match(TT.NUMBER):
            secs = int(float(self._adv().value))
        if self._match(TT.NUMBER):
            amp = int(float(self._adv().value))
        if self._match(TT.IDENT) and self._peek().value in ('true', 'false'):
            hide = self._adv().value == 'true'
        self._eat_if(TT.SEMICOLON)
        return EffectStmt(sub, target, eff_id, secs, amp, hide)

    def _if_stmt(self) -> IfStmt:
        self._adv()  # if
        self._eat(TT.LPAREN)
        cond = self._parse_cond_or()
        self._eat(TT.RPAREN)
        self._eat(TT.LBRACE)
        body = self._fn_body()
        self._eat(TT.RBRACE)
        else_body: list[Node] = []
        if self._peek().type == TT.IDENT and self._peek().value == 'else':
            self._adv()
            self._eat(TT.LBRACE)
            else_body = self._fn_body()
            self._eat(TT.RBRACE)
        return IfStmt(cond, body, else_body)

    def _parse_cond_or(self) -> Any:
        left = self._parse_cond_and()
        while self._peek().type == TT.IDENT and self._peek().value == 'or':
            self._adv()
            right = self._parse_cond_and()
            left = OrCond(left, right)
        return left

    def _parse_cond_and(self) -> Any:
        left = self._parse_cond_term()
        while self._peek().type == TT.IDENT and self._peek().value == 'and':
            self._adv()
            right = self._parse_cond_term()
            left = AndCond(left, right)
        return left

    def _parse_cond_term(self) -> Any:
        t = self._peek()
        if t.type == TT.LPAREN:
            self._adv()
            cond = self._parse_cond_or()
            self._eat(TT.RPAREN)
            return cond
        if t.type == TT.SCORE:
            score_val = self._adv().value
            if self._peek().type == TT.IDENT and self._peek().value == 'matches':
                self._adv()
                return ScoreMatchesCond(score_val, self._parse_range())
            _CMP = {TT.EQ: '=', TT.LT: '<', TT.GT: '>', TT.LTEQ: '<=', TT.GTEQ: '>='}
            if self._peek().type in _CMP:
                op = _CMP[self._adv().type]
                if self._peek().type == TT.SCORE:
                    return ScoreCompareCond(score_val, op, self._adv().value)
            return self._finish_raw([Token(TT.SCORE, score_val)])
        return self._finish_raw([])

    def _parse_range(self) -> str:
        if self._peek().type == TT.DOTDOT:
            self._adv()
            if self._peek().type == TT.NUMBER:
                return f"..{self._adv().value}"
            return ".."
        if self._peek().type == TT.NUMBER:
            n1 = self._adv().value
            if self._peek().type == TT.DOTDOT:
                self._adv()
                if self._peek().type == TT.NUMBER:
                    return f"{n1}..{self._adv().value}"
                return f"{n1}.."
            return n1
        return self._adv().value

    def _finish_raw(self, initial: list[Token]) -> RawCond:
        tokens = list(initial)
        depth = 0
        while not self._match(TT.EOF):
            t = self._peek()
            if t.type == TT.LPAREN:
                depth += 1; tokens.append(self._adv())
            elif t.type == TT.RPAREN:
                if depth == 0:
                    break
                depth -= 1; tokens.append(self._adv())
            elif t.type == TT.IDENT and t.value in ('and', 'or') and depth == 0:
                break
            else:
                tokens.append(self._adv())
        return RawCond(tokens)

    def _wait_stmt(self) -> WaitStmt:
        self._adv()  # wait
        self._eat(TT.LPAREN)
        dur = self._eat(TT.TICK_DUR).value
        self._eat(TT.RPAREN)
        if self._peek().type == TT.IDENT and self._peek().value == 'then':
            self._adv()
        self._eat(TT.LBRACE)
        body = self._fn_body()
        self._eat(TT.RBRACE)
        self._eat_if(TT.SEMICOLON)
        return WaitStmt(int(dur[:-1]), dur[-1], body)

    # ---- score ----

    def _score_stmt(self) -> Node:
        target = self._adv().value   # SCORE

        # $obj = new("criterion", "display")
        if (self._match(TT.EQ) and
                self._peek(1).type == TT.IDENT and self._peek(1).value == 'new'):
            self._adv()   # =
            self._adv()   # new
            self._eat(TT.LPAREN)
            crit = self._eat(TT.STRING).value
            self._eat(TT.COMMA)
            disp = self._eat(TT.STRING).value
            self._eat(TT.RPAREN)
            self._eat_if(TT.SEMICOLON)
            return ScoreNewDecl(target, crit, disp)

        _OPS = {
            TT.EQ: '=', TT.PLUS_EQ: '+=', TT.MINUS_EQ: '-=',
            TT.STAR_EQ: '*=', TT.SLASH_EQ: '/=', TT.PERCENT_EQ: '%=',
        }
        if self._peek().type not in _OPS:
            self._eat_if(TT.SEMICOLON)
            return RawCmd(f"# unresolved: ${target}")
        op = _OPS[self._adv().type]
        rhs = self._score_rhs()
        self._eat_if(TT.SEMICOLON)
        return ScoreAssignStmt(target, op, rhs)

    def _score_rhs(self) -> Any:
        t = self._peek()
        if t.type == TT.NUMBER:
            return int(float(self._adv().value))
        if t.type == TT.SCORE:
            lhs = self._adv().value
            if self._peek().type in (TT.PLUS, TT.MINUS, TT.STAR, TT.SLASH):
                op = self._adv().value
                return ('arith', lhs, op, self._score_rhs())
            return ('score', lhs)
        if t.type == TT.TARGET_SEL:
            sel = self._adv().value
            path_parts: list[str] = []
            while self._match(TT.DOT):
                self._adv()
                path_parts.append(self._adv().value)
            fallback = None
            if self._match(TT.NULLCOAL):
                self._adv()
                fallback = int(float(self._eat(TT.NUMBER).value))
            return ('entity', sel, '.'.join(path_parts) if path_parts else None, fallback)
        if t.type == TT.BLOCK_POS:
            pos = self._adv().value
            bp_parts: list[str] = []
            while self._match(TT.DOT):
                self._adv()
                bp_parts.append(self._adv().value)
            bp_fallback = None
            if self._match(TT.NULLCOAL):
                self._adv()
                bp_fallback = int(float(self._eat(TT.NUMBER).value))
            return ('block', pos, '.'.join(bp_parts) if bp_parts else None, bp_fallback)
        return ('raw', self._adv().value)

    # ---- storage ----

    def _storage_stmt(self) -> StorageAssignStmt:
        target = self._adv().value   # STORAGE
        self._eat(TT.EQ)
        rhs = self._data_value()
        self._eat_if(TT.SEMICOLON)
        return StorageAssignStmt(target, rhs)

    def _data_value(self) -> Any:
        t = self._peek()
        if t.type == TT.LBRACE:
            return self._json_obj()
        if t.type == TT.LBRACKET:
            return self._json_arr()
        if t.type == TT.NUMBER:
            v = self._adv().value
            return float(v) if '.' in v else int(v)
        if t.type == TT.STRING:
            return self._adv().value
        if t.type == TT.IDENT and t.value in ('true', 'false'):
            return self._adv().value == 'true'
        if t.type == TT.SCORE:
            return ('score', self._adv().value)
        if t.type == TT.TARGET_SEL:
            sel = self._adv().value
            path_parts: list[str] = []
            while self._match(TT.DOT):
                self._adv()
                path_parts.append(self._adv().value)
            return ('entity', sel, '.'.join(path_parts) if path_parts else None)
        if t.type == TT.BLOCK_POS:
            pos = self._adv().value
            bp_parts: list[str] = []
            while self._match(TT.DOT):
                self._adv()
                bp_parts.append(self._adv().value)
            return ('block', pos, '.'.join(bp_parts) if bp_parts else None)
        # bare ident — may be minecraft:id
        if t.type == TT.IDENT:
            v = self._adv().value
            if self._match(TT.COLON):
                self._adv()
                return f"{v}:{self._adv().value}"
            return v
        return self._adv().value

    def _json_obj(self) -> dict:
        self._eat(TT.LBRACE)
        obj: dict = {}
        while not self._match(TT.RBRACE, TT.EOF):
            kt = self._peek()
            if kt.type == TT.STRING:
                key = self._adv().value
            elif kt.type == TT.IDENT:
                key = self._adv().value
            else:
                break
            self._eat(TT.COLON)
            obj[key] = self._data_value()
            self._eat_if(TT.COMMA)
        self._eat(TT.RBRACE)
        return obj

    def _json_arr(self) -> list:
        self._eat(TT.LBRACKET)
        arr: list = []
        while not self._match(TT.RBRACKET, TT.EOF):
            arr.append(self._data_value())
            self._eat_if(TT.COMMA)
        self._eat(TT.RBRACKET)
        return arr

    # ---- other namespace statements ----

    def _tag_decl(self) -> TagDecl:
        self._adv()   # tag
        name = self._adv().value
        self._eat(TT.LBRACE)
        values: list[str] = []
        while not self._match(TT.RBRACE, TT.EOF):
            t = self._peek()
            if t.type == TT.IDENT:
                v = self._adv().value
                if self._match(TT.COLON):
                    self._adv()
                    v += ':' + self._adv().value
                values.append(v)
            elif t.type == TT.TAG_REF:
                values.append('#' + self._adv().value)
            else:
                self._adv()
            self._eat_if(TT.COMMA)
        self._eat(TT.RBRACE)
        return TagDecl(name, values)

    def _tag_addition(self) -> TagAddition:
        ref = self._adv().value   # TAG_REF (without #)
        self._eat(TT.LSHIFT)
        fn_name = self._eat(TT.IDENT).value
        self._eat_if(TT.SEMICOLON)
        return TagAddition(ref, fn_name)

    def _module_call(self) -> ModuleCall:
        mod = self._adv().value
        self._eat(TT.DOT)
        method = self._adv().value
        self._eat(TT.LPAREN)
        args: list[Any] = []
        while not self._match(TT.RPAREN, TT.EOF):
            args.append(self._arg_value())
            self._eat_if(TT.COMMA)
        self._eat(TT.RPAREN)
        self._eat_if(TT.SEMICOLON)
        return ModuleCall(mod, method, args)

    def _arg_value(self) -> Any:
        t = self._peek()
        if t.type == TT.STRING:
            return self._adv().value
        if t.type == TT.NUMBER:
            v = self._adv().value
            return float(v) if '.' in v else int(v)
        if t.type == TT.IDENT:
            return ('ref', self._adv().value)
        if t.type == TT.SCORE:
            return ('score', self._adv().value)
        return self._adv().value

    def _recipe_decl(self) -> RecipeDecl:
        self._adv()   # recipe
        name = self._adv().value
        return RecipeDecl(name, self._json_obj())

    def _raw_cmd(self) -> RawCmd:
        parts: list[str] = []
        while not self._match(TT.SEMICOLON, TT.RBRACE, TT.EOF):
            parts.append(self._adv().value)
        self._eat_if(TT.SEMICOLON)
        return RawCmd(' '.join(parts))


# ===========================================================================
# Code Generator
# ===========================================================================

_ctr = Counter()


class CodeGenerator:
    def __init__(self) -> None:
        self._modules: dict[str, Any] = {}
        self._ns: Namespace | None = None
        self._fns: dict[str, Function] = {}
        self._objs: dict[str, ScoreboardObjective] = {}
        self._tags: dict[str, Tag] = {}

    def run(self, prog: Program) -> None:
        for node in prog.body:
            self._top(node)

    def _top(self, node: Node) -> None:
        if isinstance(node, Directive):
            self._directive(node)
        elif isinstance(node, NamespaceDecl):
            self._namespace(node)

    def _directive(self, d: Directive) -> None:
        m = re.match(r'require\(([^)]+)\)', d.text)
        if not m:
            return
        path = m.group(1)
        parts = path.rsplit('.', 1)
        try:
            if len(parts) == 2:
                mod = importlib.import_module(parts[0])
                self._modules[parts[1]] = getattr(mod, parts[1])
            else:
                self._modules[parts[0]] = importlib.import_module(parts[0])
        except (ImportError, AttributeError):
            pass

    def _namespace(self, node: NamespaceDecl) -> None:
        ns = Namespace(node.name)
        prev = (self._ns, self._fns, self._objs, self._tags)
        self._ns = ns
        self._fns = {}
        self._objs = {}
        self._tags = {}

        # first pass: pre-declare functions + objectives so later stmts can reference them
        for stmt in node.body:
            if isinstance(stmt, FnDecl):
                self._fns[stmt.name] = Function(ns / stmt.name)
            elif isinstance(stmt, ScoreNewDecl):
                self._objs[stmt.obj_name] = Scoreboard.objective(
                    stmt.obj_name,
                    Text.literal(stmt.display),
                    ObjectiveCriterion(stmt.criterion),
                )

        for stmt in node.body:
            self._ns_stmt(stmt, ns)

        self._ns, self._fns, self._objs, self._tags = prev

    def _ns_stmt(self, node: Node, ns: Namespace) -> None:
        if isinstance(node, FnDecl):
            self._fn_decl(node, ns)
        elif isinstance(node, TagDecl):
            self._tag_decl(node, ns)
        elif isinstance(node, TagAddition):
            self._tag_addition(node, ns)
        elif isinstance(node, RecipeDecl):
            self._recipe_decl(node, ns)
        elif isinstance(node, ModuleCall):
            self._module_call(node, ns)
        # ScoreNewDecl already handled in first pass

    def _fn_decl(self, node: FnDecl, ns: Namespace) -> None:
        func = self._fns.setdefault(node.name, Function(ns / node.name))
        for stmt in node.body:
            cmd = self._fn_stmt(stmt, ns, node.params, func)
            if cmd is not None:
                func.add_command(cmd)
        ns.add_function(func)
        if node.inside_tag:
            self._add_to_tag(node.inside_tag, func, ns)

    def _add_to_tag(self, ref: str, func: Function, ns: Namespace) -> None:
        tns, tpath = ref.split(':', 1) if ':' in ref else ('minecraft', ref)
        if tns == 'minecraft' and tpath == 'load':
            ns.minecraft.load.add_value(func)
        elif tns == 'minecraft' and tpath == 'tick':
            ns.minecraft.tick.add_value(func)
        else:
            if ref not in self._tags:
                ft = FunctionTag(Identifier.of(tns, tpath), [])
                self._tags[ref] = ft
                ns.add_tag(ft)
            self._tags[ref].add_value(func)

    def _tag_addition(self, node: TagAddition, ns: Namespace) -> None:
        func = self._fns.get(node.fn_name) or Function(ns / node.fn_name)
        self._add_to_tag(node.tag_ref, func, ns)

    def _tag_decl(self, node: TagDecl, ns: Namespace) -> None:
        items = [
            Item(Identifier.of(*v.split(':', 1)) if ':' in v else Identifier.of('minecraft', v))
            for v in node.values if not v.startswith('#')
        ]
        tag = ItemTag(ns / node.name, items)
        self._tags[node.name] = tag
        ns.add_tag(tag)

    def _recipe_decl(self, node: RecipeDecl, ns: Namespace) -> None:
        r = Recipe(Identifier.of(ns.name, node.name), node.data)
        ns.add_recipe(r)

    def _module_call(self, node: ModuleCall, ns: Namespace) -> None:
        cls = self._modules.get(node.module)
        if cls is None:
            return
        method = getattr(cls, node.method, None)
        if method is None:
            return
        resolved = [
            self._fns.get(a[1], a[1]) if isinstance(a, tuple) and a[0] == 'ref' else a
            for a in node.args
        ]
        result = method(*resolved)
        if hasattr(result, 'merge'):
            result.merge(ns)

    def _fn_stmt(self, node: Node, ns: Namespace, params: list[str], parent: Function) -> Any:
        if isinstance(node, SayStmt):
            return Say(node.message)
        if isinstance(node, EffectStmt):
            return self._effect(node)
        if isinstance(node, IfStmt):
            return self._if_stmt(node, ns, params, parent)
        if isinstance(node, WaitStmt):
            return self._wait_stmt(node, ns, params, parent)
        if isinstance(node, ScoreAssignStmt):
            return self._score_assign(node)
        if isinstance(node, StorageAssignStmt):
            return self._storage_assign(node)
        if isinstance(node, RawCmd):
            return CustomCommand(node.text)
        return None

    def _effect(self, node: EffectStmt) -> CustomCommand:
        eff_id = node.effect_id if ':' in node.effect_id else f"minecraft:{node.effect_id}"
        if node.sub == 'clear':
            return CustomCommand(f"effect clear {node.target}")
        parts = ["effect give", node.target, eff_id]
        if node.seconds is not None:
            parts.append(str(node.seconds))
        if node.amplifier is not None:
            parts.append(str(node.amplifier))
        if node.hide is not None:
            parts.append("true" if node.hide else "false")
        return CustomCommand(' '.join(parts))

    def _if_stmt(self, node: IfStmt, ns: Namespace, params: list[str], parent: Function) -> Any:
        assert self._ns is not None
        anon = Function(self._ns / f"__if_{_ctr}")
        for stmt in node.body:
            cmd = self._fn_stmt(stmt, ns, params, anon)
            if cmd:
                anon.add_command(cmd)
        ns.add_function(anon)

        if_cmds = self._cond_to_commands(node.condition, str(anon.id))

        if node.else_body:
            else_fn = Function(self._ns / f"__else_{_ctr}")
            for stmt in node.else_body:
                c = self._fn_stmt(stmt, ns, params, else_fn)
                if c:
                    else_fn.add_command(c)
            ns.add_function(else_fn)
            else_cmds = self._else_cmds(node.condition, str(else_fn.id))
            return CustomCommand('\n'.join(if_cmds + else_cmds))
        return CustomCommand('\n'.join(if_cmds))

    def _cond_to_if_chunks(self, cond: Any) -> list[str]:
        if isinstance(cond, ScoreMatchesCond):
            obj_name, holder = cond.score.split(':', 1) if ':' in cond.score else (cond.score, 'value')
            return [f"score {holder} {obj_name} matches {cond.range_str}"]
        if isinstance(cond, ScoreCompareCond):
            lo, lh = cond.left.split(':', 1) if ':' in cond.left else (cond.left, 'value')
            ro, rh = cond.right.split(':', 1) if ':' in cond.right else (cond.right, 'value')
            return [f"score {lh} {lo} {cond.op} {rh} {ro}"]
        if isinstance(cond, AndCond):
            return self._cond_to_if_chunks(cond.left) + self._cond_to_if_chunks(cond.right)
        if isinstance(cond, RawCond):
            return [_tokens_to_str(cond.tokens)]
        return []

    def _cond_to_commands(self, cond: Any, fn_id: str) -> list[str]:
        if isinstance(cond, OrCond):
            return (
                self._cond_to_commands(cond.left, fn_id) +
                self._cond_to_commands(cond.right, fn_id)
            )
        chunks = self._cond_to_if_chunks(cond)
        return [f"execute {' '.join(f'if {c}' for c in chunks)} run function {fn_id}"]

    def _else_cmds(self, cond: Any, else_fn_id: str) -> list[str]:
        if isinstance(cond, OrCond):
            # !(A || B) = !A && !B  — chain all unless in one execute
            if not isinstance(cond.left, OrCond) and not isinstance(cond.right, OrCond):
                all_chunks = self._cond_to_if_chunks(cond.left) + self._cond_to_if_chunks(cond.right)
                return [f"execute {' '.join(f'unless {c}' for c in all_chunks)} run function {else_fn_id}"]
            # nested or: recurse
            return self._else_cmds(cond.left, else_fn_id) + self._else_cmds(cond.right, else_fn_id)
        if isinstance(cond, AndCond):
            # !(A && B) = !A || !B
            # execute unless A run else_fn
            # execute if A unless B run else_fn
            lc = self._cond_to_if_chunks(cond.left)
            rc = self._cond_to_if_chunks(cond.right)
            unless_left = ' '.join(f'unless {c}' for c in lc)
            if_left_unless_right = ' '.join(f'if {c}' for c in lc) + ' ' + ' '.join(f'unless {c}' for c in rc)
            return [
                f"execute {unless_left} run function {else_fn_id}",
                f"execute {if_left_unless_right} run function {else_fn_id}",
            ]
        chunks = self._cond_to_if_chunks(cond)
        return [f"execute {' '.join(f'unless {c}' for c in chunks)} run function {else_fn_id}"]

    def _wait_stmt(self, node: WaitStmt, ns: Namespace, params: list[str], parent: Function) -> Any:
        assert self._ns is not None
        anon = Function(self._ns / f"__wait_{_ctr}")
        for stmt in node.body:
            cmd = self._fn_stmt(stmt, ns, params, anon)
            if cmd:
                anon.add_command(cmd)
        ns.add_function(anon)
        _unit_map = {'t': 'tick', 's': 'second', 'd': 'day'}
        return Schedule.function(anon, node.ticks, _unit_map.get(node.unit, 'tick'))  # type: ignore[arg-type]

    def _score_assign(self, node: ScoreAssignStmt) -> CustomCommand | None:
        obj_name, holder = node.target.split(':', 1) if ':' in node.target else (node.target, 'value')
        obj = self._objs.get(obj_name) or _dummy_obj(obj_name)
        player = obj.player(holder)
        rhs = node.rhs

        if isinstance(rhs, int):
            if node.op == '=':    return player.set(rhs)
            if node.op == '+=':   return player.add(rhs)
            if node.op == '-=':   return player.remove(rhs)
            return player.set(rhs)

        if isinstance(rhs, tuple):
            kind = rhs[0]
            if kind == 'score':
                o2, h2 = rhs[1].split(':', 1) if ':' in rhs[1] else (rhs[1], 'value')
                obj2 = self._objs.get(o2) or _dummy_obj(o2)
                return player.operation(obj2.player(h2), _score_op(node.op))  # type: ignore[arg-type]

            if kind == 'entity':
                _, sel, path, fallback = rhs
                base = f"execute store result score {holder} {obj_name} run data get entity {sel}"
                if path:
                    base += f" {path}"
                if fallback is not None:
                    base += (
                        f"\nexecute unless data entity {sel} "
                        f"run scoreboard players set {holder} {obj_name} {fallback}"
                    )
                return CustomCommand(base)

            if kind == 'block':
                _, pos, path, _ = rhs
                base = f"execute store result score {holder} {obj_name} run data get block {pos}"
                if path:
                    base += f" {path}"
                return CustomCommand(base)

            if kind == 'arith':
                _, lhs_str, op, rhs2 = rhs
                o1, h1 = lhs_str.split(':', 1) if ':' in lhs_str else (lhs_str, 'value')
                obj1 = self._objs.get(o1) or _dummy_obj(o1)
                p1 = obj1.player(h1)
                arith_op = {'+': '+=', '-': '-=', '*': '*=', '/': '/='}.get(op, op)
                return CustomCommand(
                    player.operation(p1, '=').to_string() + '\n' +
                    player.operation(p1, arith_op).to_string()  # type: ignore[arg-type]
                )

        return None

    def _storage_assign(self, node: StorageAssignStmt) -> CustomCommand | None:
        # &ns:storagename.key.path  →  StorageID=ns:storagename  data_path=key.path
        if ':' in node.target:
            ns_part, rest = node.target.split(':', 1)
        else:
            ns_part, rest = 'temp', node.target

        dot = rest.find('.')
        if dot == -1:
            storage_id = Identifier.of(ns_part, rest)
            data_path: str | None = None
        else:
            storage_id = Identifier.of(ns_part, rest[:dot])
            data_path = rest[dot + 1:]

        storage = DataStorage(storage_id)
        rhs = node.rhs

        if isinstance(rhs, tuple):
            kind = rhs[0]
            if kind == 'entity':
                _, sel, ent_path = rhs
                target_path = data_path or 'root'
                if ent_path:
                    return storage.set_from_entity(target_path, TargetSelector(sel), ent_path)
                return storage.set_from_entity(target_path, TargetSelector(sel))
            if kind == 'block':
                _, pos, block_path = rhs
                target_path = data_path or 'root'
                if block_path:
                    return CustomCommand(f"data modify storage {storage_id} {target_path} set from block {pos} {block_path}")
                return CustomCommand(f"data modify storage {storage_id} {target_path} set from block {pos}")
            if kind == 'score':
                o, h = rhs[1].split(':', 1) if ':' in rhs[1] else (rhs[1], 'value')
                target_path = data_path or 'value'
                return CustomCommand(
                    f"execute store result storage {storage_id} {target_path} int 1 "
                    f"run scoreboard players get {h} {o}"
                )

        if data_path:
            try:
                return storage.set(data_path, _json.dumps(rhs))
            except Exception:
                return storage.set(data_path, str(rhs))
        else:
            # no key → merge whole storage
            try:
                return CustomCommand(f"data merge storage {storage_id} {_json.dumps(rhs)}")
            except Exception:
                return CustomCommand(f"data merge storage {storage_id} {rhs}")


# ===========================================================================
# Helpers
# ===========================================================================

def _score_op(op: str) -> str:
    return {'=': '=', '+=': '+=', '-=': '-=', '*=': '*=', '/=': '/=', '%=': '%='}.get(op, '=')


def _dummy_obj(name: str) -> ScoreboardObjective:
    return ScoreboardObjective(name, Text.literal(name), ObjectiveCriterion.DUMMY)


def _tokens_to_str(tokens: list[Token]) -> str:
    parts: list[str] = []
    for t in tokens:
        if t.type == TT.SCORE:
            parts.append(f"${t.value}")
        elif t.type == TT.STORAGE:
            parts.append(f"&{t.value}")
        elif t.type == TT.TAG_REF:
            parts.append(f"#{t.value}")
        elif t.type == TT.TARGET_SEL:
            parts.append(t.value)
        elif t.type == TT.STRING:
            parts.append(f'"{t.value}"')
        elif t.type == TT.DOTDOT:
            parts.append('..')
        elif t.type == TT.BLOCK_POS:
            parts.append(f'&({t.value})')
        else:
            parts.append(t.value)
    return ' '.join(parts)


# ===========================================================================
# Public API
# ===========================================================================

class ScriptLanguage:
    @staticmethod
    def compile(source: str) -> None:
        """Parse and compile a ScriptLanguage DSL string into datagen artifacts."""
        tokens = Tokenizer(source).tokenize()
        ast = Parser(tokens).parse()
        CodeGenerator().run(ast)
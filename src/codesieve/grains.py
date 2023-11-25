from __future__ import annotations

from typing import Callable, Literal

from tree_sitter import Parser, Node

from ._defaults import LEVEL, DIST
from .walker import treewalk

DistFunc = Callable[[Node, tuple[int, int]], int]


def start2start(node: Node, span: tuple[int, int]):
    return abs(node.start_byte - span[0])


def end2end(node: Node, span: tuple[int, int]):
    return abs(node.end_byte - span[1])


def inbetween(node: Node, span: tuple[int, int]):
    return start2start(node, span) + end2end(node, span)


def start2end(node: Node, span: tuple[int, int]):
    return abs(node.start_byte - span[1])


def end2start(node: Node, span: tuple[int, int]):
    return abs(node.end_byte - span[0])


def closeref(
        nodes: list[Node],
        span: tuple[int, int],
        distfunc: DistFunc | Literal['s2s', 'e2e', 'btw', 's2e', 'e2s'] = None
):
    if distfunc is None:
        distfunc = DIST

    if isinstance(distfunc, str):
        if distfunc == 's2s':
            distfunc = start2start
        elif distfunc == 'e2e':
            distfunc = end2end
        elif distfunc == 'btw':
            distfunc = inbetween
        elif distfunc == 's2e':
            distfunc = start2end
        elif distfunc == 'e2s':
            distfunc = end2start
        else:
            raise TypeError(f'`{distfunc}` is not an accepted distance function.')

    refdists = [(el, distfunc(el, span)) for el in nodes]
    close = min(refdists, key=lambda x: x[1])
    return close[0]


def getparent(node: Node | None, types: list[str], level: int = None):
    if level is None:
        level = LEVEL

    if len(types) == 0:
        raise RuntimeError('Allowed parent node types should not be empty.')
    if node is None:
        return node
    typeset = set(types)

    if level == 0:
        if node.type in typeset:
            return node
        return None

    currentlevel = 0
    if node.type in typeset:
        currentlevel += 1

    currentnode = node
    while currentlevel < level and currentnode is not None:
        currentnode = currentnode.parent
        if currentnode is not None and currentnode.type in typeset:
            currentlevel += 1

    return currentnode


def linegrained(_, context: str, span: tuple[int, int], *, level: int = None):
    if level is None:
        level = LEVEL
    if level == 0:
        return ''

    startline = len(context[0: span[0]].splitlines())
    endline = len(context[0: span[1]].splitlines())

    lines = context.splitlines()
    text = '\n'.join(lines[max(0, startline - level):min(len(lines), endline + level - 1)])
    return text


def functiongrained(parser: Parser, context: str, span: tuple[int, int], *, level: int = None, dist: str = None):
    if level is None:
        level = LEVEL
    if level == 0:
        return ''

    nodes = [*treewalk(parser.parse(context.encode('utf-8')))]
    if len(nodes) == 0:
        return ''
    ref = closeref(nodes, span, distfunc=dist)
    parent = getparent(
        ref,
        [
            'arrow_function', 'function_declaration', 'method_definition', 'method_declaration',
            'function', 'method', 'function_definition'
        ]
    )
    if parent is None:
        return ''
    return parent.text.decode('utf-8')


def classgrained(parser: Parser, context: str, span: tuple[int, int], *, level: int = None, dist: str = None):
    if level is None:
        level = LEVEL
    if level == 0:
        return ''

    nodes = [*treewalk(parser.parse(context.encode('utf-8')))]
    if len(nodes) == 0:
        return ''
    ref = closeref(nodes, span, distfunc=dist)
    parent = getparent(
        ref, ['class_declaration', 'class_specifier', 'class_definition'])
    if parent is None:
        return ''
    return parent.text.decode('utf-8')


def finegrained(
        parser: Parser,
        context: str,
        span: tuple[int, int],
        *,
        clazz: Literal['line', 'function', 'class'],
        level: int = None,
        dist: DistFunc | Literal['s2s', 'e2e', 'btw', 's2e', 'e2s'] = None
):
    if clazz == 'line':
        return linegrained(None, context=context, span=span, level=level)
    if clazz == 'function':
        return functiongrained(parser=parser, context=context, span=span, level=level, dist=dist)
    if clazz == 'class':
        return functiongrained(parser=parser, context=context, span=span, level=level, dist=dist)
    raise TypeError(f'`{clazz}` is not supported by the fine grainer.')

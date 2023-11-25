import difflib
from typing import Iterable

import numpy as np
from tree_sitter import Parser

from ._defaults import LIMIT
from .sieve import Granulator, LineGranulator, FunctionGranulator, ClassGranulator


class GranulateCollector:
    def __init__(self, granulator: Granulator):
        self._granulator = granulator

    def collect(self, text: str, spans: Iterable[tuple[int, int]]):
        memory = set()
        buffer = []

        for span in spans:
            granulatum = self._granulator.sieve(text, span)
            if granulatum not in memory:
                memory.add(granulatum)
                buffer.append(granulatum)

        return buffer

    def collectall(self, texts: Iterable[str], spans: Iterable[Iterable[tuple[int, int]]]):
        for text, span in zip(texts, spans):
            data = self.collect(text, span)
            for el in data:
                yield el


def datasieve(srcparser, tgtparser, src, tgt, clazz, level=None, limit=None, dist=None):
    """
    Dataset sieve.

    Parameters:
        srcparser (Parser):
        tgtparser (Parser):
        src (str):
        tgt (str):
        clazz (Literal['line', 'function', 'class']):
        level (int):
        limit (int):
        dist (Literal['s2s', 'e2e', 'btw', 's2e', 'e2s']):

    Returns:
        (list[str]): dataparts falling through the sieve
    """
    if limit is None:
        limit = LIMIT
    if len(src) > limit or len(tgt) > limit:
        return []

    if clazz == 'line':
        srcgrain = LineGranulator(srcparser, level=level)
        tgtgrain = LineGranulator(tgtparser, level=level)
    elif clazz == 'function':
        srcgrain = FunctionGranulator(srcparser, level=level, dist=dist)
        tgtgrain = FunctionGranulator(tgtparser, level=level, dist=dist)
    elif clazz == 'class':
        srcgrain = ClassGranulator(srcparser, level=level, dist=dist)
        tgtgrain = ClassGranulator(tgtparser, level=level, dist=dist)
    else:
        raise TypeError(f'Type of `{clazz} is not supported.')

    srccollector = GranulateCollector(srcgrain)
    tgtcollector = GranulateCollector(tgtgrain)

    src_lines = src.splitlines(keepends=True)
    tgt_lines = tgt.splitlines(keepends=True)
    matcher = difflib.SequenceMatcher(None, src_lines, tgt_lines)
    src_ll = [len(ln) for ln in src_lines]
    tgt_ll = [len(ln) for ln in tgt_lines]
    src_cll = np.cumsum(src_ll).tolist()
    tgt_cll = np.cumsum(tgt_ll).tolist()
    opcodes = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag != 'equal':
            try:
                opcodes.append((
                    tag, src_cll[i1], src_cll[i2 - 1] + src_ll[i2 - 1],
                    tgt_cll[j1], tgt_cll[j2 - 1] + tgt_ll[j2 - 1])
                )
            except IndexError:
                continue

    srcdatapreview = srccollector.collect(src, [(el[1], el[2]) for el in opcodes])
    tgtdatapreview = tgtcollector.collect(tgt, [(el[3], el[4]) for el in opcodes])
    pairs = [
        (src, tgt) for src, tgt in zip(srcdatapreview, tgtdatapreview)
        if src != tgt != '' and not src.isspace() and not tgt.isspace()
    ]

    if len(pairs) == 0:
        return []

    return pairs

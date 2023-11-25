from __future__ import annotations

import abc
from typing import overload, Literal

from tree_sitter import Parser
from tree_sitter_languages import get_parser

from ._defaults import LEVEL, DIST
from .grains import finegrained


class Granulator(abc.ABC):
    _parser: Parser
    _level: int
    _dist: Literal['s2s', 'e2e', 'btw', 's2e', 'e2s']

    @overload
    def __init__(self, parser: Parser, level: int = LEVEL, dist: Literal['s2s', 'e2e', 'btw', 's2e', 'e2s'] = DIST):
        ...

    @overload
    def __init__(self, lang: str, level: int = LEVEL, dist: Literal['s2s', 'e2e', 'btw', 's2e', 'e2s'] = DIST):
        ...

    def __init__(self, *args, **kwargs):
        """
        TODO: description
        """

        assert len(args) > 0 or 'parser' in kwargs or 'lang' in kwargs, 'The first parameter is mandatory.'
        parser_or_lang = args[0] if len(args) > 0 else kwargs.get('parser', kwargs['lang'])
        assert isinstance(parser_or_lang, (str, Parser)), f'First argument must be of type {str} or {Parser}.'
        if isinstance(parser_or_lang, str):
            self._parser = get_parser(language=parser_or_lang)
        else:
            self._parser = parser_or_lang
        self._level = kwargs.get('level', LEVEL)
        self._dist = kwargs.get('dist', DIST)
        assert isinstance(self._level, int) and self._level > 0, 'Param `level` must be of type int and > 0.'

    @abc.abstractmethod
    def sieve(self, context, span, *, level=None):
        """
        Selects the specified level of fine graining.

        Parameters:
            context (str): context (possibly the whole source code) of the grain to be found
            span (tuple[int, int]): approximate location in code
            level (int): nesting level of fine graining (defaults to 1)
        Returns:
            str: the code grains falling through the specified sieve
        """


class LineGranulator(Granulator):
    def sieve(self, context, span, *, level=None):
        return finegrained(self._parser, context=context, span=span, clazz='line', level=level)


class FunctionGranulator(Granulator):
    def sieve(self, context, span, *, level=None):
        return finegrained(self._parser, context=context, span=span, clazz='function', level=level, dist=self._dist)


class ClassGranulator(Granulator):
    def sieve(self, context, span, *, level=None):
        return finegrained(self._parser, context=context, span=span, clazz='class', level=level, dist=self._dist)

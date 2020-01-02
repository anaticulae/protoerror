# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import dataclasses
import re
import typing

from protocol.solution import Solution


@dataclasses.dataclass(unsafe_hash=True)
class Location:
    """The location defines the object on which the Finding belongs to.

    Examples for location:
        page                p10
        chapter             c2     p10
        section             sec3   p5
        paragraph           pa5    p10
        sentence            s10    p10
        word                w100   p13
        char                cr137  p4
        whitespace          ws17   p3
        image               i1     p1
        oneline             ol5    p13
    """
    page: int = -1
    shortcut: str = None
    value: int = None

    def raw(self) -> str:  # pylint:disable=no-self-use
        value = self.value if self.value else ''
        if self.shortcut == 'p':
            return f'p{self.page}'
        return f'{self.shortcut}{value}p{self.page}'

    PATTERN = re.compile(r'((?P<shortcut>[a-z]+)(?P<value>\d+))?p(?P<page>\d+)')

    @classmethod
    def fromstr(cls, raw: str):
        if not raw:
            return None
        matched = re.match(Location.PATTERN, raw)
        if not matched:
            return None

        page, shortcut, value = int(matched['page']), 'p', None
        with contextlib.suppress(TypeError):
            value = int(matched['value'])
            shortcut = matched['shortcut']

        result = cls(page=page, shortcut=shortcut, value=value)
        return result

    @classmethod
    def from_page(cls, page: int):
        assert page >= 0, str(page)
        return cls.fromstr(f'p{page}')

    @classmethod
    def from_chapter(cls, chapter: int, page: int):
        assert page >= 0, str(page)
        assert chapter >= 0, str(chapter)
        return cls.fromstr(f'c{chapter}p{page}')

    @classmethod
    def from_oneline(cls, line: int, page: int):
        assert page >= 0, str(page)
        assert line >= 0, str(line)
        return cls.fromstr(f'ol{line}p{page}')


@dataclasses.dataclass(unsafe_hash=True)
class Finding:  # pylint:disable=R0903
    """Non active findings are presentend to the use cause of lag of
    quality. There purpose is to improve the platform. A second point
    for non presenting is a to low confidence of the result.
    """

    number: int = dataclasses.field(compare=False, default=-1)
    location: Location = None
    msgid: str = None
    solution: Solution = None
    confidence: float = None
    active: bool = False


Findings = typing.List[Finding]


@dataclasses.dataclass
class PageFinding:
    page: int = None
    content: Findings = dataclasses.field(default_factory=list)

    def __len__(self):
        return len(self.content)

    def __getitem__(self, index):
        return self.content[index]  # pylint:disable=E1136

    def append(self, item):
        self.content.append(item)  # pylint:disable=E1101


PageFindings = typing.List[PageFinding]

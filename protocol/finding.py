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

import utila
import yaml

import protocol
from protocol.solution import Solution


@dataclasses.dataclass(unsafe_hash=True)
class Location:
    """The location defines the object on which the Finding belongs to.

    .. code-block :: none

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
    def from_sentence(cls, sentence: int, page: int):
        assert page >= 0, str(page)
        assert sentence >= 0, str(sentence)
        return cls.fromstr(f's{sentence}p{page}')

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
class RangedLocation:
    """RangedLocation defines a mark which can include more than one
    page, line and token definition.

    Examples:

    - ('p10_12~l6_9~t5_19', protocol.RangedLocation(10, 12, 6, 9, 5, 19))
    - ('p10_12~l6~t5', protocol.RangedLocation(10, 12, line=6, token=5))
    - ('p10~l6', protocol.RangedLocation(page=10, line=6))
    - ('p5', protocol.RangedLocation(page=5))
    - ('p5~t17', protocol.RangedLocation(page=5, token=17))
    """
    page: int = None
    page_end: int = None
    line: int = None
    line_end: int = None
    token: int = None
    token_end: int = None

    PATTERN = re.compile(r'p(?P<page>\d+)(_(?P<page_end>\d+))?[~]?'
                         r'(l(?P<line>\d+)(_(?P<line_end>\d+))?[~]?)?'
                         r'(t(?P<token>\d+)(_(?P<token_end>\d+))?)?')

    @classmethod
    def fromstr(cls, raw: str):
        matched = re.match(RangedLocation.PATTERN, raw)
        if not matched:
            return None
        result = RangedLocation()
        for item in [
                'page',
                'page_end',
                'line',
                'line_end',
                'token',
                'token_end',
        ]:
            with contextlib.suppress(TypeError):
                setattr(result, item, int(matched[item]))
        return result

    def raw(self) -> str:
        result = f'p{self.page}'
        if self.page_end is not None:
            result += f'_{self.page_end}'
        if self.line is not None:
            result += f'~l{self.line}'
        if self.line_end is not None:
            result += f'_{self.line_end}'
        if self.token is not None:
            result += f'~t{self.token}'
        if self.token_end is not None:
            result += f'_{self.token_end}'
        return result


@dataclasses.dataclass(unsafe_hash=True)
class BoundingLocation:
    """The location defines the object on which the Finding belongs to.
    Defines rectangle which can be highlighted in further presentation
    steps. The rectangle is the simplest highlighting method.

    .. code-block :: none

        Examples for location:

        bounding    b(137.0;145.0;123.0;232.0)p5
    """
    page: int = -1
    shortcut: str = None
    value: tuple = None

    PATTERN = r'(?P<shortcut>b)\((?P<tuple>((\d+\.\d+;{0,1}){4}))\)p(?P<page>\d+)'

    def __str__(self) -> str:
        joined = ';'.join([str(item) for item in self.value])  # pylint:disable=E1133
        raw = f'b({joined})p{self.page}'
        return raw

    @classmethod
    def fromstr(cls, raw: str):
        assert raw, 'require input'
        matched = re.match(BoundingLocation.PATTERN, raw)
        if not matched:
            return None

        page, shortcut, value = int(matched['page']), 'b', None
        value = matched['tuple'].split(';')
        value = utila.roundme([float(item) for item in value])
        value = tuple(value)
        shortcut = matched['shortcut']
        result = cls(page=page, shortcut=shortcut, value=value)
        return result

    @classmethod
    def fromtuple(cls, bounding: tuple, page: int):
        return cls(shortcut='b', page=page, value=bounding)


@dataclasses.dataclass(unsafe_hash=True)
class Finding:  # pylint:disable=R0903
    """Non active findings are not presentend to the user cause of lag
    of quality. There purpose is to improve the platform. A second point
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


def load_result(path: str) -> Findings:
    """Load list of `Finding`s which was produced by linter

    Args:
        path(str): path to file with lists of `Finding`
    Returns:
        list of Finding
    Raises:
        Assertion: if file is corrupt
    """
    raw = utila.from_raw_or_path(path)
    loaded = yaml.load(raw, yaml.FullLoader)

    assert isinstance(loaded, list), type(loaded)
    assert all([isinstance(item, Finding) for item in loaded]), str(loaded)
    return loaded

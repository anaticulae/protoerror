# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import concurrent.futures
import contextlib
import dataclasses
import enum
import os
import re
import typing

import utila
import utila.feature.processor
import yaml

import protocol
from protocol.solution import ProblemStatus
from protocol.solution import Solution

SUMMARY = -1


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
        assert page >= SUMMARY, str(page)
        return cls.fromstr(f'p{page}')

    @classmethod
    def from_sentence(cls, sentence: int, page: int):
        assert page >= SUMMARY, str(page)
        assert sentence >= 0, str(sentence)
        return cls.fromstr(f's{sentence}p{page}')

    @classmethod
    def from_chapter(cls, chapter: int, page: int):
        assert page >= SUMMARY, str(page)
        assert chapter >= 0, str(chapter)
        return cls.fromstr(f'c{chapter}p{page}')

    @classmethod
    def from_oneline(cls, line: int, page: int):
        assert page >= SUMMARY, str(page)
        assert line >= 0, str(line)
        return cls.fromstr(f'ol{line}p{page}')


SUMMARY_LOCATION = Location.from_page(SUMMARY)


@dataclasses.dataclass(unsafe_hash=True)
class RangedLocation:
    """RangedLocation defines a mark which can include more than one
    page, line and token definition.

    >>> RangedLocation.fromstr('p10_12~l6_9~t5_19')
    RangedLocation(page=10, page_end=12, line=6, line_end=9, token=5, token_end=19)
    >>> RangedLocation.fromstr('p10_12~l6~t5')
    RangedLocation(page=10, page_end=12, line=6, token=5)
    >>> RangedLocation.fromstr('p10~l6')
    RangedLocation(page=10, line=6)
    >>> RangedLocation.fromstr('p5')
    RangedLocation(page=5)
    >>> RangedLocation.fromstr('p5~t17')
    RangedLocation(page=5, token=17)
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

    KEYS = ['page', 'page_end', 'line', 'line_end', 'token', 'token_end']

    @classmethod
    def fromstr(cls, raw: str):
        matched = re.match(RangedLocation.PATTERN, raw)
        if not matched:
            return None
        result = RangedLocation()
        for item in RangedLocation.KEYS:
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

    def __repr__(self):
        values = [
            f'{key}={getattr(self, key)}' for key in RangedLocation.KEYS
            if getattr(self, key) is not None
        ]
        values = ', '.join(values)
        return f'RangedLocation({values})'

    @property
    def shortcut(self):
        return 'r'


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


class FindingLevel(enum.Enum):
    """Define how important an `Finding` is.

    Color:
        green(1)
        yellow(2, 3, 6)
        red(8, 10)
    """
    # MESSAGE = 0 ???
    # advice to use other pattern or style
    ADVICE = 1
    # page order
    CONVENTION = 2
    # style of paragraph, page
    REFACTOR = 3
    # umgangssprache, image black and white problem
    WARNING = 6
    # writing over border
    ERROR = 8
    # pdf analyzing error
    FATAL = 10
    UNDEFINED = -1


@dataclasses.dataclass(unsafe_hash=True)
class Finding:  # pylint:disable=R0903
    """Non active findings are not presentend to the user cause of lag
    of quality. There purpose is to improve the platform. A second point
    for non presenting is a to low confidence of the result."""

    number: int = dataclasses.field(compare=False, hash=False, default=-1)
    location: Location = None
    # how important a level is
    level: FindingLevel = None
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


def load_result(path: str, msgids: set = None) -> Findings:
    """Load list of `Finding`s which was produced by linter

    Args:
        path(str): path to file with lists of `Finding`
        msgids(set): set of selected Findings; if msgids is None, select all
    Returns:
        list of Finding
    Raises:
        Assertion: if file is corrupt
    """
    raw = utila.from_raw_or_path(path)
    loaded = yaml.load(raw, yaml.FullLoader)

    assert isinstance(loaded, list), type(loaded)
    assert all([isinstance(item, Finding) for item in loaded]), str(loaded)

    result = protocol.select_findings(loaded, msgids)
    return result


def findings_from_path(path: str, worker: int = 10) -> PageFindings:
    """Load Findings from `path` directory and group them by page as
    `PageFindings`."""
    assert os.path.isdir(path), str(path)
    files = utila.file_list(path, include='yaml', recursive=True)
    files = [item for item in files if utila.file_name(item).endswith('_user')]
    paths = [os.path.join(path, item) for item in files]

    # limit worker by max file count
    worker = utila.mins(worker, len(files))
    # ensure to have at least one worker when collection now file
    worker = utila.maxs(1, worker)
    # yaml parsing is cpu bound, therefore we need a process pool instead
    # of thread pool.
    executor = utila.feature.processor.select_executor()
    with executor(max_workers=worker) as executor:
        todo = {
            executor.submit(protocol.load_result, path): path for path in paths
        }
        findings = []
        for job in concurrent.futures.as_completed(todo):
            data = job.result()
            findings.extend(data)
    result = protocol.bypage(findings)
    return result


def dump_findings(findings: list) -> str:
    # TODO: MOVE TO SERIALIZERAW AND REPLACE WITH HAND MADE DUMPING
    assert isinstance(findings, list), type(findings)
    for item in findings:
        if not item.solution:
            continue
        try:
            description = item.solution.description
        except AttributeError:
            continue
        message = f'template is not fully replaced:\n{description}'
        # ensure that the user could not see any not fully replaced templates
        assert utila.istemplate_replaced(item.solution.description), message
    dumped = yaml.dump(findings)
    return dumped


def iter_findings(path: str):
    files = utila.file_list(path, include='yaml', recursive=True)
    files = [item for item in files if utila.file_name(item).endswith('_user')]
    for item in files:
        location = os.path.join(path, item)
        findings = load_result(location)

        yield location, findings


def hash_finding(item):
    return hash(item)


def make_finding_number_unique(path: str) -> bool:
    """Collect all findings from path and replace with unqiue finding
    number.

    Note: Remove lintings with equal hash cause there seem/must to be
          equal.

    Args:
        path(str): location where files wither user linter are located
    Returns:
        True if some file was located and replace.
        False if no user file is in `path`.
    """
    assert os.path.isdir(path), str(path)
    single = utila.Single()
    replaced = False
    for location, findings in iter_findings(path):
        for finding in findings:
            hashed = hash_finding(finding)
            if single.contains(hashed):
                utila.error(f'duplicated finding: {finding}')
                finding.number = None  # None -> do not dump this finding
                continue
            finding.number = hashed
        findings = [item for item in findings if item.number is not None]
        # TODO: REFACTOR LATER
        dumped = dump_findings(findings)
        utila.file_replace(location, dumped)
        replaced = True
    return replaced


def finding_status_update(
        path: str,
        number: int,
        status: ProblemStatus,
) -> bool:
    assert os.path.isdir(path), str(path)
    assert isinstance(status, ProblemStatus), type(status)
    # TODO: IMPROVE SPEED LATER? MAY USE A BUFFERED OBJECT ORIENTED APPROACH
    for location, findings in iter_findings(path):
        for finding in findings:
            if finding.number != number:
                continue
            if finding.solution is None:
                utila.error(f'could not update status: {finding}')
                return False
            finding.solution.status = status
            dumped = dump_findings(findings)
            utila.file_replace(location, dumped)
            return True
    return False


def finding_status(path: str, number: int) -> ProblemStatus:
    assert os.path.isdir(path), str(path)
    assert isinstance(number, int), type(number)
    for _, findings in iter_findings(path):
        for finding in findings:
            if finding.number != number:
                continue
            if finding.solution is None:
                utila.error(f'could not get status: {finding}')
                return None
            return finding.solution.status
    return None

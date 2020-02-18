# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Solution
========

Solution describes a possible fix for the user to solve an error
which was told by checker.

Possible solution:
 * Hint as text block
 * Homepage
 * Link to internal documentation

.. code-block :: none

    Writen over border
    ------------------
    id:int
    msgid/problem:E0007
    title: Text element hits the autodetected border
    description:
    solution:open,hide,disagree,solved

    solution:
      open
      hide
      disagree
      solved

Enable printing solution list, does we need this?
"""
import contextlib
import copy
import dataclasses
import enum
import re
import typing

import utila

import protocol.utils


class ProblemStatus(enum.Enum):
    OPEN = enum.auto()  # default status when non-CLOSED problem appears
    HIDDEN = enum.auto()  # user don't want to see this message
    DISAGREE = enum.auto()  # false alarm or user does agree with judgement
    SOLVED = enum.auto()  # user solved this issue in there document
    CLOSED = enum.auto()  # user can not change this state, e.g. pdf read error


@dataclasses.dataclass(unsafe_hash=True)  # pylint:disable=R0903
class Solution:
    number: int = dataclasses.field(compare=False, default=-1)
    msgid: str = None
    status: ProblemStatus = ProblemStatus.OPEN


Solutions = typing.List[Solution]
Validators = typing.List[callable]


@dataclasses.dataclass(unsafe_hash=True)  # pylint:disable=R0903
class Text(Solution):
    title: str = None
    description: str = None


@dataclasses.dataclass(unsafe_hash=True)  # pylint:disable=R0903
class Web(Text):

    hyperlinks: list = dataclasses.field(default=list)
    """List of hyperlinks to underline the description."""


@dataclasses.dataclass(unsafe_hash=True)  # pylint:disable=R0903
class Doctails(Text):
    """Describes link to internal documentation database.

    Example:
     * `/writing/manuskript/zitate`
     * `/writing/user`
    """


class Solver:

    def __init__(self):
        self.solutions = {}

    def add_solution(self, msgid: str, solution: Solution):
        assert msgid, solution
        self.solutions[msgid] = solution

    def append(self, item: Solution):
        self.solutions[item.msgid] = item

    def solution(self, msgid: str, **kwargs) -> Solution:
        try:
            result = copy.deepcopy(self.solutions[msgid])
        except KeyError:
            return None
        for pattern, value in kwargs.items():
            value = str(value)
            pattern = ('{%' f'{pattern}' '%}')
            with contextlib.suppress(AttributeError):
                result.title = result.title.replace(pattern, value)
            with contextlib.suppress(AttributeError):
                result.description = result.description.replace(pattern, value)
        return result

    @classmethod
    def fromlist(cls, solutions: list):
        assert isinstance(solutions, list), str(solutions)

        result = cls()
        for item in solutions:
            result.add_solution(item.msgid, item)

        return result

    @classmethod
    def fromdict(cls, solutions: dict):
        assert isinstance(solutions, dict), str(solutions)
        result = cls()
        for msgid, solution in solutions.items():
            result.add_solution(msgid, solution)
        return result


SOLUTION_PATTERN = r'^SOLUTION_(?P<type>[A-Z]{0,1})(?P<number>\d{2,5})$'


def parse_solutions(module) -> Solutions:
    if isinstance(module, str):
        module = protocol.utils.module_fromname(module)
    result = []
    for name, value in vars(module).items():
        matched = re.match(SOLUTION_PATTERN, name)
        if not matched:
            continue
        typ, number = matched['type'], int(matched['number'])  # pylint:disable=W0612
        try:
            title, message = value.split('\n\n', maxsplit=1)
        except ValueError:
            utila.error(f'{name} requires newline between headline and content')
            raise
        item = protocol.Text(title=title, msgid=number, description=message)
        result.append(item)
    return result


def parse_checkers(module) -> Validators:
    """Parse def check_{number}_{name} methods out of a module."""
    if isinstance(module, str):
        module = protocol.utils.module_fromname(module)
    result = []
    for name, value in vars(module).items():
        parsed = parse_msgid(name)
        if not parsed:
            continue
        parsed = int(parsed)
        value.msgid = parsed
        if not hasattr(value, 'confidence'):
            # enable on default
            value.confidence = 1.0
        result.append(value)
    return result


VALIDATOR_PATTERN = r'^check_(?P<number>\d{2,5})_'


def parse_msgid(name) -> int:
    """Parse the message id of a checker method.

    Expected pattern:

    .. code-block :: python

        def check_1337_this_is_an_error_checker():
            pass
    """
    matched = re.match(VALIDATOR_PATTERN, name)
    if not matched:
        return None
    result = int(matched['number'])
    return result


def confidence(value=1.0):
    """Decorator to define confidence a confidence level for a checker
    method. The default confidence of a checker is 1.0, that means it is
    enabled for the user. To pipe linting results as developer results,
    a lower confidence must be defined."""

    def decorating_function(user_function):
        user_function.confidence = value
        return user_function

    return decorating_function


SOLUTION = [
    Text(
        title='Interner Fehler: Dokument konnte nicht gelesen werden',
        description=(
            'Das Dokument konnte nicht eingelesen werden.\n\n'
            'Dieser Fehler wurde durch eine korrupte PDF-Datei verursacht oder '
            'ist durch einen technischen Fehler der `checkitweg`-Plattform '
            'entstanden.\n\n'
            'Ein Techniker arbeitet an der Loesung dieses Problems.'),
        status=ProblemStatus.CLOSED,
        msgid='F0000',
    ),
    Text(
        title='Interner Fehler: Dokument konnte verarbeitet werden',
        description=('Das Dokument konnte nicht verarbeitet werden.\n\n'
                     'Dieser Fehler ist durch einen technischen Fehler der '
                     '`checkitweg`-Plattform verursacht worden.\n\n'
                     'Ein Techniker arbeitet an der Loesung dieses Problems.'),
        status=ProblemStatus.CLOSED,
        msgid='F0001',
    ),
]

SOLUTION = {item.msgid: item for item in SOLUTION}

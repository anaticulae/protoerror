# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Solution describes a possible fix for the user to solve an error which
was told by checker.

Possible solution:
 - Hint as text block
 - Homepage

    Writen over border
    ------------------
    id:int
    msgid/problem:E0007
    title: Text element hits the autodetected border
    describtion:
    solution:open,hide,disagree,solved

    solution:
      open
      hide
      disagree
      solved

Enable printing solution list, does we need this?
"""
import contextlib
import dataclasses
import enum


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


@dataclasses.dataclass(unsafe_hash=True)  # pylint:disable=R0903
class Text(Solution):
    title: str = None
    description: str = None


@dataclasses.dataclass(unsafe_hash=True)  # pylint:disable=R0903
class Web(Text):
    hyperlink: str = None


class Solver:

    def __init__(self):
        self.solutions = {}

    def add_solution(self, msgid: str, solution: Solution):
        assert msgid, solution
        self.solutions[msgid] = solution

    def solution(self, msgid: str) -> Solution:
        with contextlib.suppress(KeyError):
            return self.solutions[msgid]
        return None

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

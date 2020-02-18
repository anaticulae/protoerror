# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""The `Linter` defines an interface to write and separate `Finding`s
which are produced due the `Checker`s.

There are 2 types of Findings. The first finding type is to deliver
information to the user. These are findings which are `active` and
`confident` enough to present them to the user as FAILUREs in there
document. The other type is to give the devloper more information to
improve the platform.

This class is thread-safe.
"""
import contextlib
import dataclasses
import importlib
import os
import threading
import typing

import utila
import yaml

import protocol.utils
from protocol.config import MessageStatus
from protocol.config import MessageStatuses
from protocol.finding import Finding
from protocol.finding import Findings
from protocol.finding import Location
from protocol.solution import Solutions
from protocol.solution import Solver
from protocol.solution import parse_checkers
from protocol.solution import parse_msgid

USER_FILE = 'user.lin'
DEVELOPER_FILE = 'developer.lin'


@dataclasses.dataclass
class DumpedLinterResult:
    user: str
    developer: str

    def __getitem__(self, index):
        """Support tuple-like access.

        Example:
            user, developer = linter_result
        """

        if index == 0:
            return self.user
        if index == 1:
            return self.developer
        raise IndexError(f'index to high {index}')


class Linter:
    """Hint: Messages are activate in default."""

    def __init__(
            self,
            solver: Solver = None,
            active: typing.List[MessageStatus] = None,
    ):
        # TODO: USE CHECKER DIRECTLY TO REDUCE AMOUT OF CODE
        self.solver = solver
        self.active = {item.msgid: item for item in active} if active else {}
        self.checkers = []
        self.findings = []
        self.lock = threading.Lock()  # make class thread safe

    def add_finding(
            self,
            location: Location = None,
            msgid: str = None,
            confidence: float = 1.0,
            **kwargs,
    ):
        """Add Finding to store linted result.

        Args:
            location: locate linting in document
            msgid: use msgid to mark this problem and find a solution.
            confidence: how confident this linting is in range
                        lowest(0.0) to highest (1.0). Lower confident
                        findings are not presented to the user to avoid
                        bad quality lintings.
            kwargs: use key words args to replace values in solution
                    template.
        """
        # Determine a possible solution
        solution = None
        if self.solver:
            solution = self.solver.solution(msgid=msgid, **kwargs)
        active = self.is_active(msgid, confidence)

        with self.lock:
            finding = Finding(
                number=len(self.findings),
                confidence=confidence,
                location=location,
                msgid=msgid,
                solution=solution,
                active=active,
            )
            self.findings.append(finding)

    def is_active(self, msgid, confidence):
        if not self.active:
            return True
        active = True
        with contextlib.suppress(KeyError):
            msgstatus = self.active[msgid]
            active = msgstatus.active and msgstatus.confidence >= confidence
        return active

    def write(self, path: str, unique: bool = False):
        """Write linter result to `user` and `developer`-file.

        Args:
            path(str): directory to write both files
            unique(bool): if unique no duplicated user-message are written
        """
        assert os.path.isdir(path), str(path)

        # create result
        result = self.result(unique=unique)
        write_result(result, path, unique=unique)

    def result(self, unique: bool = False):
        """Return current linter result of `user`, `developer`"""
        with self.lock:
            result = self.findings[:]
        if unique:
            result = utila.make_unique(result)
        return result

    def register_checker(self, checker):
        """Required method to auto register this checker."""
        self.checkers.append(checker)


def dump_result(
        items: Findings,
        *,
        unique: bool = False,
) -> DumpedLinterResult:
    """Write linter result to `user` and `developer`-file.

    Args:
        items(list): list of `Finding`s
        unique(bool): remove duplicated linter findings
    Returns:
        Result with dumped user ander developer result in yaml format.
    """
    if unique:
        items = utila.make_unique(items)

    user = [item for item in items if item.active]
    developer = [item for item in items if not item.active]

    dumped_user = yaml.dump(user)
    dumped_developer = yaml.dump(developer)

    result = DumpedLinterResult(user=dumped_user, developer=dumped_developer)
    return result


def write_result(
        result: Findings,
        path: str,
        *,
        unique: bool = False,
):
    """Write linter result to `user` and `developer`-file.

    Args:
        result(list): list of `Finding`s
        path(str): directory to write both files unique(bool): if unique
                   no duplicated user-messages are written
        unique(bool): remove duplication out of result
    """
    assert os.path.isdir(path), str(path)

    dumped_user, dumped_developer = dump_result(result, unique=unique)

    user_outpath = os.path.join(path, USER_FILE)
    utila.file_replace(user_outpath, dumped_user)

    developer_outpath = os.path.join(path, DEVELOPER_FILE)
    utila.file_replace(developer_outpath, dumped_developer)


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


def from_file(path: str) -> Linter:
    filename = os.path.basename(path)
    spec = importlib.util.spec_from_file_location(
        filename,
        os.path.join(path),
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    try:
        solution = module.SOLUTION
    except AttributeError:
        raise ValueError(f'could not create solver, no SOLUTION: {path}')
    try:
        status = module.STATUS
    except AttributeError:
        utila.debug(f'no `STATUS` provided in {path}')
        status = []
    result = from_solution(solution, status)
    return result


def from_solution(solutions: Solutions, statuses: MessageStatuses) -> Linter:
    solver = Solver.fromlist(solutions)
    result = Linter(solver, active=statuses)
    return result


def from_module(name: str) -> Linter:
    with contextlib.suppress(AttributeError):
        # support module type, ensure that module name is str
        name = name.__name__
    module = protocol.utils.module_fromname(name)
    solution = protocol.solution.parse_solutions(module)
    status = parse_active(module)
    result = protocol.from_solution(solution, status)
    return result


def parse_active(module):
    checkers = parse_checkers(module)
    result = [
        protocol.MessageStatus(
            msgid=parse_msgid(item.__name__),
            active=item.confidence > 0.0,
            confidence=item.confidence,
        ) for item in checkers
    ]
    return result


# def register(linter):
#     """required method to auto register this checker """
#     linter.register_checker(MisdesignChecker(linter))

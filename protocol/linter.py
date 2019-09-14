# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""
The `Linter` defines an interface to write and separate `Finding`s which
are produced due the `Checker`s.

There are 2 types of Findings. The first finding type is to deliver
information to the user. These are findings which are `active` and
`confident` enough to present them to the user as FAILUREs in there
document. The other type is to give the devloper more information to
improve the platform.

This class is thread-safe.
"""
import contextlib
import os
import threading
import typing

import utila
import yaml

from protocol.config import MessageStatus
from protocol.finding import Finding
from protocol.finding import Location
from protocol.solution import Solver

USER_FILE = 'user.lin'
DEVELOPER_FILE = 'developer.lin'


class Linter:

    def __init__(
            self,
            solver: Solver = None,
            active: typing.List[MessageStatus] = None,
    ):
        self.solver = solver
        self.active = {item.msgid: item for item in active} if active else None
        self.checkers = []
        self.findings = []
        self.lock = threading.Lock()  # make class thread safe

    def add_finding(
            self,
            location: Location = None,
            msgid: str = None,
            confidence: float = None,
    ):
        # Determine a possible solution
        solution = self.solver.solution(msgid) if self.solver else None
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
            return False
        active = False
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
        user, developer = self.result(unique=unique)

        dumped_user = yaml.dump(user)
        dumped_developer = yaml.dump(developer)

        user_outpath = os.path.join(path, USER_FILE)
        utila.file_replace(user_outpath, dumped_user)

        developer_outpath = os.path.join(path, DEVELOPER_FILE)
        utila.file_replace(developer_outpath, dumped_developer)

    def result(self, unique: bool = False):
        """Return current linter result of `user`, `developer`"""
        with self.lock:
            user = [item for item in self.findings if item.active]
            developer = [item for item in self.findings if not item.active]

        if unique:
            user = make_unique(user)
        return user, developer

    def register_checker(self, checker):
        """Required method to auto register this checker."""
        self.checkers.append(checker)


def make_unique(items):
    """Stable remove duplications of container `items`."""
    written = set()
    result = []
    for item in items:
        if item in written:
            continue
        written.add(item)
        result.append(item)
    return result


# def register(linter):
#     """required method to auto register this checker """
#     linter.register_checker(MisdesignChecker(linter))

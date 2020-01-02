# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""
How does the Checker work

Extracted data of different sources -> Checker[Judegement] -> Problem
                                                        with possible solution

    Base id of standard checkers (used in msg and report ids):
    01: base
    02: classes
    03: format
    04: import
    05: misc
    06: variables
    07: exceptions
    08: similar
    09: design_analysis
    10: newstyle
    11: typecheck
    12: logging
    13: string_format
    14: string_constant
    15: stdlib
    16: python3
    17: refactoring
    18-50: not yet used: reserved for future internal checkers.
    51-99: perhaps used: reserved for external checkers
"""

import typing

from protocol.finding import Findings
from protocol.finding import Location


class Checker:

    def __init__(self, linter):
        self.linter = linter

    def problems(self) -> typing.List[str]:
        """Return list of implemented problems"""

    def add_finding(
            self,
            location: Location = None,
            msgid: str = None,
            confidence: float = None,
    ):
        self.linter.add_finding(location, msgid, confidence)

    def open(self):
        pass

    def judge(self, *args) -> Findings:
        pass

    def close(self):
        pass


def check_messages(*messages: str) -> typing.Callable:
    """decorator to store messages that are handled by a checker method"""

    def store_messages(func):
        func.checks_msgs = messages
        return func

    return store_messages

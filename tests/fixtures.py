# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import pytest

import protocol
import protocol.solution


@pytest.fixture
def solver() -> protocol.Solver:
    result = protocol.Solver()
    for key, value in protocol.solution.SOLUTION.items():
        result.add_solution(key, value)
    return result


@pytest.fixture
def template_solver() -> protocol.Solver:
    result = protocol.Solver()
    result.append(
        iamraw.Text(
            number=10,
            msgid='1337',
            title='Solution {{number}} is open.',
            description='This is just a {{text}} {{double}}.',
        ))
    return result


@pytest.fixture
def linter_withlocation(solver) -> protocol.Linter:  # pylint:disable=W0621
    result = protocol.Linter(solver=solver)

    result.add_finding(
        location=iamraw.Location(page=2),
        msgid='F0001',
        confidence=1.0,
    )
    result.add_finding(
        location=iamraw.Location(page=0),
        msgid='F0000',
        confidence=0.5,
    )
    result.add_finding(
        location=iamraw.Location(page=5, shortcut='w'),
        msgid='F1337',
        confidence=0.3,
    )
    result.add_finding(
        location=iamraw.Location(page=5, shortcut='ol'),
        msgid='F1338',
        confidence=0.3,
    )
    result.add_finding(
        location=iamraw.Location(page=5, shortcut='ol'),
        msgid='1337',
        confidence=0.3,
    )
    result.add_finding(
        location=iamraw.Location(page=5, shortcut='ol'),
        msgid='1337',
        confidence=0.3,
    )
    return result

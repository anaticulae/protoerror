# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import pytest
import utila

import protocol
# pylint:disable=W0611
from tests import solver
from tests import template_solver


@pytest.fixture
def linter(solver) -> protocol.Linter:  # pylint:disable=W0621
    result = protocol.Linter(solver=solver)
    result.add_finding(location=None, msgid='F0001', confidence=1.0)
    result.add_finding(location=None, msgid='F0000', confidence=0.5)
    result.add_finding(location=None, msgid='F1337', confidence=0.3)
    return result


def test_linter_solver(linter):  # pylint:disable=W0621
    assert len(linter.findings) == 3


def test_linter_write(linter: protocol.Linter, testdir):  # pylint:disable=W0621
    root = str(testdir)
    linter.write(root)


def test_linter_write_unique(linter: protocol.Linter, testdir):  # pylint:disable=W0621
    root = str(testdir)

    before = len(linter.findings)
    # Add size check
    for _ in range(10):
        linter.add_finding(location=None, msgid='F0005', confidence=0.5)

    unique_findings = utila.make_unique(linter.findings)
    after = len(unique_findings)

    # one element was added by range
    assert after - before == 1, str(unique_findings)

    linter.write(root, unique=True)


def test_linter_linter_load_result(linter: protocol.Linter, testdir):  # pylint:disable=W0621
    root = str(testdir)
    linter.write(root, unique=True)

    user, _ = linter.result(unique=True)
    assert user  # ensure that developer contain some elements

    loaded = protocol.load_result(os.path.join(root, protocol.USER_FILE))
    assert loaded == user


def test_linter_template_solution(template_solver):  # pylint:disable=W0621
    result = protocol.Linter(solver=template_solver)
    result.add_finding(
        location=None,
        msgid='1337',
        confidence=1.0,
        number=42,
        text='Hello',
        double='half')
    output = result.result()
    expected = ([
        protocol.Finding(
            number=0,
            location=None,
            msgid='1337',
            solution=protocol.Text(
                number=10,
                msgid='1337',
                status=protocol.ProblemStatus.OPEN,
                title='Solution 42 is open.',
                description='This is just a Hello half.'),
            confidence=1.0,
            active=True)
    ], [])
    assert output == expected

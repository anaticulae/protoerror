# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest

import protocol
# pylint:disable=W0611
from tests import solver


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

    unique_findings = protocol.linter.make_unique(linter.findings)
    after = len(unique_findings)

    # one element was added by range
    assert after - before == 1, str(unique_findings)

    linter.write(root, unique=True)

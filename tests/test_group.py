# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import pytest

import protocol
from tests import solver  # pylint:disable=W0611


@pytest.fixture
def linter_withlocation(solver) -> protocol.Linter:  # pylint:disable=W0621
    result = protocol.Linter(solver=solver)

    result.add_finding(
        location=protocol.Location(page=2),
        msgid='F0001',
        confidence=1.0,
    )
    result.add_finding(
        location=protocol.Location(page=0),
        msgid='F0000',
        confidence=0.5,
    )
    result.add_finding(
        location=protocol.Location(page=5),
        msgid='F1337',
        confidence=0.3,
    )
    result.add_finding(
        location=protocol.Location(page=5),
        msgid='F1338',
        confidence=0.3,
    )
    return result


def test_group_bylocation_empty():
    assert protocol.bylocation([]) == []


def test_group_bylocation(linter_withlocation):  # pylint:disable=W0621
    user, _ = linter_withlocation.result()
    result = protocol.bylocation(user)
    assert len(result) == 3
    assert len(result[2]) == 2

    pages = [item.page for item in result]
    assert pages == [0, 2, 5], str(pages)

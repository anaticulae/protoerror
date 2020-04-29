# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest

from protocol import Checker
from protocol import Linter
from protocol import MessageStatus
from protocol import check_messages


@pytest.fixture
def active():
    result = [
        MessageStatus('F0000', True, 0.0),
        MessageStatus('F0001', True, 0.4),
    ]
    return result


@pytest.fixture
def linter(solver, active):  # pylint:disable=W0621
    result = Linter(solver=solver, active=active)
    return result


class PDFChecker(Checker):

    @check_messages('F0000')
    def check_loading_document(self, document):  # pylint:disable=W0613
        self.add_finding('F0000')

    @check_messages('F0001')
    def check_processing_document(self, document):  # pylint:disable=W0613
        self.add_finding('F0001')


def test_checker_checker(linter):  # pylint:disable=W0621
    checker = PDFChecker(linter)

    checker.check_processing_document(None)
    checker.check_loading_document(None)

    assert len(linter.findings) == 2, str(linter.findings)

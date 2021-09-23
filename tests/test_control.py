# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import iamraw
import pytest

import protocol


def test_linter_with_decorators():
    source = 'tests.example.solver_with_decorator'
    linter_ = protocol.from_module(source)
    assert linter_
    assert linter_.solver
    document = iamraw.DocInfo(
        pages=122,
        doctype=iamraw.DocumentType.DISS,
        generator=iamraw.Generator.MSWORD,
    )
    # parse checkers
    checkers = protocol.parse_checkers(source)
    checkers = protocol.filter_checkers(checkers, document)
    for checker in checkers:
        call = functools.partial(
            linter_.add_finding,
            msgid=checker.msgid,
        )
        checker(call, {})
    assert len(checkers) == 2


@pytest.mark.parametrize(
    'finding_location, expected',
    [
        pytest.param(iamraw.Location.from_page(0), 2, id='include_title'),
        pytest.param(iamraw.Location.from_page(1), 1, id='skip_title'),
    ],
)
def test_linter_section_only(finding_location, expected):
    """Skip finding depending on section decorator."""
    source = 'tests.example.solver_section_skip'

    def sections(location, only, skip):  # pylint:disable=W0613
        if iamraw.sections.TitlePage.__class__ in only:
            if location.page != 0:  # pylint:disable=C2001
                return False
        return True

    document = iamraw.DocInfo(pages=122, sections=sections)
    linters = protocol.from_module(source, document=document)
    assert linters.solver
    checkers = linters.checkerlist
    assert len(checkers) == 2
    for checker in checkers:
        call = functools.partial(
            linters.add_finding,
            msgid=checker.msgid,
            location=finding_location,
        )
        checker(call, {})
    assert len(linters.result()) == expected

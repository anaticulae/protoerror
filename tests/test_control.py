# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import protocol


def test_linter_with_decorators():
    source = 'tests.example.solver_with_decorator'
    linter_ = protocol.from_module(source)
    assert linter_
    assert linter_.solver

    document = protocol.Document(
        pages=122,
        doctype=protocol.DocType.DISS,
        generator=protocol.Generator.MSWORD,
    )

    checkers = protocol.parse_checkers(source)
    checkers = protocol.filter_checkers(checkers, document)

    for checker in checkers:
        call = functools.partial(
            linter_.add_finding,
            msgid=checker.msgid,
        )
        checker(call, {})
    assert len(checkers) == 1

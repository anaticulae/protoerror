# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools
import typing

import iamraw

import protocol

ResultType = typing.Tuple[str, str]
ResultDefault = ('user', 'developer')  # pylint:disable=C0103


def run(modulename, driver=None, location=None):
    location = location if location else iamraw.Location.from_page(0)
    # create linter
    checkers = protocol.parse_checkers(modulename)
    linter = protocol.from_module(modulename)
    # run linter
    result = linting(linter, checkers, driver, location)
    # dump results
    user, developer = protocol.dump_result(result)
    return user, developer


def linting(
        linter: protocol.Linter,
        checkers: 'protocol.Validators',
        driver,
        location: iamraw.Location,
):
    for checker in checkers:
        call = functools.partial(
            linter.add_finding,
            msgid=checker.msgid,
            location=location,
        )
        checker(call, driver)
    result = linter.result(unique=True)
    return result

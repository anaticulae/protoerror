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


def run(modulename, driver=None, location=None, before_dump: callable = None):
    location = location if location else iamraw.Location.from_page(0)
    # create linter
    if isinstance(modulename, str):
        modulename = [modulename]
    linter = protocol.from_modules(modulename)
    # run linter
    result = linting(linter, linter.checkers, driver, location)
    if before_dump:
        # TODO: DIRTY
        # TODO: INTRODUCE UTILA CONCEPT
        try:
            result = before_dump(result=result, driver=driver, linter=linter)
        except TypeError:
            try:
                result = before_dump(result=result, driver=driver)
            except TypeError:
                result = before_dump(result=result)
    # dump results
    user, developer = protocol.dump_result(result, checkers=linter.checkers)
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

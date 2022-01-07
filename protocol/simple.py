# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools
import typing

import iamraw
import utila

import protocol

ResultType = typing.Tuple[str, str]
ResultDefault = ('user', 'developer')  # pylint:disable=C0103


def run(
    modulename,
    driver=None,
    location: iamraw.Location = None,
    document: iamraw.DocInfo = None,
    findings_merge: bool = True,
    before_dump: callable = None,
):
    location = location if location else iamraw.Location.from_page(0)
    # create linter
    if isinstance(modulename, str):
        modulename = [modulename]
    linter = protocol.from_modules(modulename, document=document)
    # run linter
    result = linting(linter, linter.checkers, driver, location)
    if findings_merge:
        result = protocol.merge_findings(result)
    if before_dump:
        result = utila.pass_required(
            before_dump,
            result=result,
            driver=driver,
            linter=linter,
        )
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

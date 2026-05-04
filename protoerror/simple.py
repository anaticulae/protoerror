# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import iamraw
import utila

import protoerror

ResultType = tuple[str, str]
ResultDefault = ('user', 'developer')  # pylint:disable=C0103


def run(
    modulename,
    driver=None,
    location: iamraw.Location = None,
    document: iamraw.DocInfo = None,
    findings_merge: bool = True,
    before_dump: callable = None,
):
    if not location:
        location = protoerror.OVERVIEW
    # create linter
    linter = protoerror.from_modules(
        modules=modulename,
        document=document,
    )
    # run linter
    result = linting(
        linter=linter,
        checkers=linter.checkers,
        driver=driver,
        location=location,
    )
    if findings_merge:
        result = protoerror.merge_findings(result)
    if before_dump:
        result = utila.pass_required(
            before_dump,
            result=result,
            driver=driver,
            linter=linter,
        )
    # dump results
    user, developer = protoerror.dump_result(
        result,
        checkers=linter.checkers,
    )
    return user, developer


def linting(
    linter: protoerror.Linter,
    checkers: 'protoerror.Validators',
    driver,
    location: iamraw.Location,
):
    failure = []
    for checker in checkers:
        utila.debug(checker.__name__)
        call = functools.partial(
            linter.add_finding,
            msgid=checker.msgid,
            location=location,
        )
        try:
            checker(call, driver)
        except Exception as error:  # pylint:disable=broad-except
            utila.error(error)
            failure.append(error)
        else:
            utila.debug('done')
    if failure:
        first_failure = failure[0]
        raise RuntimeError('linter step error') from first_failure
    result = linter.result(unique=True)
    return result

# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw

import protoerror


@protoerror.homework
@protoerror.bachelor
@protoerror.master
@protoerror.dissertation
@protoerror.book
def check_1234_many_decorator(linter, _):  # pylint:disable=W0613
    linter()


@protoerror.nolarge
@protoerror.nomedium
@protoerror.nosmall
def check_1235_more_decorators(linter, _):  # pylint:disable=W0613
    linter()


@protoerror.book
@protoerror.disable_perpage(morethan=10)
def check_1236_book_only_check(linter, _):  # pylint:disable=W0613
    linter()


@protoerror.disable_perpage(morethan=10)
def check_1237_more_than(linter, _):  # pylint:disable=W0613
    for index in range(15):
        linter(location=iamraw.Location.from_sentence(
            sentence=index,
            page=5,
        ))

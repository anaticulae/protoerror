# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protocol


@protocol.homework
@protocol.bachelor
@protocol.master
@protocol.dissertation
@protocol.diss
@protocol.book
def check_1234_many_decorator(linter, _):  # pylint:disable=W0613
    linter()


@protocol.nolarge
@protocol.nomedium
@protocol.nosmall
def check_1235_more_decorators(linter, _):  # pylint:disable=W0613
    linter()


@protocol.book
def check_1236_book_only_check(linter, _):  # pylint:disable=W0613
    linter()

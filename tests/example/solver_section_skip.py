# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw

import protocol


@protocol.section_only(iamraw.sections.TitlePage)
def check_1240_title_check(linter, _):  # pylint:disable=W0613
    linter()


def check_1241_general_check(linter, _):  # pylint:disable=W0613
    linter()

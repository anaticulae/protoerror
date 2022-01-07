# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protocol

SOLUTION_1230 = """\
Titleseite enthält keinen Prüfer

Fügen Sie die Namen und die akademischen Grade der Prüfer auf der
Titelseite hinzu.
"""

S1235 = """Short Confidence

Message.
"""


@protocol.disable_perpage(morethan=10)
@protocol.confidence(0.9)
def check_1230_author_matrikel_existence(linter, titlepage):
    if titlepage is None:
        return
    if titlepage.examiner:
        return
    linter()


def check_1235_confidence_checker():
    pass

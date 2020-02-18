# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protocol

SOLUTION_1230 = """\
Titleseite enthaelt keinen Pruefer

Fuegen Sie die Namen und die akademischen Gerade der Pruefer auf der
Titelseite hinzu.
"""


@protocol.confidence(0.9)
def check_1230_author_matrikel_existence(linter, titlepage):
    if titlepage is None:
        return
    if titlepage.examiner:
        return
    linter()


def check_1235_confidence_checker():
    pass

# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from protocol.messages import parse_msgid


def test_messages_parse_msgid():
    msgid = 'I0300'

    typ, index = parse_msgid(msgid)

    assert typ == 'I', typ
    assert index == 300, index

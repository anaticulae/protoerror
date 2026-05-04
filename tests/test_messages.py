# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest

from protoerror.messages import parse_msgid


def test_messages_parse_msgid():
    msgid = 'I0300'

    typ, number = parse_msgid(msgid)

    assert typ == 'I', typ
    assert number == 300, number


def test_messages_parse_invalid_msgid():
    msgid = 'V0300'
    with pytest.raises(AssertionError, match='invalid msg type:'):
        parse_msgid(msgid)

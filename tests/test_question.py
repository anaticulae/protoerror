# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protocol
import tests.example.question


def test_question_parser():
    parsed = protocol.parse_questions(tests.example.question)
    assert len(parsed) == 2

    assert parsed[0].msgid == 1337
    assert parsed[1].msgid == 1338

    assert parsed[0].title
    assert not parsed[0].description

    assert parsed[1].title
    assert parsed[1].description


def test_question_str():
    parsed = protocol.parse_questions(tests.example.question)
    from_str = protocol.parse_questions('tests.example.question')
    assert from_str == parsed

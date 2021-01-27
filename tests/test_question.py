# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protocol
import tests.example.solver_question


def test_question_parser():
    parsed = protocol.parse_questions(tests.example.solver_question)
    assert len(parsed) == 2

    assert parsed[0].msgid == '1337'
    assert parsed[1].msgid == '1338'

    assert parsed[0].title
    assert not parsed[0].description
    assert parsed[0].finding == 1

    assert parsed[1].title
    assert parsed[1].description
    assert parsed[1].finding == 5


def test_question_str():
    parsed = protocol.parse_questions(tests.example.solver_question)
    from_str = protocol.parse_questions('tests.example.solver_question')
    assert from_str == parsed


def test_answer(testdir, linter_withlocation):
    linter_withlocation.write(testdir.tmpdir)
    questions = protocol.parse_questions(tests.example.solver_question)

    result = protocol.answer_questions(testdir.tmpdir, questions)
    assert len(result) >= 1

    protocol.write_result(result, testdir.tmpdir, user_file='answer.yaml')

# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protocol
import protocol.report_parser
import tests.test_report


def test_parses(capsys):
    raw = tests.test_report.run_report('list', capsys)
    assert raw
    parsed = protocol.parses(raw)
    assert len(parsed.features) == 2
    assert parsed.features[0].title == 'double'
    assert parsed.features[1].title == 'single'
    assert len(parsed.features[0].solutions) == 1
    assert len(parsed.features[1].solutions) == 2


def test_parses_active(capsys):
    raw = tests.test_report.run_report('list', capsys)
    assert raw
    parsed = protocol.parses(raw, active={1240})
    assert len(parsed.features) == 1


RAW = """\
~1235:ABC~
Messages Messages Messages

~1234:Short Confidence~
        Message.

~1233:Noch mehr Nachrichten~
        Message.
"""


def test_parse_steps():
    parsed = protocol.report_parser.parse_steps(RAW)
    assert len(parsed) == 3
    assert [item.msgid for item in parsed] == [1235, 1234, 1233]

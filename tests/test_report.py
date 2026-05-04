# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import pytest
import utilotest

import protoerror


def run_report(cmd: str, capsys):
    root = os.path.join(protoerror.ROOT)
    run = protoerror.integrate(root=root, features='tests.report')[1]
    args = dict(show=cmd)
    with pytest.raises(SystemExit):
        run(args)
    stdout = utilotest.stdout(capsys)
    return stdout


def test_report_list(capsys):
    stdout = run_report('list', capsys)
    assert '~1235:' in stdout
    assert '<<single>>' in stdout


def test_report_show_solution(capsys):
    stdout = run_report('1235', capsys)
    assert 'Short Confidence' in stdout


def test_report_show_feature(capsys):
    stdout = run_report('single', capsys)
    assert 'Short Confidence' in stdout
    assert '~1235:' in stdout


def test_report_empty_cmd(capsys):
    stdout = run_report('list', capsys)
    empty = run_report('', capsys)
    assert empty == stdout
    wrong = run_report('wrong', capsys)
    assert wrong != empty

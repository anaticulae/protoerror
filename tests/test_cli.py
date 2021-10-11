# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import utila

import tests


def test_cli_optimize(dumped_findings, monkeypatch):
    optimized = dumped_findings.join('__optimized__')
    assert not os.path.exists(optimized)
    cmd = f'--optimize -i {dumped_findings} -o {dumped_findings}'
    tests.run(cmd, monkeypatch=monkeypatch)
    assert os.path.exists(optimized)
    assert len(utila.file_list(optimized)) == 3

# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import utilo

import tests


def test_cli_optimize(dumped_findings, mp):
    optimized = dumped_findings.join('__optimized__')
    assert not os.path.exists(optimized)
    cmd = f'--optimize -i {dumped_findings} -o {dumped_findings}'
    tests.run(cmd, mp=mp)
    assert os.path.exists(optimized)
    assert len(utilo.file_list(optimized)) == 3

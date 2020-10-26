# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protocol


def test_create_group(testdir, linter_withlocation):
    findings = linter_withlocation.findings
    written = protocol.write_grouped(findings, testdir.tmpdir)
    assert len(written) == 3

    loaded = protocol.load_grouped(testdir.tmpdir)
    assert len(loaded) == 3

    loaded = protocol.load_grouped(testdir.tmpdir, pages=(0, 1, 2))
    assert len(loaded) == 2

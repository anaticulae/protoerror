# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest

import protoerror


@pytest.mark.parametrize(
    'private',
    [
        True,
        False,
    ],
)
def test_create_group(private, td, linter_withlocation):
    findings = linter_withlocation.findings
    written = protoerror.write_grouped(findings, td.tmpdir, private=private)
    assert len(written) == 3

    loaded = protoerror.load_grouped(td.tmpdir)
    assert len(loaded) == 3

    loaded = protoerror.load_grouped(td.tmpdir, pages=(0, 1, 2))
    assert len(loaded) == 2

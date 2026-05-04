# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import pytest
import utila

import protoerror


def test_finding_from_path(linter_withlocation, td):
    root = td.tmpdir
    protoerror.write_result(
        linter_withlocation.result(),
        root,
        user_file='first_user.yaml',
        dev_file=None,
    )
    loaded = protoerror.findings_from_path(root)
    assert len(loaded) == 3


def test_finding_number_unique(linter_withlocation, td):
    root = td.tmpdir
    negative_default = -1
    for item in ['first_user.yaml', 'second_user.yaml', 'third_user.yaml']:
        findings = linter_withlocation.result()
        for single in findings:
            single.number = negative_default
        protoerror.write_result(
            result=findings,
            path=root,
            user_file=item,
            dev_file=None,
        )
    assert protoerror.make_finding_number_unique(root)

    loaded = protoerror.findings_from_path(root)
    assert len(loaded) == 3

    flat = utila.flat([item.content for item in loaded])
    for item in flat:
        assert item.number != negative_default, item


def test_finding_update_status(linter_withlocation, td):
    root = td.tmpdir
    result = linter_withlocation.result()
    protoerror.write_result(
        result=result,
        path=root,
        user_file='first_user.yaml',
        dev_file=None,
    )
    # position zero may change when hashing or dataclass `Finding` changes.
    number = result[0].number
    current = protoerror.finding_status(root, number)
    assert current != iamraw.ProblemStatus.SOLVED
    assert protoerror.finding_status_update(
        root,
        number,
        iamraw.ProblemStatus.SOLVED,
    )
    current = protoerror.finding_status(root, number)
    assert current == iamraw.ProblemStatus.SOLVED


def test_finding_assert_on_not_fully_replaced():
    # yapf:disable
    result = [
        iamraw.Finding(solution=iamraw.Text(description='not replaced {{noname}}')),
        iamraw.Finding(solution=iamraw.Text(description='replaced')),
        iamraw.Finding(),
    ]
    # yapf:enable
    with pytest.raises(AssertionError):
        protoerror.dump_result(result)

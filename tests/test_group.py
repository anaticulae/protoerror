# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protocol


def test_group_bypage_empty():
    assert protocol.bypage([]) == []


def test_group_bypage(linter_withlocation):
    findings = linter_withlocation.result()
    result = protocol.bypage(findings)
    assert len(result) == 3
    assert len(result[2]) == 4

    pages = [item.page for item in result]
    assert pages == [0, 2, 5], str(pages)


def test_group_filter_words(linter_withlocation):
    todo = linter_withlocation.findings
    words = protocol.words(todo)
    assert len(words) == 1


def test_group_filter_lines(linter_withlocation):
    todo = linter_withlocation.findings
    words = protocol.lines(todo)
    assert len(words) == 3


def test_group_select_page(linter_withlocation):
    findings = linter_withlocation.findings
    assert len(protocol.select_pages(findings, pages={0, 5})) == 5
    assert len(protocol.select_pages(findings, pages=2)) == 1
    assert len(protocol.select_pages(findings, pages=None)) == 6

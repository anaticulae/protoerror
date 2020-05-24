# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import contextlib

from .finding import Findings
from .finding import PageFinding
from .finding import PageFindings


def bypage(items: Findings) -> PageFindings:
    """Group `items` by location.page of `Finding`. Sort the groups
    ascending by page number."""
    pages = collections.defaultdict(list)
    for item in items:
        assert item.location, 'require location'
        pages[item.location.page].append(item)

    result = [
        PageFinding(page=page, content=pages[page])
        for page in sorted(pages.keys())
    ]
    return result


def filter_mark(items: Findings, shortcut: str) -> Findings:
    """Filter `Findings` by shortcut and sort them by `location.value`
    afterwards.

    Args:
        items(protocol.Findings): list of findings
        shortcut(str): shortcut of finding.location, w word, p page,
                       ol oneline, etc.
    Returns:
        filtered, sorted list of `Findings`
    """
    assert all([item.location for item in items]), f'require location: {items}'
    selected = []
    for item in items:
        with contextlib.suppress(AttributeError):
            if item.location.shortcut == shortcut:
                selected.append(item)
    items = sorted(selected, key=lambda x: x.location.value)
    return items


def words(items: Findings) -> Findings:
    return filter_mark(items, shortcut='w')


def lines(items: Findings) -> Findings:
    return filter_mark(items, shortcut='ol')


def sentences(items: Findings) -> Findings:
    return filter_mark(items, shortcut='s')


def select_findings(findings, msgid: int):
    return [item for item in findings if item.msgid == msgid]

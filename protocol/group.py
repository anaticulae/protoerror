# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import collections

from .finding import Findings
from .finding import PageFinding
from .finding import PageFindings


def bylocation(items: Findings) -> PageFindings:
    """Group `items` by location of `Finding`. Sort the groups ascending
    by page number."""
    pages = collections.defaultdict(list)
    for item in items:
        assert item.location, 'require location'
        pages[item.location.page].append(item)

    result = [
        PageFinding(page=page, content=pages[page])
        for page in sorted(pages.keys())
    ]
    return result


def bypage(items: Findings) -> dict:
    # TODO: use itertools.groupby()?
    collected = collections.defaultdict(list)
    for item in items:
        collected[item.location.page].append(item)

    # convert to normal dict to have KeyError's
    result = dict(collected)
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
    items = [item for item in items if item.location.shortcut == shortcut]
    items = sorted(items, key=lambda x: x.location.value)
    return items


def words(items: Findings) -> Findings:
    return filter_mark(items, shortcut='w')


def lines(items: Findings) -> Findings:
    return filter_mark(items, shortcut='ol')

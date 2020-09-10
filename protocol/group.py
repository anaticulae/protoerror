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

import iamraw
import utila

import protocol


def bypage(items: iamraw.Findings) -> iamraw.PageFindings:
    """Group `items` by location.page of `Finding`. Sort the groups
    ascending by page number."""
    pages = collections.defaultdict(list)
    for item in items:
        assert item.location is not None, f'require location {item.location}'
        pages[item.location.page].append(item)

    result = [
        iamraw.PageFinding(page=page, content=pages[page])
        for page in sorted(pages.keys())
    ]
    return result


def byid(items: iamraw.Findings) -> dict:
    """Group findings by `finding.msgid`."""
    grouped = collections.defaultdict(list)
    for item in items:
        grouped[item.msgid].append(item)
    result = dict(grouped)
    return result


def filter_mark(items: iamraw.Findings, shortcut: str) -> iamraw.Findings:
    """Filter `Findings` by shortcut and sort them by `location.value`
    afterwards.

    Args:
        items(iamraw.Findings): list of findings
        shortcut(str): shortcut of protocol.location, w word, p page,
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
    items = sorted(
        selected,
        key=lambda x: x.location.value
        if x.location.value is not None else utila.INF,
    )
    return items


def words(items: iamraw.Findings) -> iamraw.Findings:
    return filter_mark(items, shortcut='w')


def lines(items: iamraw.Findings) -> iamraw.Findings:
    return filter_mark(items, shortcut='ol')


def sentences(items: iamraw.Findings) -> iamraw.Findings:
    return filter_mark(items, shortcut='s')


def ranged(items: iamraw.Findings) -> iamraw.Findings:
    return protocol.filter_mark(items, shortcut='r')


def select_findings(
        findings: iamraw.Findings,
        msgid: set = None,
) -> iamraw.Findings:
    """Select `Findings` specified by `msgid`

    >>> select_findings([iamraw.Finding(msgid=1337), iamraw.Finding(msgid=1338)], msgid=(1337,1400))
    [Finding(...msgid=1337...)]
    >>> select_findings([iamraw.Finding(msgid=1337), iamraw.Finding(msgid=1338)])
    [Finding(...msgid=1337...), Finding(...msgid=1338...)]
    """
    assert all(isinstance(item, iamraw.Finding) for item in findings)
    if msgid is None:
        return findings
    if isinstance(msgid, int):
        msgid = {msgid}
    elif isinstance(msgid, list):
        msgid = set(msgid)
    return [item for item in findings if item.msgid in msgid]

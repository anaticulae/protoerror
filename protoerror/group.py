# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import contextlib

import iamraw
import utila

import protoerror


def bypage(items: iamraw.Findings) -> iamraw.PageFindings:
    """Group `items` by location.page of `Finding`. Sort the groups
    ascending by page number."""
    pages = collections.defaultdict(list)
    for item in items:
        assert item.location is not None, f'require location {item}'
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
    for item in items:
        if item.location:
            continue
        utila.error(f'missing location: {item}')
    items = [finding for finding in items if finding.location]
    selected = []
    for item in items:
        with contextlib.suppress(AttributeError):
            if not isinstance(value(item.location), int):
                utila.debug(f'invalid location: {item.location}, require int.')
                continue
            if item.location.shortcut == shortcut:
                selected.append(item)
    selected.sort(key=lambda x: value(x.location))
    return selected


def value(location) -> int:
    with contextlib.suppress(AttributeError):
        if location.value is not None:
            return location.value
    with contextlib.suppress(AttributeError):
        if location.line is not None:
            return location.line
    if location.page is not None:
        return location.page
    return utila.INF


def words(items: iamraw.Findings) -> iamraw.Findings:
    return filter_mark(items, shortcut='w')


def lines(items: iamraw.Findings) -> iamraw.Findings:
    return filter_mark(items, shortcut='ol')


def sentences(items: iamraw.Findings) -> iamraw.Findings:
    return filter_mark(items, shortcut='s')


def ranged(items: iamraw.Findings) -> iamraw.Findings:
    return protoerror.filter_mark(items, shortcut='r')


def select_findings(
    findings: iamraw.Findings,
    msgid: set,
) -> iamraw.Findings:
    """Select `Findings` specified by `msgid`

    >>> select_findings([iamraw.Finding(msgid=1337), iamraw.Finding(msgid=1338)], msgid=(1337,1400))
    [Finding(...msgid=1337...)]
    >>> select_findings([iamraw.Finding(msgid=1337), iamraw.Finding(msgid=1338)], msgid=1337)
    [Finding(...msgid=1337...)]
    """
    assert all(isinstance(item, iamraw.Finding) for item in findings)
    if msgid is None:
        return findings
    if isinstance(msgid, int):
        msgid = {msgid}
    elif isinstance(msgid, list):
        msgid = set(msgid)
    return [item for item in findings if item.msgid in msgid]


def count_findings(findings: iamraw.Findings, msgid: set) -> int:
    counted = len(select_findings(findings, msgid))
    return counted


def select_pages(
    findings: iamraw.Findings,
    pages: int,
) -> iamraw.Findings:
    if pages is None:
        return findings
    pages = {pages} if isinstance(pages, int) else pages
    findings = flat(findings)
    findings = [
        finding for finding in findings
        if finding.location and finding.location.page in pages
    ]
    return findings


def flat(pages: iamraw.PageFinding) -> list:
    result = []
    for page in pages:
        try:
            # PageFinding
            result.extend(page.content)
        except AttributeError:
            # findings are already flat
            result.append(page)
    return result


def select(
    findings: iamraw.Findings,
    pages: int,
    msgid: set,
) -> iamraw.Findings:
    findings = select_pages(findings, pages=pages)
    findings = select_findings(findings, msgid=msgid)
    return findings

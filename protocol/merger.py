# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import protocol


def merge_findings(findings):
    """Merge lintings which are neighbors and lint the same error.

    1. Group by page
    2. Group by message id
    3. Merge equal neighbors
    """
    ranged, notranged = utila.partition(
        key=lambda x: x.location.shortcut == 'r',
        items=findings,
    )
    result = list(notranged)
    paged = protocol.bypage(ranged)
    for page in paged:
        msgid = protocol.byid(page)
        for messagegroup in msgid.values():
            merged = merge_equal_findingid(messagegroup)
            result.extend(merged)
    return result


def merge_equal_findingid(findings):
    if not findings:
        return []
    # remove findings without lines, cause we carn't merge them
    locations, nolines = utila.partition(
        lambda x: x.location.line is not None,
        findings,
    )
    if not locations:
        # no findings with lines
        return findings
    findings = sorted(locations, key=lambda x: x.location.line)
    result = [findings[0]]
    for item in findings[1:]:
        before = result[-1]
        linebefore = before.location.line
        if before.location.line_end is not None:
            linebefore = before.location.line_end
        if item.msgid != before.msgid:
            result.append(item)
            continue
        if item.solution.description != before.solution.description:
            result.append(item)
            continue
        if item.location.line != linebefore + 1:
            result.append(item)
            continue
        before.location.line_end = linebefore + 1
    # update finding number
    for finding in result:
        finding.number = protocol.finding.hash_finding(finding)
    # append no lines
    findings.extend(nolines)
    return result

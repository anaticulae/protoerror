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

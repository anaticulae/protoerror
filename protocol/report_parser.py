# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import re
import typing

Step = collections.namedtuple('Step', 'msgid title description')
Steps = typing.List[Step]
Feature = collections.namedtuple('Feature', 'title solutions')
Report = collections.namedtuple('Report', 'name features')
Reports = typing.List[Report]

TITLE = re.compile(r'^<<(?P<title>.+)>>\n', re.MULTILINE)
HEADLINE = re.compile(r'~(?P<id>\d{2,6}):(?P<headline>.+?)~\n')


def parses(content: str, name: str = '', active: set = None) -> Report:
    splitted = TITLE.split(content)
    splitted = [item for item in splitted if item]
    features = []
    for title, area in xsome(splitted, count=2):
        solutions = parse_steps(area.strip(), active=active)
        if not solutions:
            continue
        features.append(Feature(title=title, solutions=solutions))
    result = Report(name=name, features=features)
    return result


def parse_steps(content: str, active: set = None) -> Steps:
    splitted = HEADLINE.split(content)
    splitted = [item for item in splitted if item]
    result = []
    for msgid, headline, description in xsome(splitted, count=3):
        msgid = int(msgid)
        if active and msgid not in active:
            # skip solution if solution is not selected
            continue
        description = description.strip()
        result.append(Step(msgid, headline, description))
    return result


def xsome(items, count: 1):
    # TODO: MOVE TO UTILA
    collected = []
    for item in items:
        collected.append(item)
        if len(collected) != count:
            continue
        yield collected
        collected = []

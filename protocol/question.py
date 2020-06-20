# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import dataclasses
import enum
import re
import typing

import protocol

QUESTION_PATTERN = r'^QUESTION_(?P<number>\d{2,5})$'


class Answer(enum.Enum):
    OPEN = enum.auto()
    YES = enum.auto()
    NO = enum.auto()
    UNDECIDED = enum.auto()


class Action(enum.Enum):
    PAGE = enum.auto()
    DOCU = enum.auto()


@dataclasses.dataclass(unsafe_hash=True)
class Question:
    msgid: str = None
    title: str = None
    description: str = None
    status: Answer = Answer.OPEN

    action: Action = None
    finding: int = None
    yes: callable = None
    no: callable = None


Questions = typing.List[Question]


def parse_questions(module) -> Questions:
    if isinstance(module, str):
        module = protocol.utils.module_fromname(module)
    enabler = parse_enabler(module)
    result = []
    for name, value in vars(module).items():
        matched = re.match(QUESTION_PATTERN, name)
        if not matched:
            continue
        number = int(matched['number'])
        try:
            title, message = value.split('\n\n', maxsplit=1)
        except ValueError:
            title, message = value.strip(), ''
        item = protocol.Question(
            title=title,
            msgid=number,
            description=message,
        )
        try:
            selected = enabler[number]
        except KeyError:
            pass
        else:
            item.action = selected[0]
            item.finding = selected[1]
            item.yes = selected[2]
            item.no = selected[3]  # pylint:disable=C0103

        result.append(item)
    # sort ascending
    result.sort(key=lambda x: x.msgid)
    return result


ENABLE_PATTERN = r'^QUESTION_(?P<number>\d{2,5})_ENABLE$'


def parse_enabler(module) -> int:
    result = {}
    for name, value in vars(module).items():
        matched = re.match(ENABLE_PATTERN, name)
        if not matched:
            continue
        number = int(matched['number'])
        result[number] = value
    return result


def pagemore(finding_count: int, yes: callable = None, no: callable = None):  # pylint:disable=C0103
    return (Action.PAGE, finding_count, yes, no)


def documore(finding_count: int, yes: callable = None, no: callable = None):  # pylint:disable=C0103
    return (Action.DOCU, finding_count, yes, no)

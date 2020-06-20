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


@dataclasses.dataclass(unsafe_hash=True)
class Question:
    msgid: str = None
    title: str = None
    description: str = None
    status: Answer = Answer.OPEN


Questions = typing.List[Question]


def parse_questions(module) -> Questions:
    if isinstance(module, str):
        module = protocol.utils.module_fromname(module)
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
        result.append(item)
    # sort ascending
    result.sort(key=lambda x: x.msgid)
    return result

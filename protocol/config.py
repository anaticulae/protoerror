# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""
Configuration

message:
    id: str
    active : bool
    min_confidence: float

example:


"""

import dataclasses
import typing

import utila
import yaml


@dataclasses.dataclass  # pylint:disable=R0903
class MessageStatus:
    """Configurate how and if the user see the message or it will
    support the development only.

    Example:
        MessageStatus('F0000', True, 0.0)

    The example above describe the pdf-read-error-message which is used
    if there is a problem with reading the document.
    """
    msgid: str
    # The MessageStatus is active, so it will provided to the user if occurs
    active: bool = False
    # The `confidence` of 0.0 means that the message always occurs.
    confidence: float = 1.0


def load(path: str) -> typing.List[MessageStatus]:
    content = utila.from_raw_or_path(path, ftype='yaml')
    loaded = yaml.load(content, Loader=yaml.FullLoader)
    result = []
    for item in loaded:
        msgid = item.get('msgid')
        active = item.get('active', False)
        confidence = item.get('confidence', 0.0)
        result.append(
            MessageStatus(
                msgid=msgid,
                active=active,
                confidence=confidence,
            ))
    return result


def save(messages: typing.List[MessageStatus], path: str):
    result = []
    for item in messages:
        raw = {'msgid': item.msgid}
        if item.active:
            raw['active'] = True
        if item.confidence:
            raw['confidence'] = item.confidence
        result.append(raw)
    dumped = yaml.dump(result)

    utila.file_create(path, dumped)

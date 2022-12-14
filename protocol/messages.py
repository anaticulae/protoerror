# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""The `messages` defines an interface to group problems and sort them by
weight.

MSG_TYPES description:

    Info: document statistics, wordcount, information about using style,
          document equality to famous writers.

    Convention: page order - table of content at the end of the
                document, font style, font size, font spacing.

    Refactor: writing style of paragraph with rewriting hint

    Warning: Umgangsprache, Black and Write-printing warning, to high/low
             image resolution.

    Error: Write text over page border, text formatting problem
          "Hurensohn", broken table, wrong citatation, different
          citation styles, missing reference, table of content
          order/level definition.

    Fatal: An error which blocks further analysis auf the document. In
           general this is an program error which is triggered by pdf state.

MSG definition:

    'ERROR_CODE': (
        'REASON',
        'INTERNAL_SHORTCUT',
        'DESCRIPTION_OF_THE_PROBLEM',
    ),

"""

import contextlib

import utila

MSGS = {
    'F0000': (
        'Fehler beim Lesen der PDF Datei.',
        'pdf-read-error',
        'Used when pdf-miner is not able to read pdf file.',
    ),
    'F0001': (
        'Fehler beim Extrahieren der PDF Datei.',
        'pdf-extract-error',
        'Used when environment is not able to read given pdf file.',
    ),
}

MSG_TYPES = {
    "I": "info",
    "C": "convention",  # page order
    "R": "refactor",  # style of paragraph, page
    "W": "warning",  # umgangssprache, image black and white problem
    "E": "error",  # writing over border
    "F": "fatal",  # pdf analyzing error
}

TYPE_DEFAULT = 'W'


def parse_msgid(msgid: str, idonly: bool = False) -> tuple[str, int]:
    """Split `msgid` into `type` and `number`.

    Args:
        msgid(str): define type and number of used message
        idonly(bool): do not return msg type
    Returns:
        typ(str), number(int) of message
    """
    if not msgid:
        return msgid
    with contextlib.suppress(ValueError):
        msgid = int(msgid)
        if idonly:
            return msgid
        return TYPE_DEFAULT, msgid
    typ, number = msgid[0], int(msgid[1:])
    typ = typ.upper()
    assert typ in MSG_TYPES, (f'invalid msg type: {typ}; '
                              f'use {utila.from_tuple(MSG_TYPES.keys())}')
    if idonly:
        return number
    return typ, number

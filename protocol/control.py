# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Control the checker
===================

Use decorators to exclude linter step cause the step has a problem or
implementation is not finished yet:

.. code-block:: python

    @skip
    def check_1282_skip_step():
        pass

Skip linter step for special document length:

.. code-block:: python

    @nosmall
    @nomedium
    def check_1290_long_page_check():
        pass

Supported Decorators: @nosmall, @nomedium, @nolarge

Run linter for a special document type:

.. code-block:: python

    @book
    def check_1291_page_border():
        pass

Supported Decorators: @homework, @bachelor, @master, @dissertation, @book

Examples
--------

>>> @homework
... @nolarge
... def check_1234(items):
...    pass

Get list of decorators for a linter step:

>>> decorators(check_1234)
{'nolarge', 'homework'}

Templates: Doctype based replacement
====================================

Add selective advice which are platform dependent, for example give
different advice when using MSWord instead of Latex:

.. code-block:: python

    {%MSWORD%}
    ...
    {%MSWORD_END%}

    {%LATEX%}
    ...
    {%LATEX_END%}

    {%BASE%}
    ...
    {%BASE_END%}
"""

import contextlib
import dataclasses
import enum
import re

import utila


class DocType(enum.Enum):
    HOMEWORK = enum.auto()
    BACHELOR = enum.auto()
    MASTER = enum.auto()
    DISS = enum.auto()
    BOOK = enum.auto()


class Generator(enum.Enum):
    BASE = enum.auto()
    LATEX = enum.auto()
    MSWORD = enum.auto()


@dataclasses.dataclass
class Document:
    pages: int = None
    doctype: DocType = None
    generator: Generator = None


def filter_checkers(items: list, document: Document) -> list:  # pylint:disable=R0912,R1260
    assert document.pages is not None, str(document)
    small = document.pages < 35  # TODO: HOLY VALUE
    medium = 35 <= document.pages < 220
    large = 220 <= document.pages < utila.INF

    result = []
    for item in items:
        decorated = decorators(item)
        if 'skip' in decorated:
            continue
        if 'nosmall' in decorated and small:
            continue
        if 'nomedium' in decorated and medium:
            continue
        if 'nolarge' in decorated and large:
            continue

        _home, _bachelor, _master, _diss, _book = (
            'homework' in decorated,
            'bachelor' in decorated,
            'master' in decorated,
            'dissertation' in decorated,
            'book' in decorated,
        )

        if document.doctype == DocType.HOMEWORK:
            if not _home and any((_bachelor, _master, _diss, _book)):
                continue
        if document.doctype == DocType.BACHELOR:
            if not _bachelor and any((_home, _master, _diss, _book)):
                continue
        if document.doctype == DocType.MASTER:
            if not _master and any((_home, _bachelor, _diss, book)):
                continue
        if document.doctype == DocType.DISS:
            if not _diss and any((_home, _bachelor, _master, _book)):
                continue
        if document.doctype == DocType.BOOK:
            if not _book and any((_home, _bachelor, _master, _diss)):
                continue
        result.append(item)
    return result


def decorateme(method, value):
    try:
        method.__control__.add(value)
    except AttributeError:
        setattr(method, '__control__', {value})
    return method


def decorators(method) -> set:
    assert method, str(method)
    with contextlib.suppress(AttributeError):
        return method.__control__
    return {}


# pylint:disable=C0103
homework = lambda x: decorateme(x, 'homework')
bachelor = lambda x: decorateme(x, 'bachelor')
master = lambda x: decorateme(x, 'master')
dissertation = lambda x: decorateme(x, 'dissertation')
book = lambda x: decorateme(x, 'book')

nosmall = lambda x: decorateme(x, 'nosmall')
nomedium = lambda x: decorateme(x, 'nomedium')
nolarge = lambda x: decorateme(x, 'nolarge')

skip = lambda x: decorateme(x, 'skip')


def render_template(content: str, generator: Generator) -> str:

    def start(name: str):
        return r'\{\%' + name + r'\%\}(\n){0,1}'

    def end(name: str):
        return r'\{\%' + name + r'_END\%\}(\n){0,1}'

    def remove(content, selected: str):
        pattern = start(selected)
        pattern += r'.+'
        pattern += end(selected)
        replaced = re.sub(pattern, '', content, flags=re.DOTALL)
        return replaced

    content = re.sub(start(generator.name), r'', content)
    content = re.sub(end(generator.name), '', content)

    for item in Generator:
        if item == generator:
            continue
        content = remove(content, item.name)
    return content

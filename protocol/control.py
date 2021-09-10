# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
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

Supported Decorators: @homework, @bachelor, @master, @dissertation, @diss, @book

Examples
--------

>>> @homework
... @nolarge
... def check_1234(items):
...    pass

Get list of decorators for a linter step:

>>> decorators(check_1234)
['nolarge', 'homework']

>>> @homework
... @disable_perpage(morethan=20)
... def check_touch_too_much():
...     pass

>>> decorators(check_touch_too_much)
[{'disable_perpage': {'morethan': 20}}, 'homework']

Templates: Doctype based replacement
====================================

Add selective advice which are platform dependent, for example give
different advice when using MSWord instead of Latex:

.. code-block:: python

    {% if MSWORD %}
    ...
    {% endif %}

    {% if LATEX %}
    ...
    {% endif %}

    {% if BASE %}
    ...
    {% endif %}
"""

import contextlib
import dataclasses
import enum

import configo
import utila

MAX_SMALL_PAGE_LENGTH = configo.HV_INT_PLUS(default=35).value
MAX_MEDIUM_PAGE_LENGTH = configo.HV_INT_PLUS(default=35).value


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
    small = document.pages < MAX_SMALL_PAGE_LENGTH
    medium = MAX_SMALL_PAGE_LENGTH <= document.pages < MAX_MEDIUM_PAGE_LENGTH
    large = MAX_MEDIUM_PAGE_LENGTH <= document.pages < utila.INF

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
            'diss' in decorated,
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
        assert value not in method.__control__, str(method.__control__)
        method.__control__.append(value)
    except AttributeError:
        setattr(method, '__control__', [value])
    return method


def decorators(method) -> set:
    assert method, str(method)
    with contextlib.suppress(AttributeError):
        return method.__control__
    return []


# pylint:disable=C0103
homework = lambda x: decorateme(x, 'homework')
bachelor = lambda x: decorateme(x, 'bachelor')
master = lambda x: decorateme(x, 'master')
diss = lambda x: decorateme(x, 'diss')
dissertation = diss
book = lambda x: decorateme(x, 'book')

nosmall = lambda x: decorateme(x, 'nosmall')
nomedium = lambda x: decorateme(x, 'nomedium')
nolarge = lambda x: decorateme(x, 'nolarge')

skip = lambda x: decorateme(x, 'skip')


def disable_perpage(lessthan=None, morethan=None, equal=None):
    values = {}
    if lessthan is not None:
        values['lessthan'] = lessthan
    if morethan is not None:
        values['morethan'] = morethan
    if equal is not None:
        values['equal'] = equal
    return lambda x: decorateme(x, {'disable_perpage': values})


def enable_perpage(lessthan=None, morethan=None, equal=None):
    values = {}
    if lessthan is not None:
        values['lessthan'] = lessthan
    if morethan is not None:
        values['morethan'] = morethan
    if equal is not None:
        values['equal'] = equal
    return lambda x: decorateme(x, {'enable_perpage': values})


def get_perpage(methods):
    result = []
    for method in methods:
        decorator = decorators(method)
        if 'perpage' not in str(decorator):
            continue
        result.append(method)
    return result


def is_disabled_perpage(findings, method) -> bool:
    control = method.__control__
    for item in control:
        try:
            disableperpage = item['disable_perpage']
        except (TypeError, KeyError):
            continue
        with contextlib.suppress(KeyError):
            if disableperpage['equal'] == len(findings):
                return True
        with contextlib.suppress(KeyError):
            if len(findings) <= disableperpage['lessthan']:
                return True
        with contextlib.suppress(KeyError):
            if len(findings) >= disableperpage['morethan']:
                return True
    return False

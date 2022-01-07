# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
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

import configo
import iamraw
import utila

MAX_SMALL_PAGE_LENGTH = configo.HV_INT_PLUS(default=35)
MAX_MEDIUM_PAGE_LENGTH = configo.HV_INT_PLUS(default=35)

DOCTYPES = [item.name.lower() for item in iamraw.DocumentType]


def filter_checkers(items: list, document: iamraw.DocInfo) -> list:
    current = document.doctype.name.lower() if document.doctype else None
    if document.pages is not None:
        small = document.pages < MAX_SMALL_PAGE_LENGTH
        medium = MAX_SMALL_PAGE_LENGTH <= document.pages < MAX_MEDIUM_PAGE_LENGTH
        large = MAX_MEDIUM_PAGE_LENGTH <= document.pages < utila.INF
    else:
        small, medium, large = False, False, False
    result = []
    for item in items:
        decorated = decorators(item)
        # deactivated method
        if 'skip' in decorated:
            continue
        # verify document length
        if small and 'nosmall' in decorated:
            continue
        if medium and 'nomedium' in decorated:
            continue
        if large and 'nolarge' in decorated:
            continue
        if current:
            # skipped document type
            if f'no{current}' in decorated:
                # nohome nobachelor etc.
                continue
            # is check decorated for a special doctype
            some = any(item in decorated for item in DOCTYPES)
            if some and current not in decorated:
                # current document is not selected by decorators, but
                # others are. Therefore we have to skip this ckeck,
                # because this check was not made for current document
                # type.
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
paper = lambda x: decorateme(x, 'paper')
# exluce length of document
nosmall = lambda x: decorateme(x, 'nosmall')
nomedium = lambda x: decorateme(x, 'nomedium')
nolarge = lambda x: decorateme(x, 'nolarge')
# exclude types of document
nohome = lambda x: decorateme(x, 'nohomework')
nobachelor = lambda x: decorateme(x, 'nobachelor')
nomaster = lambda x: decorateme(x, 'nomaster')
nodiss = lambda x: decorateme(x, 'nodiss')
nobook = lambda x: decorateme(x, 'nobook')
nopaper = lambda x: decorateme(x, 'nopaper')

skip = lambda x: decorateme(x, 'skip')


def section_skip(sections: iamraw.PartOfDocMixin = None):
    return lambda x: decorateme(x, {'section_skip': sections})


def section_only(sections: iamraw.PartOfDocMixin = None):
    return lambda x: decorateme(x, {'section_only': sections})


def only_skip(method):
    only, skips = set(), set()
    try:
        control = method.__control__
    except AttributeError:
        return only, skips
    for item in control:
        if 'section_only' in item:
            only.add(item['section_only'])
        if 'section_skip' in item:
            skips.add(item['section_skip'])
    return only, skips


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


DOCINFO_PATTERN = utila.compiles(r"""
    ^
    (?P<typ>homework|bachelor|master|diss|habil|book|paper)?
    (?P<pages>\d{1,4})?
    (?P<lang>ger|eng|fre)?
    $
""")

DOCINFO = 'bachelor64ger'


def parse_docinfo(docinfo) -> iamraw.DocInfo:
    """\
    >>> parse_docinfo('diss215eng')
    DocInfo(pages=215, doctype=...DISS...lang=...ENGLISH...)
    >>> parse_docinfo('15GER')
    DocInfo(pages=15...NONE...lang=<Language.GERMAN...)
    >>> assert parse_docinfo(None) is None
    """
    if not docinfo:
        return None
    parsed = DOCINFO_PATTERN.match(docinfo)
    if not parsed:
        return None
    doctype = iamraw.DocumentType.NONE
    pages = 256
    lang = iamraw.Language.GERMAN
    with contextlib.suppress(KeyError):
        pages = int(parsed['pages'])
    with contextlib.suppress(KeyError, AttributeError):
        doctype = iamraw.DocumentType[parsed['typ'].upper()]
    with contextlib.suppress(KeyError):
        lang = parse_lang(parsed['lang'])
    result = iamraw.DocInfo(
        pages=pages,
        doctype=doctype,
        lang=lang,
    )
    return result


def parse_lang(lang: str) -> iamraw.Language:
    lang = lang.lower()
    if lang == 'ger':
        return iamraw.Language.GERMAN
    if lang == 'eng':
        return iamraw.Language.ENGLISH
    if lang == 'fre':
        return iamraw.Language.FRENCH
    return iamraw.Language.UNKNOWN


def integrate_docinfo():
    hook = integrate_cli
    run = evaluate_userchoice
    return hook, run


def evaluate_userchoice(argv):
    docinfo = argv.get('docinfo', None)
    parsed = parse_docinfo(docinfo)
    if parsed is None:
        parsed = iamraw.DocInfo()
    return dict(docinfo=parsed)


def integrate_cli(parser):
    parser.add_argument(
        '--docinfo',
        help='define docinfo to tell document type, length and language',
    )

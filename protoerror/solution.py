# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Solution
========

Solution describes a possible fix for the user to solve an error
which was told by checker.

Possible solution:
 * Hint as text block
 * Homepage
 * Link to internal documentation

.. code-block :: none

    Writen over border
    ------------------
    id:int
    msgid/problem:E0007
    title: Text element hits the autodetected border
    description:
    solution:open,hide,disagree,solved

    solution:
      open
      hide
      disagree
      solved

Pattern
-------

Define a solution message in short pattern:

.. code-block:: python

    S2000=\"""
    TITLE

    MESSAGE\"""

Define a solution message:

.. code-block:: python

    SOLUTION_2000=\"""
    TITLE

    MESSAGE\"""

.. todo:: Enable printing solution list, do we need this?
"""

import copy
import re

import iamraw
import jinja2
import utilo

import protoerror
import protoerror.messages
import protoerror.utils

Validators = list[callable]


class Solver:

    def __init__(self):
        self.solutions = {}

    def add_solution(self, msgid: str, solution: iamraw.Solution):
        assert msgid, solution
        msgid = protoerror.messages.parse_msgid(msgid, idonly=True)
        self.solutions[msgid] = solution

    def append(self, item: iamraw.Solution):
        msgid = protoerror.messages.parse_msgid(item.msgid, idonly=True)
        self.solutions[msgid] = item

    def solution(self, msgid: str, **kwargs) -> iamraw.Solution:
        msgid = protoerror.messages.parse_msgid(msgid, idonly=True)
        try:
            result = copy.deepcopy(self.solutions[msgid])
        except KeyError:
            return None
        result.title = render_template(result.title, **kwargs)
        result.description = render_template(result.description, **kwargs)
        return result

    @classmethod
    def fromlist(cls, solutions: list):
        assert isinstance(solutions, list), str(solutions)
        result = cls()
        for item in solutions:
            result.add_solution(item.msgid, item)
        return result

    @classmethod
    def fromdict(cls, solutions: dict):
        assert isinstance(solutions, dict), str(solutions)
        result = cls()
        for msgid, solution in solutions.items():
            result.add_solution(msgid, solution)
        return result


def render_template(raw: str, **kwargs) -> str:
    template = jinja2.Template(
        raw,
        lstrip_blocks=True,
        trim_blocks=True,
        keep_trailing_newline=False,
    )
    kwargs = {
        key: escape(value) if isinstance(value, str) else value
        for key, value in kwargs.items()
    }
    rendered = template.render(**kwargs)
    # strip final line
    rendered = rendered.strip()
    return rendered


SOLUTION_PATTERN = r'^SOLUTION_(?P<type>[A-Z]{0,1})(?P<number>\d{2,5})$'
SOLUTION_PATTERN_SIMPLE = r'^S(?P<type>[A-Z]){0,1}(?P<number>\d{2,5})$'


def parse_solutions(  # pylint:disable=R1260
    module,
    tests: set = None,
    skips: set = None,
) -> iamraw.Solutions:
    if isinstance(module, str):
        module = protoerror.utils.module_fromname(module)
    result = []
    for name, value in vars(module).items():
        # try different pattern to find solution, presented to the user
        for pattern in (SOLUTION_PATTERN_SIMPLE, SOLUTION_PATTERN):
            matched = re.match(pattern, name)
            if matched:
                break
        if not matched:
            continue
        # extract solution id
        number = int(matched['number'])
        if should_skip(number, tests, skips):
            continue
        try:
            typ = matched['type'] or protoerror.TYPE_DEFAULT
        except IndexError:
            # TODO: ADD DEFAULT LEVEL TO IAMRAW?
            typ = protoerror.TYPE_DEFAULT
        try:
            title, message = value.split('\n\n', maxsplit=1)
        except ValueError:
            utilo.error(f'{name} requires newline between headline and content')
            raise
        label = f'{typ}{number}'
        item = iamraw.Text(title=title, msgid=label, description=message)
        result.append(item)
    return result


def should_skip(number: int, tests: set = None, skips: set = None) -> bool:
    """\
    >>> should_skip(5, tests={1,2,3,4,5})
    select: 5
    False
    >>> should_skip(5, skips={1,2,3,4,5})
    skips: 5
    True
    >>> should_skip(5, tests={1,2,})
    True
    """
    tests = tests if tests is not None else {}
    skips = skips if skips is not None else {}
    if number in skips:
        utilo.log(f'skips: {number}')
        return True
    if tests:
        if number not in tests:
            return True
        utilo.log(f'select: {number}')
    return False


def parse_checkers(module, tests: set = None, skips: set = None) -> Validators:
    """Parse def check_{number}_{name} methods out of a module."""
    if isinstance(module, str):
        module = protoerror.utils.module_fromname(module)
    result = []
    for name, value in vars(module).items():
        parsed = parse_msgid(name)
        if not parsed:
            continue
        parsed = int(parsed)
        if should_skip(parsed, tests=tests, skips=skips):
            continue
        value.msgid = parsed
        if not hasattr(value, 'confidence'):
            # enable on default
            value.confidence = 1.0
        result.append(value)
    return result


VALIDATOR_PATTERN = r'^check_(?P<type>[a-zA-Z]{0,1})(?P<number>\d{2,5})_'


def parse_msgid(name) -> int:
    """Parse the message id of a checker method.

    Expected pattern:

    .. code-block :: python

        def check_1337_this_is_an_error_checker():
            pass
    """
    matched = re.match(VALIDATOR_PATTERN, name)
    if not matched:
        return None
    result = int(matched['number'])
    return result


def confidence(value=1.0):
    """Decorator to define confidence a confidence level for a checker
    method. The default confidence of a checker is 1.0, that means it is
    enabled for the user. To pipe linting results as developer results,
    a lower confidence must be defined."""

    def decorating_function(user_function):
        user_function.confidence = value
        return user_function

    return decorating_function


# Pay attention to the order to avoid internal replacements of html chars.
REPLACE = r'#*${}<>:=[]?!()@%/'


def escape(text: str) -> str:
    """Convert chars to html code to avoid processing problems in
    Markdown-Replacement.

    >>> escape('*')
    '&#42;'
    >>> escape('*#$')
    '&#42;&#35;&#36;'

    Ensure that all characters are replaced
    >>> assert escape(REPLACE).count('#') == len(REPLACE)
    >>> escape('{{hn:4:nh}}')
    '<sup>4</sup>'
    """
    # TODO: REMOVE LATER
    text = re.sub(r'\{\{hn\:(\d{1,3})\:nh\}\}', r'<sup>\1</sup>', text)
    for char in REPLACE:
        text = text.replace(char, f'&#{ord(char)};')
    # allow basic html styling
    for char in 'i u b del sup'.split():
        text = text.replace(f'&#60;{char}&#62;', f'<{char}>')
        text = text.replace(f'&#60;&#47;{char}&#62;', f'</{char}>')
    return text


SOLUTION = [
    iamraw.Text(
        title='Interner Fehler: Dokument konnte nicht gelesen werden',
        description=(
            'Das Dokument konnte nicht eingelesen werden.\n\n'
            'Dieser Fehler wurde durch eine korrupte PDF-Datei verursacht oder '
            'ist durch einen technischen Fehler der `checkitweg`-Plattform '
            'entstanden.\n\n'
            'Ein Techniker arbeitet an der Loesung dieses Problems.'),
        status=iamraw.ProblemStatus.CLOSED,
        msgid='F0000',
    ),
    iamraw.Text(
        title='Interner Fehler: Dokument konnte verarbeitet werden',
        description=('Das Dokument konnte nicht verarbeitet werden.\n\n'
                     'Dieser Fehler ist durch einen technischen Fehler der '
                     '`checkitweg`-Plattform verursacht worden.\n\n'
                     'Ein Techniker arbeitet an der Loesung dieses Problems.'),
        status=iamraw.ProblemStatus.CLOSED,
        msgid='F0001',
    ),
]

SOLUTION = {item.msgid: item for item in SOLUTION}

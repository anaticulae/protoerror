# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Report Solution
===============

example
-------

.. code-block::none

    <<titlepage>>
    ~7777:headline~
    ...
    ...
    ...
    ~7779:next headline~
    ...
    ...
    ...
    <<bibliography>>

cli
---

decider show list [--short]
        show titlepage
        show 7777

"""

import functools
import importlib
import os
import sys
import textwrap

import utila

import protocol


def integrate(root: str, features: str):
    hook = integrate_cli
    run_ = functools.partial(run, root=root, features=features)
    return hook, run_


def show_list(root, features, short: bool = False):
    print_features(root, features, choice=None, short=short)


def show_feature(root, features, choice, short: bool = False):
    print_features(root, features, choice, short)


def show_solution(root, features, choice, short: bool = False):
    parsed = parse_features(root, features)
    if not parsed:
        return
    parsed = [(checkers, solutions) for (_, (checkers, solutions)) in parsed]
    for checkers, solutions in parsed:
        for check in sorted(checkers):
            if check != choice:
                continue
            print_solution(check, solutions, short=short, single=True)
            return
    utila.error(f'could not find solution: {choice}')


def print_features(root, features, choice, short: bool = False):
    parsed = parse_features(root, features)
    if not parsed:
        return
    hit = False
    for title, (checkers, solutions) in parsed:
        if choice and title != choice:
            continue
        hit = True
        utila.log(f'<<{title}>>')
        for check in sorted(checkers):
            print_solution(check, solutions, short=short)
        utila.log()
    if not hit:
        utila.error(f'could not find feature: {choice}')
        sys.exit(utila.FAILURE)


def print_solution(
    check,
    solutions,
    *,
    short: bool = False,
    single: bool = False,
):
    indent = '\t' if short and not single else ''
    try:
        title, description = solutions[check]
    except KeyError:
        utila.log(f'{indent}~{check}:NO_SOLUTION~')
        return
    if single:
        utila.log(title)
    else:
        utila.log(f'{indent}~{check}:{title}~')
    if single:
        utila.log()
    if not short:
        prefix = '\t' if not single else ''
        utila.log(textwrap.indent(description.strip(), prefix))
        utila.log()


def run(args, root, features):
    if 'show' not in args:
        return
    assert os.path.exists(root), str(root)
    choice = args['show']
    short = args.get('short', False)
    if 'list' in choice:
        show_list(root, features, short=short)
    elif utila.isnumber(choice):
        choice = int(choice)
        show_solution(root, features, choice, short=short)
    else:
        show_feature(root, features, choice)
    sys.exit(utila.SUCCESS)


def integrate_cli(parser):
    sub = parser.add_subparsers(help='show additional linter information')
    show = sub.add_parser('show')
    show.add_argument('show', nargs='?', default='list')
    show.add_argument('--short', action='store_true', help='display fewer content') # yapf:disable


def parse_features(root: str, features: str):
    if isinstance(features, str):
        features = [features]
    collected = [parse_python(root, feature) for feature in features]
    result = []
    for collect in collected:
        for (name, item) in collect:
            parsed = parse_feature(item.__name__)
            if parsed is None:
                continue
            result.append((name, parsed))
    result = sorted(result, key=lambda x: x[0])
    if not result:
        return result
    # merge duplicated groups to single group
    grouped = [result[0]]
    for name, data in result[1:]:
        before = grouped[-1]
        if name == before[0]:
            # add before
            before[1][0].extend(data[0])
            before[1][1].update(data[1])
        else:
            # new group
            grouped.append((name, data))
    return grouped


def parse_python(root: str, feature: str) -> list:
    """Load python code from path."""
    # TODO: THERE MUST BE A BETTER WAY
    collected = [
        item.replace('.py', '')
        for item in os.listdir(os.path.join(root, feature.replace('.', '/')))
        if '__init__' not in item and item.endswith('.py')
    ]
    result = []
    for item in collected:
        current = importlib.import_module(
            feature + '.' + item,
            feature,
        )
        result.append((item, current))
    return result


def parse_feature(path: str):
    # assert os.path.exists(path), str(path)
    checkers = protocol.parse_checkers(path)
    checkers = [item.msgid for item in checkers]
    solutions = protocol.parse_solutions(path)
    solutions = {
        msgid(item.msgid): (item.title, item.description) for item in solutions
    }
    if not checkers and not solutions:
        return None
    return checkers, solutions


def msgid(item: str) -> int:
    """\
    >>> msgid('W1020')
    1020
    >>> msgid('333')
    333
    """
    if item[0].isalpha():
        return int(item[1:])
    return int(item)

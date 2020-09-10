# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw

from protocol import Solver
from protocol.solution import SOLUTION


def test_solution_solver(solver: Solver):  # pylint:disable=W0621
    msgid = 'F0001'
    solution = solver.solution(msgid)
    assert solution


def test_solution_create_solver_fromlist():
    solution = [item for item in SOLUTION.values()]

    result = Solver.fromlist(solution)
    assert len(result.solutions) == len(solution), str(result.solution)


def test_solution_create_solver_fromdict():
    result = Solver.fromdict(SOLUTION)
    assert len(result.solutions) == len(SOLUTION), str(result.solution)


def test_solution_replace_template(template_solver):  # pylint:disable=W0621
    result = template_solver.solution(
        '1337',
        number=30,
        text='"template replacement"',
        double='Here comes the Newline\n\nbeep.',
    )
    expected = iamraw.Text(
        number=10,
        msgid='1337',
        status=iamraw.ProblemStatus.OPEN,
        title='Solution 30 is open.',
        description=('This is just a "template replacement" '
                     'Here comes the Newline\n\nbeep..'),
    )
    assert result == expected

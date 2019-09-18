# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from protocol import Solver
from protocol.solution import SOLUTION
# pylint:disable=W0611
from tests import solver


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

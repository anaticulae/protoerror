#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import pytest

from protocol import Text
from protocol.solution import SOLUTION
from protocol.solution import Solver


@pytest.fixture
def solver() -> Solver:
    result = Solver()
    for key, value in SOLUTION.items():
        result.add_solution(key, value)
    return result


@pytest.fixture
def template_solver() -> Solver:
    result = Solver()
    result.append(
        Text(
            number=10,
            msgid='1337',
            title='Solution {%number%} is open.',
            description='This is just a {%text%} {%double%}.',
        ))
    return result

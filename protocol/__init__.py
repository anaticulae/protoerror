#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
"""The `protocol` library supports logging errors and giving advices how to
solve this errors.

"""
import os

from .checker import Checker
from .checker import check_messages
from .config import MessageStatus
from .config import load
from .config import save
from .finding import Finding
from .finding import Findings
from .finding import Location
from .finding import PageFinding
from .finding import PageFindings
from .finding import RangedLocation
from .group import bylocation
from .linter import DEVELOPER_FILE
from .linter import USER_FILE
from .linter import Linter
from .linter import dump_result
from .linter import load_result
from .solution import Doctails
from .solution import ProblemStatus
from .solution import Solution
from .solution import Solver
from .solution import Text
from .solution import Web

__version__ = '0.5.4'

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

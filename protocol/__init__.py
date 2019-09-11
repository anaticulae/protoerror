#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
import os

from .checker import Checker
from .checker import check_messages
from .config import MessageStatus
from .config import load
from .config import save
from .finding import Finding
from .finding import Location
from .linter import Linter
from .solution import ProblemStatus
from .solution import Solution
from .solution import Solver
from .solution import Text
from .solution import Web

__version__ = '0.1.1'

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

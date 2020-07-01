#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
"""Protocol
========

The `protocol` library supports logging errors and giving advices how
to solve this errors.
"""

import os

# checker
from protocol.checker import Checker
from protocol.checker import check_messages
# config
from protocol.config import MessageStatus
from protocol.config import load
from protocol.config import save
# finding
from protocol.finding import SUMMARY_LOCATION
from protocol.finding import BoundingLocation
from protocol.finding import Finding
from protocol.finding import FindingLevel
from protocol.finding import Findings
from protocol.finding import Location
from protocol.finding import PageFinding
from protocol.finding import PageFindings
from protocol.finding import RangedLocation
from protocol.finding import finding_status
from protocol.finding import finding_status_update
from protocol.finding import findings_from_path
from protocol.finding import load_result
from protocol.finding import make_finding_number_unique
# group
from protocol.group import byid
from protocol.group import bypage
from protocol.group import filter_mark
from protocol.group import lines
from protocol.group import select_findings
from protocol.group import sentences
from protocol.group import words
# linter
from protocol.linter import DEVELOPER_FILE
from protocol.linter import USER_FILE
from protocol.linter import DumpedLinterResult
from protocol.linter import Linter
from protocol.linter import dump_result
from protocol.linter import from_file
from protocol.linter import from_module
from protocol.linter import from_solution
from protocol.linter import write_result
# question
from protocol.question import Answer
from protocol.question import Question
from protocol.question import Questions
from protocol.question import answer_questions
from protocol.question import documore
from protocol.question import pagemore
from protocol.question import parse_questions
# solution
from protocol.solution import Doctails
from protocol.solution import ProblemStatus
from protocol.solution import Solution
from protocol.solution import Solutions
from protocol.solution import Solver
from protocol.solution import Text
from protocol.solution import Validators
from protocol.solution import Web
from protocol.solution import confidence
from protocol.solution import parse_checkers
from protocol.solution import parse_msgid
from protocol.solution import parse_solutions
# utils
from protocol.utils import driver

__version__ = '1.0.3'

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

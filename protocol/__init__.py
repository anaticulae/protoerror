#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
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

import iamraw

import protocol.__patch__
# checker
from protocol.checker import Checker
from protocol.checker import check_messages
# config
from protocol.config import MessageStatus
from protocol.config import load
from protocol.config import save
# control
from protocol.control import bachelor
from protocol.control import book
from protocol.control import decorators
from protocol.control import disable_perpage
from protocol.control import diss
from protocol.control import dissertation
from protocol.control import enable_perpage
from protocol.control import filter_checkers
from protocol.control import homework
from protocol.control import is_disabled_perpage
from protocol.control import master
from protocol.control import nobachelor
from protocol.control import nobook
from protocol.control import nodiss
from protocol.control import nohome
from protocol.control import nolarge
from protocol.control import nomaster
from protocol.control import nomedium
from protocol.control import nopaper
from protocol.control import nosmall
from protocol.control import section_only
from protocol.control import section_skip
# finding
from protocol.finding import finding_status
from protocol.finding import finding_status_update
from protocol.finding import findings_from_path
from protocol.finding import hash_finding
from protocol.finding import make_finding_number_unique
# group
from protocol.group import byid
from protocol.group import bypage
from protocol.group import count_findings
from protocol.group import filter_mark
from protocol.group import flat
from protocol.group import lines
from protocol.group import ranged
from protocol.group import select
from protocol.group import select_findings
from protocol.group import select_pages
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
from protocol.linter import from_modules
from protocol.linter import from_solution
from protocol.linter import skip_check
from protocol.linter import write_result
# merge
from protocol.merger import merge_findings
# messages
from protocol.messages import TYPE_DEFAULT
# paged
from protocol.paged import load_grouped
from protocol.paged import write_grouped
# question
from protocol.question import Answer
from protocol.question import Question
from protocol.question import Questions
from protocol.question import answer_questions
from protocol.question import documore
from protocol.question import pagemore
from protocol.question import parse_questions
# report
from protocol.report import integrate
# report parser
from protocol.report_parser import Feature
from protocol.report_parser import Report
from protocol.report_parser import Reports
from protocol.report_parser import Step
from protocol.report_parser import Steps
from protocol.report_parser import parses
# run
from protocol.simple import ResultDefault
from protocol.simple import ResultType
from protocol.simple import run
# solution
from protocol.solution import Solver
from protocol.solution import Validators
from protocol.solution import confidence
from protocol.solution import parse_checkers
from protocol.solution import parse_msgid
from protocol.solution import parse_solutions
# utils
from protocol.utils import RESULT_EMPTY
from protocol.utils import driver

__version__ = '3.12.3'

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

OVERVIEW = iamraw.Location.from_page(-1)

#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
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

import protoerror.__patch__
# checker
from protoerror.checker import Checker
from protoerror.checker import check_messages
# config
from protoerror.config import MessageStatus
from protoerror.config import load
from protoerror.config import save
# control
from protoerror.control import DOCINFO
from protoerror.control import bachelor
from protoerror.control import book
from protoerror.control import decorators
from protoerror.control import disable_perpage
from protoerror.control import diss
from protoerror.control import dissertation
from protoerror.control import enable_perpage
from protoerror.control import english
from protoerror.control import filter_checkers
from protoerror.control import german
from protoerror.control import homework
from protoerror.control import integrate_docinfo
from protoerror.control import is_disabled_perpage
from protoerror.control import master
from protoerror.control import nobachelor
from protoerror.control import nobook
from protoerror.control import nodiss
from protoerror.control import nohome
from protoerror.control import nolarge
from protoerror.control import nomaster
from protoerror.control import nomedium
from protoerror.control import nopaper
from protoerror.control import nosmall
from protoerror.control import parse_docinfo
from protoerror.control import section_only
from protoerror.control import section_skip
# finding
from protoerror.finding import finding_status
from protoerror.finding import finding_status_update
from protoerror.finding import findings_from_path
from protoerror.finding import hash_finding
from protoerror.finding import make_finding_number_unique
# group
from protoerror.group import byid
from protoerror.group import bypage
from protoerror.group import count_findings
from protoerror.group import filter_mark
from protoerror.group import flat
from protoerror.group import lines
from protoerror.group import ranged
from protoerror.group import select
from protoerror.group import select_findings
from protoerror.group import select_pages
from protoerror.group import sentences
from protoerror.group import words
# linter
from protoerror.linter import DEVELOPER_FILE
from protoerror.linter import USER_FILE
from protoerror.linter import DumpedLinterResult
from protoerror.linter import Linter
from protoerror.linter import dump_result
from protoerror.linter import from_file
from protoerror.linter import from_module
from protoerror.linter import from_modules
from protoerror.linter import from_solution
from protoerror.linter import write_result
# merge
from protoerror.merger import merge_findings
# messages
from protoerror.messages import TYPE_DEFAULT
# paged
from protoerror.paged import load_grouped
from protoerror.paged import write_grouped
# question
from protoerror.question import Answer
from protoerror.question import Question
from protoerror.question import Questions
from protoerror.question import answer_questions
from protoerror.question import documore
from protoerror.question import pagemore
from protoerror.question import parse_questions
# report
from protoerror.report import integrate
# report parser
from protoerror.report_parser import Feature
from protoerror.report_parser import Report
from protoerror.report_parser import Reports
from protoerror.report_parser import Step
from protoerror.report_parser import Steps
from protoerror.report_parser import parses
# run
from protoerror.simple import ResultDefault
from protoerror.simple import ResultType
from protoerror.simple import run
# solution
from protoerror.solution import Solver
from protoerror.solution import Validators
from protoerror.solution import confidence
from protoerror.solution import parse_checkers
from protoerror.solution import parse_msgid
from protoerror.solution import parse_solutions
# utils
from protoerror.utils import RESULT_EMPTY
from protoerror.utils import driver
from protoerror.utils import skip_method

__version__ = '3.20.1'

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

OVERVIEW = iamraw.Location.from_page(-1)

skip_check = skip_method
skip = skip_method

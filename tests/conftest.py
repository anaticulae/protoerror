# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

# pylint:disable=W0611
from tests.fixtures import dumped_findings
from tests.fixtures import linter_withlocation
from tests.fixtures import solver
from tests.fixtures import template_solver

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

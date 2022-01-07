# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""This is an example to create a linter with solver from source code via:

.. code-block :: python

    linter = protocol.from_file(__file__)
"""

import protocol  # pylint:disable=W0611

SOLUTION = []
STATUS = []

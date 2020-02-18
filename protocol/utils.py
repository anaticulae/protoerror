# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import importlib


def driver(**kwargs):
    # TODO: THERE MUST BE A BETTER WAY. PYTHONIC WAY.
    Driver = collections.namedtuple('Driver', kwargs.keys())
    result = Driver(**kwargs)
    return result


def module_fromname(name: str):
    module = importlib.import_module(name)
    return module

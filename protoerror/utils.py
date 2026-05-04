# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import importlib
import inspect

import utilo

RESULT_EMPTY = '[]', '[]'


def driver(**kwargs):
    """\
    >>> driver(name='Helmut', age=33)
    Driver(name='Helmut', age=33)
    """
    driverx = collections.namedtuple('Driver', kwargs.keys())
    result = driverx(**kwargs)
    return result


def module_fromname(name: str):
    module = importlib.import_module(name)
    return module


def skip_method(msg: str = '', methodstart='check_'):
    """\
    >>> def magic_spell():
    ...     skip_method('No enough mana.', methodstart='magic')
    >>> import utilo
    >>> with utilo.level_tmp(utilo.Level.DEBUG):
    ...     magic_spell()
          No enough mana.
          skip: magic_spell
    """
    frame = inspect.currentframe()
    caller = [item.function for item in inspect.getouterframes(frame)[0:5]]
    caller = [item for item in caller if methodstart in item]
    caller = ' '.join(caller)
    utilo.debug(msg)
    utilo.debug(f'skip: {caller}')

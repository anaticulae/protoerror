# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import glob
import os

import utila


def file_list(
        path: str,
        include: list = None,
        exclude: list = None,
        recursive: bool = True,
        absolute: bool = False,
) -> list:
    """Scans `path` recursively and returns list of relative file path
    which matches `include` or `exclude` pattern.

    Args:
        path(str): root path to scan files
        include(list): list of patterns to include
        exclude(list): list of patterns to exclude
        recursive(bool): visit child folder
        absolute(bool): if True add `path` to extracted files
    Returns:
        List of selected files.
    """
    assert os.path.exists(path), path
    msg = f'only one pattern is allowed {include} ! {exclude}'
    assert not (include and exclude), msg

    include = include if include else []
    exclude = exclude if exclude else []
    include = [include] if isinstance(include, str) else include
    exclude = [exclude] if isinstance(exclude, str) else exclude
    # make unique and ?fast?
    include = set(include)
    exclude = set(exclude)

    result = []
    with utila.chdir(path):
        for item in glob.glob('**/*', recursive=recursive):
            if not os.path.isfile(item):
                continue
            filepath = utila.forward_slash(item)
            try:
                ext = filepath.rsplit('.', maxsplit=1)[1]
            except IndexError:
                ext = None
            if include:
                if ext not in include:
                    continue
            if exclude:
                if ext in exclude:
                    continue
            if absolute:
                filepath = os.path.join(path, item)
            result.append(filepath)
    return result


utila.file_list = file_list

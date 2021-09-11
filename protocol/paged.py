# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import concurrent.futures
import contextlib
import os

import iamraw
import serializeraw
import utila

import protocol


def write_grouped(
    findings: iamraw.Findings,
    dest: str,
    overwrite: bool = True,
    private: bool = False,
) -> list:
    result = []
    grouped = protocol.bypage(findings)
    writer = utila.file_replace if overwrite else utila.file_create
    for item in grouped:
        page = fname(item.page)
        outpath = os.path.join(dest, page)
        dumped = serializeraw.dump_findings(item.content)
        writer(outpath, dumped, private=private)
        result.append(outpath)
    return result


def load_grouped(
    source: str,
    pages: tuple = None,
    sort: bool = True,
    worker=10,
) -> iamraw.PageFindings:
    if pages is None:
        # load all findings
        pages = [
            pagenumber(item, none=True) for item in utila.file_list(source)
        ]
        # remove invalid file names
        pages = utila.not_none(pages)
    # yaml parsing is cpu bound, therefore we need a process pool instead
    # of thread pool.
    executor = utila.select_executor()
    result = []
    with executor(max_workers=worker) as executor:
        todo = {
            executor.submit(load_findings, source, page): page for page in pages
        }
        for job in concurrent.futures.as_completed(todo):
            data = job.result()
            if not data:
                continue
            result.append(data)
    if sort:
        result.sort(key=lambda x: x.page)
    return result


def load_findings(source: str, page: int) -> iamraw.PageFinding:
    name = fname(page)
    source = os.path.join(source, name)
    if not os.path.exists(source):
        return None
    findings = serializeraw.load_findings(source)
    return iamraw.PageFinding(page=page, content=findings)


def fname(page: int) -> str:
    """\
    >>> fname(-5)
    '_05'
    >>> fname(1)
    '001'
    >>> fname(333)
    '333'
    """
    if page < 0:
        return '_' + f'{page*-1}'.zfill(2)
    return f'{page}'.zfill(3)


def pagenumber(page: str, none: bool = True) -> int:
    """\
    >>> pagenumber('010')
    10
    >>> pagenumber(fname(-10))
    -10
    """
    if page[0] == '_':
        page = '-' + page[1:]
    with contextlib.suppress(ValueError):
        return int(page)
    if none:
        # handle error case
        return None
    raise ValueError(f'could not convert to int: {page}')

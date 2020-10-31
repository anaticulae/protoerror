# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
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


def write_grouped(findings: iamraw.Findings, dest: str) -> list:
    result = []
    grouped = protocol.bypage(findings)
    for item in grouped:
        page = fname(item.page)
        outpath = os.path.join(dest, page)
        dumped = serializeraw.dump_findings(item.content)
        utila.file_create(outpath, dumped)
        result.append(outpath)
    return result


def load_grouped(source: str, pages: tuple = None, worker=10) -> None:
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
    >>> fname(1)
    '001'
    >>> fname(333)
    '333'
    """
    return f'{page}'.zfill(3)


def pagenumber(page: str, none: bool = True) -> int:
    """\
    >>> pagenumber('010')
    10
    """
    with contextlib.suppress(ValueError):
        return int(page)
    if none:
        # handle error case
        return None
    raise ValueError(f'could not convert to int: {page}')

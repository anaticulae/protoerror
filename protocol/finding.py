# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import concurrent.futures
import os

import iamraw
import serializeraw
import utila

import protocol


def findings_from_path(
    path: str,
    worker: int = 10,
    useronly: bool = True,
    msgid: set = None,
) -> iamraw.PageFindings:
    """Load Findings from `path` directory and group them by page as
    `PageFindings`."""
    assert os.path.isdir(path), str(path)
    files = utila.file_list(path, include='yaml', recursive=True)
    if useronly:
        files = [
            item for item in files if utila.file_name(item).endswith('_user')
        ]
    paths = [os.path.join(path, item) for item in files]
    # limit worker by max file count
    worker = utila.mins(worker, len(files))
    # ensure to have at least one worker when collection now file
    worker = utila.maxs(1, worker)
    # yaml parsing is cpu bound, therefore we need a process pool instead
    # of thread pool.
    executor = utila.select_executor()
    with executor(max_workers=worker) as executor:
        todo = {
            executor.submit(serializeraw.load_findings, path): path
            for path in paths
        }
        findings = []
        for job in concurrent.futures.as_completed(todo):
            data = job.result()
            findings.extend(data)
    if msgid:
        # select findings by msgid
        findings = protocol.select_findings(findings, msgid=msgid)
    result = protocol.bypage(findings)
    return result


def iter_findings(path: str):
    files = utila.file_list(path, include='yaml', recursive=True)
    files = [item for item in files if utila.file_name(item).endswith('_user')]
    for item in files:
        location = os.path.join(path, item)
        findings = serializeraw.load_findings(location)
        yield location, findings


def hash_finding(item):
    try:
        return hash(item)
    except TypeError as error:
        utila.error(f'could not hash finding: {item}')
        raise error


def make_finding_number_unique(path: str, private: bool = False) -> bool:
    """Collect all findings from path and replace with unqiue finding
    number.

    Note: Remove lintings with equal hash cause there seem/must to be
          equal.

    Args:
        path(str): location where files wither user linter are located
        private(bool): encrypt result
    Returns:
        True if some file was located and replace.
        False if no user file is in `path`.
    """
    assert os.path.isdir(path), str(path)
    single = utila.Single()
    replaced = False
    for location, findings in iter_findings(path):
        for finding in findings:
            hashed = hash_finding(finding)
            if single.contains(hashed):
                utila.error(f'duplicated finding: {finding}')
                finding.number = None  # None -> do not dump this finding
                continue
            finding.number = hashed
        findings = [item for item in findings if item.number is not None]
        # TODO: REFACTOR LATER
        dumped = serializeraw.dump_findings(findings)
        utila.file_replace(location, dumped, private=private)
        replaced = True
    return replaced


def finding_status_update(
    path: str,
    number: int,
    status: iamraw.ProblemStatus,
    private: bool = False,
) -> bool:
    assert os.path.isdir(path), str(path)
    assert isinstance(number, int), type(number)
    assert isinstance(status, iamraw.ProblemStatus), type(status)
    # TODO: IMPROVE SPEED LATER? MAY USE A BUFFERED OBJECT ORIENTED APPROACH
    for location, findings in iter_findings(path):
        for finding in findings:
            if finding.number != number:
                continue
            if finding.solution is None:
                utila.error(f'could not update status: {finding}')
                return False
            finding.solution.status = status
            dumped = serializeraw.dump_findings(findings)
            utila.debug(f'number: {number}; status: {status};\n'
                        f'update: {location}')
            utila.file_replace(location, dumped, private=private)
            return True
    return False


def finding_status(path: str, number: int) -> iamraw.ProblemStatus:
    assert os.path.isdir(path), str(path)
    assert isinstance(number, int), type(number)
    for _, findings in iter_findings(path):
        for finding in findings:
            if finding.number != number:
                continue
            if finding.solution is None:
                utila.error(f'could not get status: {finding}')
                return None
            return finding.solution.status
    return None

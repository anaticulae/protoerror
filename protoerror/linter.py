# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""The `Linter` defines an interface to write and separate `Finding`s
which are produced due the `Checker`s.

There are 2 types of Findings. The first finding type is to deliver
information to the user. These are findings which are `active` and
`confident` enough to present them to the user as FAILUREs in there
document. The other type is to give the devloper more information to
improve the platform.

Note: This class is thread-safe.
"""

import collections
import contextlib
import dataclasses
import functools
import importlib
import os
import threading

import iamraw
import serializeraw
import utilo

import protoerror.config
import protoerror.control
import protoerror.finding
import protoerror.solution
import protoerror.utils

USER_FILE = 'user_user.yaml'
DEVELOPER_FILE = 'developer_developer.yaml'


@dataclasses.dataclass
class DumpedLinterResult:
    user: str
    developer: str

    def __getitem__(self, index):
        """Support tuple-like access.

        Example:
            user, developer = linter_result
        """
        if index == 0:  # pylint:disable=C2001
            return self.user
        if index == 1:
            return self.developer
        raise IndexError(f'index to high {index}')


class Linter:
    """Hint: Messages are activate in default."""

    def __init__(
        self,
        solver: protoerror.solution.Solver = None,
        active: protoerror.config.MessageStatusList = None,
        checkers: list = None,
        document: iamraw.DocInfo = None,
    ):
        # TODO: USE CHECKER DIRECTLY TO REDUCE AMOUT OF CODE
        self.solver = solver
        self.active = {item.msgid: item for item in active} if active else {}
        self.checkerlist = list(checkers) if checkers else []
        self.only, self.skip = only_skip(self.checkerlist)
        self.findings = []
        self.document = document
        self.lock = threading.Lock()  # make class thread safe

    def add_finding(
        self,
        location: iamraw.Location = None,
        msgid: str = None,
        confidence: float = 1.0,
        **kwargs,
    ):
        """Add Finding to store linted result.

        Args:
            location: locate linting in document
            msgid: use msgid to mark this problem and find a solution.
            confidence: how confident this linting is in range
                        lowest(0.0) to highest (1.0). Lower confident
                        findings are not presented to the user to avoid
                        bad quality lintings.
            kwargs: use key words args to replace values in solution
                    template.
        """
        if self.document and self.document.sections:
            only, skip = set(), set()
            with contextlib.suppress(KeyError):
                only = self.only[msgid]
            with contextlib.suppress(KeyError):
                skip = self.skip[msgid]
            if not self.document.sections(
                    location=location,
                    only=only,
                    skip=skip,
            ):
                utilo.debug(f'skip finding in section: {msgid}, {location}')
                # do not add this finding
                return
        # Determine a possible solution
        solution = None
        if self.solver:
            if self.document == iamraw.Generator.MSWORD:
                kwargs['MSWORD'] = True
            if self.document == iamraw.Generator.LATEX:
                kwargs['LATEX'] = True
            if self.document == iamraw.Generator.UNDEFINED:
                kwargs['UNDEFINED'] = True
            solution = self.solver.solution(msgid=msgid, **kwargs)

        active = self.isactive(msgid, confidence)
        # create finding
        finding = iamraw.Finding(
            confidence=confidence,
            location=location,
            msgid=msgid,
            solution=solution,
            active=active,
        )
        finding.number = protoerror.finding.hash_finding(finding)
        # store finding
        with self.lock:
            self.findings.append(finding)

    def count_findings(self, msgid: str):
        with self.lock:
            counted = utilo.counts(self.findings, lambda x: x.msgid == msgid)
        return counted

    def check_findings(self, check: callable):
        """Run method to rewrite current `findings`."""
        with self.lock:
            self.findings = check(self.findings)

    @property
    def checkers(self):
        result = self.checkerlist
        if self.document:
            result = protoerror.filter_checkers(result, self.document)
        return result

    def isactive(self, msgid, confidence):
        if not self.active:
            return True
        active = True
        with contextlib.suppress(KeyError):
            msgstatus = self.active[msgid]
            active = msgstatus.active and msgstatus.confidence >= confidence
        return active

    def write(self, path: str, unique: bool = False):
        """Write linter result to `user` and `developer`-file.

        Args:
            path(str): directory to write both files
            unique(bool): if unique no duplicated user-message are written
        """
        assert os.path.isdir(path), str(path)
        # create result
        result = self.result(unique=unique)
        write_result(result, path, unique=unique)

    def run(self, driver=None):
        self.findings = []
        # select document dependend checkers
        for checker in self.checkers:
            call = functools.partial(
                self.add_finding,
                msgid=checker.msgid,
            )
            checker(call, driver)

    def result(self, unique: bool = False):
        """Return current linter result of `user`, `developer`"""
        with self.lock:
            result = self.findings[:]
        if unique:
            result = utilo.unique(result)
        return result

    def register_checker(self, checker):
        """Required method to auto register this checker."""
        self.checkers.append(checker)


def split_userdeveloper(items: list, checkers: list) -> tuple:
    if not checkers:
        checkers = []
    # move inactive findings to developer
    user, developer = utilo.partition(items=items, key=lambda item: item.active)
    perpage_disabled = perpage_disable(user, checkers)
    # move disabled findings to developer findings, do not show it to the
    # user.
    for item in perpage_disabled:
        user.remove(item)
        developer.append(item)
    return user, developer


def perpage_disable(findings, checkers):
    """Determine list of findings which are disabled by
    @disable-decorator."""
    findings = [item for item in findings if item.location is not None]
    grouped = protoerror.bypage(findings)
    # bypage
    result = []
    perpage = protoerror.control.get_perpage(checkers)
    for pageitem in grouped:
        paged = protoerror.byid(pageitem.content)
        for method in perpage:
            msgid = method.msgid
            try:
                findings = paged[msgid]
            except KeyError:
                continue
            if not protoerror.is_disabled_perpage(findings, method):
                # content is not disabled
                continue
            result.extend(findings)
    return result


def only_skip(checkers):
    only = collections.defaultdict(set)
    skip = collections.defaultdict(set)
    for item in checkers:
        msgid = item.msgid
        item_only, item_skip = protoerror.control.only_skip(item)
        only[msgid] |= item_only
        skip[msgid] |= item_skip
    only: dict = dict(only)
    skip: dict = dict(skip)
    return only, skip


def dump_result(
    items: iamraw.Findings,
    *,
    unique: bool = False,
    checkers: list = None,
) -> DumpedLinterResult:
    """Write linter result to `user` and `developer`-file.

    Args:
        items(list): list of `Finding`s
        unique(bool): remove duplicated linter findings
        checkers(methods): list of user linters
    Returns:
        Result with dumped user ander developer result in yaml format.
    """
    if unique:
        items = utilo.unique(items)

    user, developer = split_userdeveloper(items, checkers=checkers)

    dumped_user = serializeraw.dump_findings(user)
    dumped_developer = serializeraw.dump_findings(developer)

    result = DumpedLinterResult(user=dumped_user, developer=dumped_developer)
    return result


def write_result(
    result: iamraw.Findings,
    path: str,
    *,
    unique: bool = False,
    user_file=USER_FILE,
    dev_file=DEVELOPER_FILE,
    private: bool = False,
):
    """Write linter result to `user` and `developer`-file.

    Args:
        result(list): list of `Finding`s
        path(str): directory to write both files unique(bool): if unique
                   no duplicated user-messages are written
        unique(bool): remove duplication out of result
        user_file(str): filename of user linting file. If None, write
                        nothing
        dev_file(str): filename of developer linting file. If None,
                        write nothing
        private(bool): use encryption
    """
    assert os.path.isdir(path), str(path)
    dumped_user, dumped_developer = dump_result(result, unique=unique)
    if user_file:
        user_outpath = os.path.join(path, user_file)
        utilo.file_replace(user_outpath, dumped_user, private=private)
    if dev_file:
        developer_outpath = os.path.join(path, dev_file)
        utilo.file_replace(developer_outpath, dumped_developer, private=private)


def from_file(path: str, document: iamraw.DocInfo = None) -> Linter:
    filename = os.path.basename(path)
    spec = importlib.util.spec_from_file_location(
        filename,
        os.path.join(path),
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    try:
        solution = module.SOLUTION
    except AttributeError as error:
        msg = f'could not create solver, no SOLUTION: {path}'
        raise ValueError(msg) from error
    try:
        status = module.STATUS
    except AttributeError:
        utilo.debug(f'no `STATUS` provided in {path}')
        status = []
    result = from_solution(
        solution,
        status,
        document=document,
    )
    return result


def from_solution(
    solutions: iamraw.Solutions,
    statuses: protoerror.config.MessageStatusList,
    checkers: list = None,
    document: iamraw.DocInfo = None,
) -> Linter:
    solver = protoerror.solution.Solver.fromlist(solutions)
    result = Linter(
        solver,
        active=statuses,
        checkers=checkers,
        document=document,
    )
    return result


def from_module(
    name: str,
    tests: set = None,
    skips: set = None,
    document: iamraw.DocInfo = None,
) -> Linter:
    result = from_modules(
        [name],
        tests=tests,
        skips=skips,
        document=document,
    )
    return result


def from_modules(
    modules: utilo.Strings,
    tests: set = None,
    skips: set = None,
    document: iamraw.DocInfo = None,
) -> Linter:
    modules = module_list(modules)
    status = []
    checkers = []
    solutions = []
    for name in modules:
        with contextlib.suppress(AttributeError):
            # support module type, ensure that module name is str
            name = name.__name__
        module = protoerror.utils.module_fromname(name)
        solutions.extend(
            protoerror.solution.parse_solutions(
                module,
                tests=tests,
                skips=skips,
            ))
        status.extend(parse_active(module))
        checkers.extend(
            protoerror.parse_checkers(
                module,
                tests=tests,
                skips=skips,
            ))
    result = protoerror.from_solution(
        solutions,
        status,
        checkers=checkers,
        document=document,
    )
    return result


def module_list(modulename: list) -> list:
    r"""\
    >>> import protocol.simple; protocol.simple.run(protocol.simple)
    ('[]\n', '[]\n')
    """
    if isinstance(modulename, str):
        return [modulename]
    if type(modulename).__name__ == 'module':
        return [modulename]
    return modulename


def parse_active(module):
    checkers = protoerror.solution.parse_checkers(module)
    result = [
        protoerror.MessageStatus(
            msgid=protoerror.solution.parse_msgid(item.__name__),
            active=item.confidence > 0.0,
            confidence=item.confidence,
        ) for item in checkers
    ]
    return result


# def register(linter):
#     """required method to auto register this checker """
#     linter.register_checker(MisdesignChecker(linter))

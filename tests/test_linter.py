# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import iamraw
import pytest
import serializeraw
import utila

import protocol
import tests.example.solver_with_error


@pytest.fixture
def linter(solver) -> protocol.Linter:  # pylint:disable=W0621
    result = protocol.Linter(solver=solver)
    result.add_finding(location=None, msgid='F0001', confidence=1.0)
    result.add_finding(location=None, msgid='F0000', confidence=0.5)
    result.add_finding(location=None, msgid='F1337', confidence=0.3)
    return result


def test_linter_solver(linter):  # pylint:disable=W0621
    assert len(linter.findings) == 3


def test_linter_write(linter: protocol.Linter, td):  # pylint:disable=W0621
    root = str(td)
    linter.write(root)


def test_linter_write_unique(linter: protocol.Linter, td):  # pylint:disable=W0621
    root = str(td)

    before = len(linter.findings)
    # Add size check
    for _ in range(10):
        linter.add_finding(location=None, msgid='F0005', confidence=0.5)

    unique_findings = utila.unique(linter.findings)
    after = len(unique_findings)

    # one element was added by range
    assert after - before == 1, str(unique_findings)

    linter.write(root, unique=True)


def test_linter_linter_load_result(linter: protocol.Linter, td):  # pylint:disable=W0621
    root = str(td)
    linter.write(root, unique=True)

    user = linter.result(unique=True)
    assert user  # ensure that developer contain some elements

    loaded = serializeraw.load_findings(os.path.join(root, protocol.USER_FILE))
    assert loaded == user


def test_linter_template_solution(template_solver):  # pylint:disable=W0621
    result = protocol.Linter(solver=template_solver)
    result.add_finding(
        location=None,
        msgid='E1337',
        confidence=1.0,
        number=42,
        text='Hello',
        double='half',
    )
    output = result.result()
    expected = [
        iamraw.Finding(
            number=0,
            location=None,
            msgid='E1337',
            solution=iamraw.Text(
                number=10,
                msgid='E1337',
                status=iamraw.ProblemStatus.OPEN,
                title='Solution 42 is open.',
                description='This is just a Hello half.',
            ),
            confidence=1.0,
            active=True,
        )
    ]
    assert output == expected


def test_linter_count_findings(linter):  # pylint:disable=W0621
    assert linter.count_findings(msgid='F1337') == 1
    assert not linter.count_findings(msgid='F0005')


def test_linter_from_file():
    example = os.path.join(protocol.ROOT, 'tests/example/solver.py')
    created = protocol.from_file(example)
    assert created.solver is not None
    assert created.active is not None


def test_linter_from_file_invalid():
    with pytest.raises(ValueError):
        protocol.from_file(__file__)


def test_linter_from_file_no_status(capsys):
    example = os.path.join(protocol.ROOT, 'tests/example/solver_nostatus.py')
    with utila.level_tmp(utila.Level.DEBUG):
        created = protocol.from_file(example)
    assert created.solver is not None

    stdout = capsys.readouterr().out
    assert 'no `STATUS` provided' in stdout


def test_linter_from_module():
    linter_ = protocol.from_module('tests.example.solver_smart')
    assert linter_
    assert linter_.solver


def test_linter_from_module_with_error():
    with pytest.raises(ValueError):
        protocol.from_module(tests.example.solver_with_error)


def test_linter_with_decorators_run():
    source = 'tests.example.solver_with_decorator'
    linter_ = protocol.from_module(source)
    linter_.run(driver=None)


def test_linter_run():
    source = 'tests.example.solver_with_decorator'
    linted = protocol.run(source)
    assert isinstance(linted, tuple)
    user = linted[0]
    assert len(user) > 100
    developer = linted[1]
    count_1237 = developer.count('msgid: 1237')
    # 15 messages are deactivated and moved to developer and not shown to user
    assert count_1237 == 15

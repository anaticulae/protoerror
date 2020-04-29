# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import utila

import protocol


@pytest.mark.parametrize('location, expected', [
    ('p10', protocol.Location(page=10, shortcut='p')),
    ('w100p13', protocol.Location(page=13, shortcut='w', value=100)),
    ('sec3p5', protocol.Location(page=5, shortcut='sec', value=3)),
])
def test_finding_location_fromstr(location, expected):
    created = protocol.Location.fromstr(location)
    assert created == expected


@pytest.mark.parametrize('location', [
    protocol.Location(page=10, shortcut='p'),
    protocol.Location(page=13, shortcut='w', value=100),
    protocol.Location(page=5, shortcut='sec', value=3),
])
def test_finding_location_fromstr_raw(location):
    raw = location.raw()
    assert raw

    parsed = protocol.Location.fromstr(raw)
    assert parsed == location, str(parsed)


@pytest.mark.parametrize('raw', [
    'notworking',
    '',
])
def test_finding_location_fromstr_raw_none(raw):
    constructed = protocol.Location.fromstr(raw)
    assert constructed is None, constructed


def test_finding_hashing_location():
    location = protocol.Location.fromstr('p10')
    hashed = hash(location)
    assert hashed


def test_finding_location_from_ctor():
    page12 = protocol.Location(page=12, shortcut='p')
    page12ctor = protocol.Location.from_page(12)
    assert page12ctor == page12, str(page12ctor)

    chapter4page20 = protocol.Location(page=20, shortcut='c', value=4)
    chapter4page20ctor = protocol.Location.from_chapter(chapter=4, page=20)
    assert chapter4page20ctor == chapter4page20, str(chapter4page20ctor)

    oneline1page5 = protocol.Location(page=5, shortcut='ol', value=1)
    oneline1page5ctor = protocol.Location.from_oneline(line=1, page=5)
    assert oneline1page5ctor == oneline1page5, str(oneline1page5ctor)


@pytest.mark.parametrize('location, expected', [
    ('p10_12~l6_9~t5_19', protocol.RangedLocation(10, 12, 6, 9, 5, 19)),
    ('p10_12~l6~t5', protocol.RangedLocation(10, 12, line=6, token=5)),
    ('p10~l6', protocol.RangedLocation(page=10, line=6)),
    ('p5', protocol.RangedLocation(page=5)),
    ('p5~t17', protocol.RangedLocation(page=5, token=17)),
])
def test_finding_rangedlocation_fromstr(location, expected):
    location = protocol.RangedLocation.fromstr(location)
    assert location == expected


@pytest.mark.parametrize('location', [
    'p10_12~l6_9~t5_19',
    'p10_12~l6~t5',
    'p10~l6',
    'p5',
])
def test_finding_rangedlocation_str_obj_str(location):
    parsed = protocol.RangedLocation.fromstr(location)
    tostring = parsed.raw()
    assert tostring == location


def test_finding_from_path(linter_withlocation, testdir):
    root = testdir.tmpdir
    protocol.write_result(
        linter_withlocation.result(),
        root,
        user_file='first_user.yaml',
        dev_file=None,
    )
    loaded = protocol.findings_from_path(root)
    assert len(loaded) == 3


def test_finding_number_make_unique(linter_withlocation, testdir):
    root = testdir.tmpdir
    negative_default = -1
    for item in ['first_user.yaml', 'second_user.yaml', 'third_user.yaml']:
        findings = linter_withlocation.result()
        for single in findings:
            single.number = negative_default
        protocol.write_result(
            result=findings,
            path=root,
            user_file=item,
            dev_file=None,
        )
    protocol.make_finding_number_unique(root)

    loaded = protocol.findings_from_path(root)
    assert len(loaded) == 3

    flat = utila.flatten([item.content for item in loaded])
    for item in flat:
        assert item.number != negative_default, item

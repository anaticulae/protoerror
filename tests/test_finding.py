# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest

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
    page12ctor = protocol.Location.frompage(12)
    assert page12ctor == page12, str(page12ctor)

    chapter4page20 = protocol.Location(page=20, shortcut='c', value=4)
    chapter4page20ctor = protocol.Location.fromchapter(chapter=4, page=20)
    assert chapter4page20ctor == chapter4page20, str(chapter4page20ctor)

    oneline1page5 = protocol.Location(page=5, shortcut='ol', value=1)
    oneline1page5ctor = protocol.Location.from_oneline(line=1, page=5)
    assert oneline1page5ctor == oneline1page5, str(oneline1page5ctor)

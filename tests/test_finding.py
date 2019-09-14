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

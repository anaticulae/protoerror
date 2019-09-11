# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest

from protocol import Location


@pytest.mark.parametrize('location, expected', [
    ('p10', Location(page=10, shortcut='p')),
    ('w100p13', Location(page=13, shortcut='w', value=100)),
    ('sec3p5', Location(page=5, shortcut='sec', value=3)),
])
def test_finding_location_fromstr(location, expected):
    created = Location.fromstr(location)
    assert created == expected


@pytest.mark.parametrize('location', [
    Location(page=10, shortcut='p'),
    Location(page=13, shortcut='w', value=100),
    Location(page=5, shortcut='sec', value=3),
])
def test_finding_location_fromstr_raw(location):
    raw = location.raw()
    assert raw

    parsed = Location.fromstr(raw)
    assert parsed == location, str(parsed)


@pytest.mark.parametrize('raw', [
    'notworking',
    '',
])
def test_finding_location_fromstr_raw_none(raw):
    constructed = Location.fromstr(raw)
    assert constructed is None, constructed

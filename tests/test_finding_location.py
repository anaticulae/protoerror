# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protocol


def test_bounding_location_from_str():
    example = 'b(123.5;100.0;500.0;500.0)p5'
    parsed = protocol.BoundingLocation.fromstr(example)

    assert parsed.value == (123.5, 100.0, 500.0, 500.0), parsed.value


def test_bounding_location_dump_load():
    example = protocol.BoundingLocation.fromtuple(
        (5.0, 10.0, 50.0, 50.0),
        page=36,
    )
    dumped = str(example)
    loaded = protocol.BoundingLocation.fromstr(dumped)
    assert loaded == example

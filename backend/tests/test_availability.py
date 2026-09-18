import sys
sys.path.insert(0, "/app")

from services import AvailabilityService


def test_bogota_requires_two_rooms():

    result = AvailabilityService.search(
        city="Bogotá",
        room_type="estandar",
        check_in="2026-10-20",
        check_out="2026-10-22",
        guests=8
    )

    assert result["rooms_required"] == 2
    assert result["available"] is True


def test_invalid_dates():

    try:

        AvailabilityService.search(
            city="Bogotá",
            room_type="estandar",
            check_in="2026-10-20",
            check_out="2026-10-19",
            guests=2
        )

        assert False

    except ValueError:
        assert True

from datetime import datetime, timedelta
from decimal import Decimal

import pytest

from rental import ElectricScooter, Motorbike, RentalError, User, default_fleet


class FakeClock:
    def __init__(self):
        self.now = datetime(2025, 1, 1, 9, 0)

    def __call__(self):
        return self.now

    def advance(self, **kwargs):
        self.now += timedelta(**kwargs)


@pytest.fixture
def clock():
    return FakeClock()


@pytest.fixture
def fleet(clock):
    return default_fleet(clock)


@pytest.fixture
def evie():
    return User("U1", "Evie")


def test_renting_takes_exactly_one_vehicle_from_the_station(fleet, evie):
    before = len(fleet.available("motorbike"))

    rental = fleet.rent(evie, "motorbike", "Selly Oak")

    assert rental.vehicle.vehicle_id == "MB1"
    assert len(fleet.available("motorbike")) == before - 1
    assert evie.current_rental is rental


def test_station_names_are_matched_without_regard_to_case(fleet, evie):
    assert fleet.rent(evie, "scooter", "  selly oak ").depart_station == "Selly Oak"


def test_an_unknown_station_is_reported_rather_than_ignored(fleet, evie):
    with pytest.raises(RentalError, match="no station called 'Moseley'"):
        fleet.rent(evie, "motorbike", "Moseley")


def test_a_rented_vehicle_is_no_longer_available_to_others(fleet, evie):
    fleet.rent(evie, "scooter", "Harborne")

    with pytest.raises(RentalError, match="No scooters are available at Harborne"):
        fleet.rent(User("U2", "Nathan"), "scooter", "Harborne")


def test_a_user_can_only_hold_one_rental_at_a_time(fleet, evie):
    fleet.rent(evie, "motorbike", "Bournville")

    with pytest.raises(RentalError, match="already got a vehicle"):
        fleet.rent(evie, "scooter", "Bournville")


def test_returning_moves_the_vehicle_and_charges_by_the_minute(fleet, evie, clock):
    fleet.rent(evie, "motorbike", "Selly Oak")
    clock.advance(minutes=20)

    rental = fleet.give_back(evie, "Harborne")

    assert rental.fare() == Decimal("30.00")  # 20 min at £1.50
    assert rental.vehicle.location == "Harborne"
    assert rental.vehicle.available
    assert evie.current_rental is None


def test_the_fare_is_rounded_to_the_penny(fleet, evie, clock):
    fleet.rent(evie, "scooter", "Selly Oak")
    clock.advance(seconds=100)

    rental = fleet.give_back(evie, "Selly Oak")

    assert rental.fare() == Decimal("1.83")  # 1.667 min at £1.10 = £1.8333


def test_returning_without_a_rental_is_refused(fleet, evie):
    with pytest.raises(RentalError, match="not got a vehicle"):
        fleet.give_back(evie, "Selly Oak")


def test_a_motorbike_tank_never_overfills():
    bike = Motorbike("MB9", "Selly Oak")
    bike.refuel(50)
    bike.refuel(50)

    assert bike.fuel_level == Motorbike.TANK_LITRES


def test_a_scooter_only_recharges_when_its_battery_is_low():
    scooter = ElectricScooter("ES9", "Selly Oak")
    scooter.refuel(50)
    message = scooter.refuel(50)

    assert scooter.battery_level == 50
    assert "doesn't need charging" in message


def test_history_records_every_rental_in_order(fleet, evie):
    fleet.rent(evie, "motorbike", "Selly Oak")
    fleet.give_back(evie, "Harborne")
    fleet.rent(evie, "scooter", "Bournville")

    assert [r.vehicle.vehicle_id for r in evie.rental_history] == ["MB1", "ES2"]

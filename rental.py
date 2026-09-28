"""Vehicle rental domain: a fleet of motorbikes and e-scooters rented by the minute."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal

Clock = Callable[[], datetime]

PENNY = Decimal("0.01")


class Vehicle:
    kind = "vehicle"
    rate_per_minute = Decimal("0")

    def __init__(self, vehicle_id: str, location: str):
        self.vehicle_id = vehicle_id
        self.location = location
        self.available = True

    def rent(self) -> None:
        self.available = False

    def return_to(self, station: str) -> None:
        self.available = True
        self.location = station

    def refuel(self, amount: int) -> str:
        raise NotImplementedError


class Motorbike(Vehicle):
    kind = "motorbike"
    rate_per_minute = Decimal("1.50")
    TANK_LITRES = 80

    def __init__(self, vehicle_id: str, location: str):
        super().__init__(vehicle_id, location)
        self.fuel_level = 0

    def refuel(self, amount: int) -> str:
        self.fuel_level = min(self.TANK_LITRES, self.fuel_level + amount)
        return f"Your motorbike has been refuelled to {self.fuel_level}L."


class ElectricScooter(Vehicle):
    kind = "scooter"
    rate_per_minute = Decimal("1.10")
    LOW_BATTERY = 20

    def __init__(self, vehicle_id: str, location: str):
        super().__init__(vehicle_id, location)
        self.battery_level = 0

    def battery_low(self) -> bool:
        return self.battery_level < self.LOW_BATTERY

    def refuel(self, amount: int) -> str:
        if not self.battery_low():
            return f"Battery is at {self.battery_level}%, so your scooter doesn't need charging."
        self.battery_level = min(100, self.battery_level + amount)
        return f"Your scooter has been recharged to {self.battery_level}%."


@dataclass
class Rental:
    vehicle: Vehicle
    depart_station: str
    rent_time: datetime
    return_station: str | None = None
    return_time: datetime | None = None

    def fare(self) -> Decimal:
        """Per-minute fare, rounded to the penny. Money is Decimal so pennies never drift."""
        if self.return_time is None:
            raise ValueError("Rental has not been returned")
        minutes = Decimal(str((self.return_time - self.rent_time).total_seconds())) / 60
        return (self.vehicle.rate_per_minute * minutes).quantize(PENNY, ROUND_HALF_UP)


@dataclass
class User:
    user_id: str
    name: str
    current_rental: Rental | None = None
    rental_history: list[Rental] = field(default_factory=list)


class RentalError(Exception):
    """A rental request that can't be fulfilled; the message is shown to the user."""


class Fleet:
    def __init__(self, vehicles: list[Vehicle], clock: Clock = datetime.now):
        self.vehicles = vehicles
        self.clock = clock

    @property
    def stations(self) -> list[str]:
        return sorted({v.location for v in self.vehicles})

    def find_station(self, name: str) -> str | None:
        """Case-insensitive match, so "selly oak" finds "Selly Oak"."""
        for station in self.stations:
            if station.lower() == name.strip().lower():
                return station
        return None

    def available(self, kind: str | None = None) -> list[Vehicle]:
        return [v for v in self.vehicles if v.available and (kind is None or v.kind == kind)]

    def rent(self, user: User, kind: str, station_name: str) -> Rental:
        if user.current_rental is not None:
            raise RentalError("You've already got a vehicle on loan.")
        station = self.find_station(station_name)
        if station is None:
            raise RentalError(f"There's no station called {station_name!r}.")
        # Rent exactly one vehicle; the old loop rented every free one at the station.
        vehicle = next((v for v in self.available(kind) if v.location == station), None)
        if vehicle is None:
            raise RentalError(f"No {kind}s are available at {station}.")

        vehicle.rent()
        rental = Rental(vehicle, station, self.clock())
        user.current_rental = rental
        user.rental_history.append(rental)
        return rental

    def give_back(self, user: User, station_name: str) -> Rental:
        rental = user.current_rental
        if rental is None:
            raise RentalError("You've not got a vehicle on loan, so can't return anything.")
        station = self.find_station(station_name)
        if station is None:
            raise RentalError(f"There's no station called {station_name!r}.")

        rental.return_station = station
        rental.return_time = self.clock()
        rental.vehicle.return_to(station)
        user.current_rental = None
        return rental


def default_fleet(clock: Clock = datetime.now) -> Fleet:
    return Fleet(
        [
            Motorbike("MB1", "Selly Oak"),
            Motorbike("MB2", "Bournville"),
            Motorbike("MB3", "Harborne"),
            ElectricScooter("ES1", "Selly Oak"),
            ElectricScooter("ES2", "Bournville"),
            ElectricScooter("ES3", "Harborne"),
        ],
        clock,
    )

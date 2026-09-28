# Vehicle Rental

[![CI](https://github.com/FuaadBashi/Vehicle-Rental-App/actions/workflows/ci.yml/badge.svg)](https://github.com/FuaadBashi/Vehicle-Rental-App/actions/workflows/ci.yml)

A console rental system for a fleet of motorbikes and electric scooters spread across stations.
Users rent a vehicle, ride, return it to any station, and pay by the minute.

## Highlights

- **Domain model separate from the console.** `rental.py` holds vehicles, rentals, users and the
  fleet, with no `input()` or `print()`. `main.py` is a thin menu on top.
- **Inheritance where behaviour differs.** `Motorbike` and `ElectricScooter` share a `Vehicle`
  base but refuel differently: a fuel tank that can't overfill versus a battery that only charges
  when low.
- **Exact fares.** Money is `Decimal`, charged per minute and rounded to the penny.
- **Clear failures.** Invalid requests (unknown station, nothing available, already renting) raise
  a `RentalError` whose message the console shows as is.
- **Testable time.** The fleet takes a clock function, so tests fast-forward a rental by exactly 20
  minutes and assert the fare.

## Getting started

Requires Python 3.10+. No third-party packages are needed to run it.

```bash
git clone https://github.com/FuaadBashi/Vehicle-Rental-App.git
cd Vehicle-Rental-App
python3 main.py
```

Log in as `U1` (Evie) or `U2` (Nathan). Stations are Selly Oak, Bournville and Harborne.

| Vehicle | Rate |
| --- | --- |
| Motorbike | £1.50 / minute |
| E-scooter | £1.10 / minute |

## Tests

```bash
pip install pytest ruff
pytest
ruff format --check . && ruff check .
```

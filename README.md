# Vehicle Rental — Python Console App

A Python learning project for renting and returning motorbikes and electric scooters, tracking availability, calculating fares, and maintaining rental history during a session.

## Run locally

Use Python 3.10 or later. The application uses the standard library.

```bash
git clone https://github.com/FuaadBashi/Vehicle-Rental-App.git
cd Vehicle-Rental-App
python3 main.py
```

## Code to explore

[main.py](main.py) brings together the base `Vehicle` type, `Motorbike` and `ElectricScooter` specializations, and the rental workflow. Compare how the subclasses implement refueling and recharging.

Use the menu to inspect availability, rent a vehicle, and return it to a station. This is an in-memory simulation; payment processing and persistent storage are outside its scope.

# Vehicle-Rental-App
Python-based vehicle rental system for managing motorbikes and electric scooters. Features include vehicle availability tracking, rental processing, fare calculation, refueling/recharging, and user rental history. The program includes a CLI for user interactions, supporting actions like renting, returning, and displaying vehicle details.

# Vehicle Rental System

A Python-based vehicle rental system for managing the rental and return of motorbikes and electric scooters. The system includes functionality for tracking vehicle availability, calculating fares, handling refueling/recharging, and displaying user rental histories. This project demonstrates object-oriented programming (OOP) concepts effectively.

---

## Features

- **Vehicle Management:**
  - Rent and return motorbikes and electric scooters.
  - Check vehicle availability by location.
  
- **User Interaction:**
  - Command-line interface (CLI) for seamless user experience.
  - Personalized user accounts with rental history tracking.

- **Fare Calculation:**
  - Automated fare computation based on rental duration and vehicle type.

- **Refueling & Recharging:**
  - Refuel motorbikes and recharge electric scooters.
  - Alerts for low battery on scooters.

- **Rental History:**
  - Log of past and current rentals for each user.

---

## Project Structure

- **`Vehicle` Class:** Base class for vehicles, with attributes for ID, location, availability, and rental rate.
- **`Motorbike` and `ElectricScooter` Classes:** Subclasses implementing specific features like fuel capacity and battery level.
- **`VehicleRental` Class:** Handles rental and return processes, fare calculation, and vehicle tracking.
- **`User` Class:** Manages individual user accounts, current rentals, and rental history.

---

## How to Run

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/vehicle-rental-system.git
   cd vehicle-rental-system
   ```

2. **Run the Program:**
   ```bash
   python3 Shurie_2720316.py
   ```

3. **Follow the CLI Prompts:**
   - Enter your user ID to log in.
   - Select actions like renting, returning, or refueling a vehicle.

---

## Example Usage

- Display available vehicles:
  ```
  Motorbike MB1 is available from Selly Oak
  Scooter ES1 is available from Selly Oak
  ```

- Rent a vehicle:
  ```
  Please enter your current station: Selly Oak
  Would you like to rent a (b)ike or a (s)cooter: b
  You have successfully rented vehicle MB1 from Selly Oak
  ```

- Return a vehicle:
  ```
  Please enter the returning station: Harborne
  You have successfully returned vehicle MB1 to Harborne
  The fare for this rental is £5.50
  ```

---

## Technologies Used

- Python 3.10+
- Object-Oriented Programming (OOP)
- `datetime` module for time calculations

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.


"""Console front end for the vehicle rental system."""

from rental import Fleet, RentalError, User, default_fleet

MENU = """
1. Display available vehicles
2. Rent a vehicle
3. Return a vehicle
4. Refuel / recharge your vehicle
5. Display rental history
6. Log out
7. Exit
"""


def show_available(fleet: Fleet) -> None:
    vehicles = fleet.available()
    if not vehicles:
        print("Every vehicle is out on loan.")
    for v in vehicles:
        print(f"  {v.kind.capitalize():<10} {v.vehicle_id}  at {v.location}")


def show_history(user: User) -> None:
    print(f"Rental history for {user.name} ({user.user_id}):")
    if not user.rental_history:
        print("  No rentals yet.")
    for r in user.rental_history:
        print(f"  {r.vehicle.kind} {r.vehicle.vehicle_id}")
        print(f"    Rented from {r.depart_station} at {r.rent_time:%Y-%m-%d %H:%M}")
        if r.return_time:
            print(f"    Returned to {r.return_station} at {r.return_time:%Y-%m-%d %H:%M}")
            print(f"    Fare £{r.fare()}")
        else:
            print("    Currently rented")


def rent(fleet: Fleet, user: User) -> None:
    if user.current_rental is not None:
        raise RentalError("You've already got a vehicle on loan.")
    choice = input("Rent a (b)ike or a (s)cooter? ").strip().lower()
    kinds = {"b": "motorbike", "s": "scooter"}
    if choice not in kinds:
        print("Please enter b or s.")
        return
    station = input(f"Which station? ({', '.join(fleet.stations)}) ")
    rental = fleet.rent(user, kinds[choice], station)
    print(f"You've rented {rental.vehicle.vehicle_id} from {rental.depart_station}.")


def give_back(fleet: Fleet, user: User) -> None:
    station = input(f"Which station are you returning to? ({', '.join(fleet.stations)}) ")
    rental = fleet.give_back(user, station)
    print(f"Returned {rental.vehicle.vehicle_id} to {rental.return_station}.")
    print(f"The fare for this rental is £{rental.fare()}")


def main() -> None:
    fleet = default_fleet()
    users = {"U1": User("U1", "Evie"), "U2": User("U2", "Nathan")}
    user = None

    while True:
        try:
            if user is None:
                user = users.get(input("Please enter your user ID (U1 or U2): ").strip().upper())
                if user is None:
                    print("No user exists with that ID.")
                    continue
                print(f"Welcome, {user.name}!")

            choice = input(MENU + "Choose an option: ").strip()
            match choice:
                case "1":
                    show_available(fleet)
                case "2":
                    rent(fleet, user)
                case "3":
                    give_back(fleet, user)
                case "4":
                    if user.current_rental is None:
                        print("You've not got a vehicle on loan.")
                    else:
                        print(user.current_rental.vehicle.refuel(50))
                case "5":
                    show_history(user)
                case "6":
                    user = None
                case "7":
                    break
                case _:
                    print("Please enter a number from 1 to 7.")
        except RentalError as e:
            print(e)
        except EOFError:
            print()
            break


if __name__ == "__main__":
    main()

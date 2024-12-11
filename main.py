from datetime import datetime
import math


class Vehicle:
    def __init__(self, vehicle_id, location, rate):
        self.vehicle_id = vehicle_id
        self.location = location
        self.available = True
        self.rate = rate

    def rent_vehicle(self):
        self.available = False

    def return_vehicle(self, return_station):
        self.available = True
        self.location = return_station

    def refuel(self, amount):
        pass


class Motorbike(Vehicle):
    def __init__(self, vehicle_id, location):
        super().__init__(vehicle_id, location, 1.5)
        self.capacity = 80
        self.fuel_level = 0

    def refuel(self, amount):
        """
        Task E - Insert code here
        """
        self.fuel_level += amount
        if self.fuel_level > self.capacity:
            self.fuel_level = self.capacity
        print(f'Your motorbike has been refueled to {self.fuel_level}L')


class ElectricScooter(Vehicle):
    def __init__(self, vehicle_id, location):
        super().__init__(vehicle_id, location, 1.1)
        self.battery_level = 0

    def refuel(self, amount):
        """
        Task E - Insert code here
        """
        check = self.check_battery_low()
        if check == True:
            self.battery_level = amount
            if amount > 100:
                self.battery_level = 100

            print(f"Your scooter has been recharged to {self.battery_level}%")
        pass

    def check_battery_low(self):
        """
        Task E - Insert code here
        """
        if self.battery_level < 20:
            print("ALERT: Time to recharge!")
            return True
        else:
            print(f"Battery level is {self.battery_level}%, so your scooter doesnt need charging")
            return False
        pass


class VehicleRental:
    motorbikes = [
        Motorbike('MB1', 'Selly Oak'),
        Motorbike('MB2', 'Bournville'),
        Motorbike('MB3', 'Harborne')
    ]
    scooters = [
        ElectricScooter('ES1', 'Selly Oak'),
        ElectricScooter('ES2', 'Bournville'),
        ElectricScooter('ES3', 'Harborne')
    ]

    def __init__(self):
        self.vehicle = None
        self.depart_station = None
        self.rent_time = None
        self.return_station = None
        self.return_time = None

    def rent_vehicle(self, vehicle):
        """
        Task C - Insert code here
        """
        self.vehicle = vehicle
        self.vehicle.rent_vehicle()
        self.depart_station = vehicle.location
        self.rent_time = datetime.now()
        print(self.rent_time,"\n")
        print(f'You have successfully rented vehicle {self.vehicle.vehicle_id} from {self.depart_station}')

    def return_vehicle(self, return_station):
        fare = 0
        """
        Task D - Insert code here
        """
        self.return_time = datetime.now()
        self.return_station = return_station
        self.vehicle.return_vehicle(return_station)
        print(self.return_time,"\n")
        fare = self.calculate_fare()
        print(f'You have successfully returned vehicle {self.vehicle.vehicle_id} to {self.return_station}')
        print(f'The fare for this rental is £{fare:.2f}')

    def calculate_fare(self):
        fare = 0
        """
        Task D - Insert code here
        """

        diff =  self.return_time - self.rent_time

        minutes = diff.total_seconds() / 60
  

        fare = self.vehicle.rate * minutes

        return fare


class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.current_rental = None
        self.rental_history = []

    def rent_vehicle(self, vehicle: Vehicle):
        """
        Task C - Insert code here
        """
        
        self.current_rental =  VehicleRental()
        self.rental_history.append(self.current_rental)
        self.current_rental.rent_vehicle(vehicle)
        pass

    def return_vehicle(self, return_station):
        """
        Task D - Insert code here
        """

        self.current_rental.return_vehicle(return_station)
        self.current_rental = None
        pass

    def display_rental_history(self):
        print(f'Rental history for {self.name} with ID: {self.user_id}')
        for rental in self.rental_history:
            print(f'Vehicle {rental.vehicle.vehicle_id}')
            print(f'  Rented from: {rental.depart_station} at {rental.rent_time}')
            if rental.return_station:
                print(f'  Returned to: {rental.return_station} at {rental.return_time}')
            else:
                print(f'  Status: Currently rented')
            print('-' * 55)


def display_available_vehicles():
    bikes = VehicleRental.motorbikes
    scooters = VehicleRental.scooters
    for b in bikes:
        print(f"Motorbike { b.vehicle_id} is available from {b.location}")
    for s in scooters:
        print(f"Scooter { s.vehicle_id} is available from {s.location}")
    pass


def main():
    users = {
        'U1': User('U1', 'Evie'),
        'U2': User('U2', 'Nathan')
    }
    current_user = None
    while True:
        if not current_user:
            user_id = input('Please enter your user ID: ')
            if users.get(user_id):
                current_user = users.get(user_id)
                print(f"welcom {current_user}")
            else:
                print(f"no user exist with ID {user_id}")
                continue

        try:
            choice = int(input('Book a Motorbike or an Electric Scooter\n'
                               '1. Display available vehicles\n'
                               '2. Rent a vehicle\n'
                               '3. Return a vehicle\n'
                               '4. Refuel / Recharge a vehicle\n'
                               '5. Display user history\n'
                               '6. Logout\n'
                               '7. Exit\n'))
        except ValueError:
            print('You must enter a number from 1-7')
            continue

        match choice:
            case 1:
                display_available_vehicles()
            case 2:
                if not current_user.current_rental:
                    borrow_station = input('Please enter your current station: ')
                    vehicle_type = input('Would you like to rent a (b)ike or a (s)cooter: ')
                    """
                    Task C - Insert code here
                    """
                    if not (vehicle_type.lower() == "s" or "b"):
                        print(f"Invalid option, you must pick 'b'(bike) or 's'(scooter)")
                        continue
                    else: 

                        if vehicle_type == 's':
                            scooters = VehicleRental.scooters
                            for s in scooters:
                                if s.location == borrow_station:
                                    if not s.available:
                                        print(f"No Scooters are available to rent at {borrow_station}")
                                        continue
                                    else:
                                        available_scooter = s
                                        current_user.rent_vehicle(available_scooter)

                
                            
                        if vehicle_type == 'b':
                            bikes = VehicleRental.motorbikes
                            for b in bikes:
                                if b.location == borrow_station:
                                    if not b.available:
                                        print(f"No Scooters are available to rent at {borrow_station}")
                                        continue
                                    else:
                                        available_bike = b
                                        current_user.rent_vehicle(available_bike)

                        


                        
                else:
                    print("You've already got a vehicle on loan")

            case 3:
                if current_user.current_rental:
                    return_station = input('Please enter the returning station: ')
                    """
                    Task D - Insert code here
                    """
                    current_user.return_vehicle(return_station)
                else:
                    print("You've not got a vehicle on loan, so can't return anything")
            case 4:
                if current_user.current_rental:
                    """
                    Task E - Insert code here
                    """
                    current_vehicle = current_user.current_rental.vehicle
                    current_vehicle.refuel(50)
                    pass
                else:
                    print("You've not got a vehicle on loan, so can't refuel/recharge anything")
            case 5:
                current_user.display_rental_history()
            case 6:
                current_user = None
            case 7:
                break
            case _:
                print('Invalid choice entered. You must enter a number from 1-7')


if __name__ == '__main__':
    main()

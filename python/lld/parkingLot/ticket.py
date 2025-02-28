class Ticket:
    def __init__(self, ticket_id, vehicle_id, floor_id, spot_id, entry_time, exit_time):
        self.ticket_id = ticket_id
        self.vehicle_id = vehicle_id
        self.floor_id = floor_id
        self.spot_id = spot_id
        self.entry_time = entry_time
        self.exit_time = exit_time

    def calculate_fare(self):
        val = (self.exit_time - self.entry_time) // 60
        return val * 5

    def display_ticket(self):
        return f"{self.ticket_id} {self.vehicle_id} {self.floor_id} {self.spot_id} {self.entry_time} {self.exit_time} {self.calculate_fare}"


class Floor:
    def __init__(self, floor_id, address, total_spots, avaiable_spots):
        self.floor_id = floor_id
        self.address = address
        self.total_spots = total_spots
        self.avaiable_spots = avaiable_spots

    def add_spot():
        pass

    def get_available_spots():
        pass


class ParkingLot:
    def __init__(self, name, address, total_spots, avaiable_spots):
        self.name = name
        self.address = address
        self.total_spots = total_spots
        self.avaiable_spots = avaiable_spots
        self.floor = {}

    def add_floor():
        pass

    def find_parking_spot():
        pass


from enum import Enum


class SpotType(Enum):
    CAR = "Car"
    BIKE = "Bike"
    ELECTRIC_CAR = "Electric Car"
    ELECTRIC_BIKE = "Electric Bike"


class ParkingSpot:
    def __init__(self, spot_id, spot_type, is_occupied, vehicle_id):
        self.spot_id = spot_id
        self.spot_type = spot_type
        self.is_occupied = is_occupied
        self.vehicle_id = vehicle_id

    def assgin_vechile():
        pass

    def free_spot():
        pass


class Entrance:
    def __init__(self, entrance_id, floor_id):
        self.floor_id = floor_id
        self.entrance_id = entrance_id

    def process_entry():
        pass


class Exit:
    def __init__(self, exit_id, floor_id):
        self.exit_id = exit_id
        self.floor_id = floor_id

    def process_exit():
        pass

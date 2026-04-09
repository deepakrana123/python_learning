from enum import Enum
from datetime import datetime
import heapq

from enum import Enum


class SpotType(Enum):
    CAR = "Car"
    BIKE = "Bike"
    ELECTRIC_CAR = "Electric Car"
    ELECTRIC_BIKE = "Electric Bike"
    TRUCK = "Truck"


class ParkingSpot:
    def __init__(self, spot_id, spot_type, distance_to_exit):
        self.spot_id = spot_id
        self.spot_type = spot_type
        self.is_occupied = False
        self.distance_to_exit = distance_to_exit
        self.vehicle = None

    def assgin_vechile(self, vehicle):
        if not self.is_occupied:
            self.vehicle = vehicle
            self.is_occupied = True
            return True
        return False

    def free_spot(self):
        self.vehicle = None
        self.is_occupied = False

    def get_spot_id(self):
        return self.spot_id

    def get_vechile_type(self):
        return self.vehicle

    def get_hourly_Rate(self):
        rates = {
            SpotType.CAR: 5,
            SpotType.BIKE: 2,
            SpotType.ELECTRIC_CAR: 6,
            SpotType.ELECTRIC_BIKE: 3,
            SpotType.TRUCK: 10,
        }
        return rates.get(self.spot_type, 5)

    def __lt__(self, other):
        return self.distance_to_exit < other.distance_to_exit


class Ticket:
    def __init__(
        self,
        ticket_id,
        vehicle_id,
        floor_id,
        spot_id,
        entry_time,
        hourly_rate,
    ):
        self.ticket_id = ticket_id
        self.vehicle_id = vehicle_id
        self.floor_id = floor_id
        self.spot_id = spot_id
        self.entry_time = entry_time
        self.exit_time = None
        self.hourly_rate = hourly_rate
        self.vechile_type = None
        self.peak = None
        self.discount = None

    def calculate_fare(self, vechile_type=None, peak=0, discount=0):
        if self.exit_time:
            duration_minutes = (self.exit_time - self.entry_time) // 60
            hours = max(duration_minutes // 60, 1)
            if vechile_type == "ELETRIC":
                fare = (
                    hours * self.hourly_rate
                    - (hours * self.hourly_rate * discount) // 100
                )
                return fare
            elif peak:
                fare = (
                    hours * self.hourly_rate + (hours * self.hourly_rate * peak) // 100
                )
                return fare
            return hours * self.hourly_rate
        return 0

    def close_tickets(self):
        self.exit_time = datetime.now()

    def display_ticket(self):
        return f"{self.ticket_id} {self.vehicle_id} {self.floor_id} {self.spot_id} {self.entry_time} {self.exit_time} {self.calculate_fare}"


class Floor:
    def __init__(self, floor_id, address, spots_info):
        self.floor_id = floor_id
        self.address = address
        self.spot_heap = {
            "CAR": [],
            "BIKE": [],
            "ELECTRIC_CAR": [],
            "ELECTRIC_BIKE": [],
            "TRUCK": [],
        }
        self.totalSpots = len(spots_info)
        self.spots_in_floor = {spot_type: 0 for spot_type in SpotType}
        self.occupied = 0

        for spot_id, spot_type, distance_to_exit in spots_info:
            spot = ParkingSpot(spot_id, spot_type, distance_to_exit)
            heapq.heappush(self.spot_heap[spot_type], spot)
            self.spots_in_floor[spot_type] += 1

    def get_available_spots(self, vehicle_type):
        temp_heap = []
        closest_spot = None
        while self.spot_heap[vehicle_type]:
            spot = heapq.heappop(self.spot_heap[vehicle_type])
            if not spot.is_occupied:
                closest_spot = spot
                break
            heapq.heappush(temp_heap, spot)
        while temp_heap:
            heapq.heappush(self.spot_heap[vehicle_type], heapq.heappop(temp_heap))
        return closest_spot

    def update_spots(self, spot_type, isoccupied):
        if isoccupied:
            self.available_spots[spot_type] -= 1
            self.occupied_spots += 1
        else:
            self.available_spots[spot_type] += 1
            self.occupied_spots -= 1


class ParkingLot:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.floors = []
        self.tickets = {}
        self.total_spots = 0
        self.available_spots = 0

    def add_floor(self, floor):
        self.floors.append(floor)
        self.total_spots += floor.total_spots
        for spot_type in SpotType:
            self.available_spots[spot_type] += floor.available_spots[spot_type]

    def issue_ticket(self, vehicle):
        for floor in self.floors:
            spot = floor.find_available_spot(vehicle.vehicle_type)
            if spot:
                spot.assign_vehicle(vehicle)
                floor.update_spot_counts(vehicle.vehicle_type, True)
                self.available_spots[vehicle.vehicle_type] -= 1
                ticket_id = len(self.tickets) + 1
                hourly_rate = spot.get_hourly_Rate()
                ticket = Ticket(
                    ticket_id,
                    vehicle.vechile_id,
                    floor.floor_id,
                    spot.spot_id,
                    datetime.now(),
                    hourly_rate,
                )
                self.tickets[ticket_id] = ticket
                return ticket
        return None

    def pre_book(self, vehicle, entry_time, exit_time):
        for floor in self.floors:
            spot = floor.find_available_spot(vehicle.vehicle_type)
            if spot:
                spot.assign_vehicle(vehicle)
                floor.update_spot_counts(vehicle.vehicle_type, True)
                self.available_spots[vehicle.vehicle_type] -= 1
                ticket_id = len(self.tickets) + 1
                hourly_rate = spot.get_hourly_Rate()
                ticket = Ticket(
                    ticket_id,
                    vehicle.vechile_id,
                    floor.floor_id,
                    spot.spot_id,
                    entry_time,
                    exit_time,
                    hourly_rate,
                )
                Analytic.add_total_revenue(ticket.calculate_fare())
                Analytic.add_total_parktime(entry_time, exit_time)
                ticket.exit_time = exit_time
                self.tickets[ticket_id] = ticket
                return ticket
        return None

    def process_exit(self, ticket_id):
        ticket = self.tickets[ticket_id]
        if ticket:
            ticket.close_ticket()
            for floor in self.floors:
                for spot in floor.spots:
                    pass


class Entrance:
    def __init__(self, entrance_id, floor_id):
        self.floor_id = floor_id
        self.entrance_id = entrance_id

    def process_entry():
        pass


class User:
    def __init__(self, user_id, name, contact_number, vehicle):
        self.user_id = user_id
        self.name = name
        self.contact_number = contact_number
        self.vehicle = vehicle


class Exit:
    def __init__(self, exit_id, floor_id):
        self.exit_id = exit_id
        self.floor_id = floor_id

    def process_exit():
        pass


class Analytic:
    def __init__(self):
        self.fare = 0
        self.total_time = 0
        self.peak = 0

    def add_total_revenue(self, fare):
        self.fare += fare

    def add_total_parktime(self, entry_time, exit_time):
        duration = (exit_time - entry_time).seconds // 60
        self.total_time += duration

    def add_total_peak_hours(self, peak):
        self.peak += peak

    def get_total_revenue(self):
        return self.fare

    def get_total_parktime(self):
        return self.total_time

    def get_total_peak_hours(self):
        return self.peak

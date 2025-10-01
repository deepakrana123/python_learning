from abc import ABC, abstractmethod
import datetime
from threading import threading

from enum import Enum


class VechileType(Enum):
    CAR = 1
    BUS = 2
    TWO_WHEELER = 3
    ELECTRIC_WHEELER = 4


class SLOT_TYPE(Enum):
    MEDIUM = 2
    SMALL = 1
    LARGE = 3


class Slot:
    def __init__(
        self,
        slotType: SLOT_TYPE,
        id,
        distance_from_entry: float,
        floor_number: int,
    ):
        self.slotType = slotType
        self.slot_id = id
        self.floor_number = floor_number
        self.distance_from_entry = distance_from_entry
        self.is_available = True
        self.lock = threading.Lock()

    def hold(self):
        with self.lock:
            if not self.is_available:
                raise Exception(f"Slot {self.slot_id} not available")
            self.is_available = True

    def relase(self):
        with self.lock:
            if not self.is_available:
                raise Exception(f"Slot {self.slot_id} available")
            self.is_available = False


class Vehicle:
    def __init__(self, vechile_number, vehicle_type: VechileType):
        vehicle_type = vehicle_type
        vechile_number = vechile_number

class Ticket:
    def __init__(
        self, ticket_id, starttime, endtime, amountPaid, vechile_type, vechilde_number
    ):
        self.ticket_id = ticket_id
        self.starttime = starttime
        self.endtime = endtime
        self.amountPaid = amountPaid
        self.vechile_type = vechile_type
        self.vechile_number = vechilde_number


rate_per_hour = {"CAR": 20, "BUS": 50, "TWO_WHEELER": 10, "ELECTRIC_WHEELER": 15}


class PricingStrategy:
    @abstractmethod
    def calculate_fee(
        self, entry_time: datetime.datetime, exit_time: datetime.datetime, vehicle_type
    ):
        pass


class HourlyPricing:
    def calculate_fee(self, entry_time, exit_time, vehicle_type):
        hours = (exit_time - entry_time).seconds // 3600 + 1
        return rate_per_hour[vehicle_type] * hours


class FlatRatePricing:
    def calculate_fee(self, entry_time, exit_time, vehicle_type):
        return 100 * rate_per_hour[vehicle_type]


class WeekendPricing(PricingStrategy):
    def calculate_fee(self, entry_time, exit_time, vehicle_type):
        if entry_time.weekday() >= 5:
            return 50
        else:
            return 20


class PricingManager:
    def __init__(self, strategy: PricingStrategy):
        self.strategy = strategy

    def calculate_fee(self, entry_time, exit_time, vehicle_type):
        return self.strategy.calculate_fee(entry_time, exit_time, vehicle_type)


class FloorManager:
    def __init__(self, floor_number):
        self.floor_number = floor_number
        self.slot = []
        self.lock = threading.Lock()
    

    def add_slot(self):
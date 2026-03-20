from enum import Enum


class VehicleType(Enum):
    CAR = "Car"
    BIKE = "Bike"
    ELECTRIC_CAR = "Electric Car"
    ELECTRIC_BIKE = "Electric Bike"


class Vehicle:
    def __init__(self, vehicle_id, vehicle_type: VehicleType, license_plate: str):
        self.vehicle_id = vehicle_id
        self.vehicle_type = vehicle_type
        self.license_plate = license_plate

    def display_info(self):
        return f"ID: {self.vehicle_id} | Type: {self.vehicle_type.value} | Plate: {self.license_plate}"

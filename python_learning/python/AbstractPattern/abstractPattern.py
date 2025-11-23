class Car:
    def drive(self):
        pass
class Bike:
    def ride(self):
        pass
class ToyotaCar(Car):
    def drive(self):
        return "Driving a Toyota Car"
class ToyotaBike(Bike):
    def ride(self):
        return "Ride a toyota bike"
class HondaCar(Car):
    def drive(self):
        return "Drive a honda Car"
class HondaBike(Bike):
    def ride(self):
        return "Ride a honda bike"
class VehicleFactory:
    def create_car(self):
        pass
    def create_bike(self):
        pass
class ToyotaFactory(VehicleFactory):
    def create_car(self):
        return ToyotaCar()
    def create_bike(self):
        return ToyotaBike()

class HondaFactory(VehicleFactory):
    def create_car(self):
        return HondaCar()
    def create_bike(self):
        return HondaBike()

def client_code(factory: VehicleFactory):
    car = factory.create_car()
    bike = factory.create_bike()
    print(car.drive())
    print(bike.ride())


 
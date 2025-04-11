from datetime import date
from enum import Enum
from threading import Lock


class Flight:
    def __init__(self, filghtNumber, source, departure, arrivalTime, destination):
        self.filghtNumber = filghtNumber
        self.source = source
        self.departure = departure
        self.arrivalTime = arrivalTime
        self.availableSeats = []
        self.destination = destination

    def get_source(self):
        return self.source

    def get_destination(self):
        return self.destination

    def get_departure_date(self):
        return self.departure


class FlightSearch:
    def __init__(self, flights):
        self.flights = flights

    def search_by_source(self, source, destination, date):
        return [
            flight
            for flight in self.flights
            if flight.get_source().lower() == source
            and flight.get_destination().lower() == destination
            and flight.get_departure_date().date() == date
        ]


class SeatStatus(Enum):
    AVAILABLE = 1
    RESERVED = 2
    OCCUPIED = 3


class SeatType(Enum):
    ECONOMY = 1
    PREMIUM_ECONOMY = 2
    BUSINESS = 3
    FIRST_CLASS = 4


class Seat:
    def __init__(self, seat_number, seat_type):
        self.seat_number = seat_number
        self.seat_type = seat_type
        self.status = SeatStatus.AVAILABLE

    def reserve(self):
        self.status = SeatStatus.RESERVED

    def release(self):
        self.status = SeatStatus.AVAILABLE


class Passenger:
    def __init__(self, passenger_id, name, email, phone):
        self.id = passenger_id
        self.name = name
        self.email = email
        self.phone = phone


class Aircraft:
    def __init__(self, tail_number, model, total_seats):
        self.tail_number = tail_number
        self.model = model
        self.total_seats = total_seats


class PaymentStatus(Enum):
    PENDING = 1
    COMPELETED = 2
    FAILED = 3
    REFUNDED = 4


class Payment:
    def __init__(self, payment_id, payment_method, amount):
        self.payment_id = payment_id
        self.payment_method = payment_method
        self.amount = amount
        self.status = PaymentStatus.PENDING

    def process_payment(self):
        self.status = PaymentStatus.COMPELETED


class PaymentProcessor:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def process_payment(self, payment):
        payment.process_payment()


class BookingStatus(Enum):
    CONFIRMED = 1
    CACELLED = 2
    PENDING = 3
    EXPIRED = 4


class Booking:
    def __init__(self, booking_number, flight, passenger, seat, price):
        self.booking_number = booking_number
        self.flight = flight
        self.passenger = passenger
        self.seat = seat
        self.price = price
        self.status = BookingStatus.CONFIRMED

    def cancel(self):
        self.status = BookingStatus.CACELLED


class BookingManager:
    _instance = None
    _lock = Lock()

    def __init__(self):
        self.bookings = {}
        self.booking_counter = 0

    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def create_booking(self, flight, passenger, seat, price):
        booking_number = self._generate_booking_number()
        booking = Booking(booking_number, flight, passenger, seat, price)
        with self._lock:
            self.bookings[booking_number] = booking
        return booking

    def cancel_booking(self, booking_number):
        with self._lock:
            booking = self.bookings.get(booking_number)
            if booking:
                booking.cancel()

    def _generate_booking_number(self):
        self.booking_counter += 1
        timestamp = date.now().strftime("%Y%m%d%H%M%S")
        return f"BKG{timestamp}{self.booking_counter:06d}"


class AirlineManagementSystem:
    def __init__(self):
        self.flight = []
        self.aircrafts = []
        self.flight_search = FlightSearch(self.flight)
        self.booking_manager = BookingManager()
        self.payment_processor = PaymentProcessor()

    def add_flight(self, flight):
        self.flight.append(flight)

    def add_aircraft(self, aircraft):
        self.aircrafts.append(aircraft)

    def search_flights(self, source, destination, date):
        self.flight_search.search_by_source(source, destination, date)

    def cancel_booking(self, booking_number):
        self.booking_manager.cancel_booking(booking_number)

    def process_payment(self, payment):
        self.payment_processor.process_payment(payment)

    def booking_flight(self, flight, passenger, seat, price):
        return self.booking_manager.create_booking(flight, passenger, seat, price)

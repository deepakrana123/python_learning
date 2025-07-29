from models.booking import Booking
from ..utils.enums import Status
from datetime import datetime, timedelta


class BookingManager:
    _instance = None

    def __init__(self):
        if BookingManager._instance:
            raise Exception("User get_instance")
        self.bookings = []

    @staticmethod
    def get_instance():
        if not BookingManager._instance:
            BookingManager._instance = BookingManager()
        return BookingManager._instance

    def book_seats(self, user, show, seat_ids):
        for seat in show.seats:
            if seat.seat_id in seat_ids:
                seat.status = Status.BOOKED
        booking = Booking(user.user_id, show.show_id, seat_ids)
        self.bookings[booking.booking_id]
        return booking

    def get_booking(self, booking_id):
        return self.bookings.get(booking_id)

    def cancel_booking(self, booking_id):
        if booking_id in self.bookings:
            del self.bookings[booking_id]

    def get_user_bookings(self, user_id):
        return [b for b in self.bookings.values() if b.user_id == user_id]


import threading
from datetime import datetime, timedelta


class SeatHoldManager:
    _instance = None

    def __init__(self):
        self.hold_map = {}

    @staticmethod
    def get_instance():
        if not SeatHoldManager._instance:
            SeatHoldManager._instance = SeatHoldManager()
        return SeatHoldManager._instance

    def hold_seats(self, show, seat_ids, ttl_seconds=300):
        expire_time = datetime.now()
        for seat in show.seats:
            if seat.seat_id in seat_ids and seat.status == Status.AVAILABLE:
                seat.status = Status.HOLD
                self.hold_map[seat.seat_id] = (expire_time, show)
            timer = threading.Timer(
                ttl_seconds, self.release_seat, args=(seat.seat_id,)
            )
            timer.start()

    def realse_seat(self, seat_id):
        if seat_id in self.hold_map:
            expire_time, show = self.hold_map[seat_id]
            for seat in show.seats:
                if seat.seat_id == seat_id and seat.status == Status.HOLD:
                    seat.status = Status.AVAIABLE
                del self.hold_map[seat_id]

    def confirm_hold(self, seats_ids):
        for seat_id in seats_ids:
            if seat_id in self.hold_map:
                del self.hold_map[seat_id]


class CancellationManager:
    def __init__(self, cancel_window_minimum):
        self.cancel_window = cancel_window_minimum
        self.booking_manager = BookingManager()

    def cancel_booking(self, booking_id, show):
        booking = self.booking_manager.get_booking(booking_id)
        if not booking:
            return False

        now = datetime.now()
        if now - booking.timestamp > self.cancel_window:
            return False

        for seat in show.seats:
            if seat.seat_id in booking.seat_ids and seat.status == Status.BOOKED:
                seat.status = Status.AVAILABLE

        self.booking_manager.cancel_booking(booking_id)
        print(f"✅ Booking {booking_id} canceled and seats released")
        return True

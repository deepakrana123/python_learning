from enum import Enum
from typing import List
from datetime import datetime, timedelta
from threading import Timer


class SeatTye(Enum):
    Regular, Premium, Vip = 1, 2, 3


class SeatStatus(Enum):
    Available, Booked, Reserved = 1, 2, 3


class BookingStatus(Enum):
    Pending, Confirmed, Cancelled = 1, 2, 3


class Seat:
    def __init__(self, id, seatNumber, seatType, price, status):
        self.status = SeatStatus.Reserved
        self.seatNumber = seatNumber
        self.seatType = seatType
        self.price = price
        self.id = id
        self.hold_at = None
        self.hold_duration = timedelta(minutes=5)

    def bookSeats(self):
        self.status = SeatStatus.Booked
        self.hold_at = None

    def release(self):
        self.status = SeatStatus.Available
        self.hold_at = None

    def hold(self):
        self.status = SeatStatus.Reserved
        self.hold_at = datetime.now()

    def is_hold_expired(self):
        if self.status != SeatStatus.Reserved or self.hold_at is None:
            return False
        return datetime.now() > self.hold_at - self.hold_duration


class Concert:
    def __init__(self, id, artist, venue, date, time, seatList: List[Seat]):
        self.id = id
        self.artist = artist
        self.venue = venue
        self.date = date
        self.time = time
        self.seats = seatList


class User:
    def __init__(self, id, name, email):
        self.email = email
        self.id = id
        self.name = name

    def getEmail(self):
        return self.email


class SeatNotAvailableException:
    def __init__(self, message="Seat is not available for booking."):
        super().__init__(message)


class Booking:
    def __init__(self, id, user, concert, seats, totalPrice):
        self.id = id
        self.user = user
        self.concert = concert
        self.seats = seats
        self.totalPrice = totalPrice
        self.status = BookingStatus.Pending

    def bookingCancelled(self, seat):
        if seat.status == SeatStatus.Available:
            seat.release()
        raise SeatNotAvailableException(f"Seat {seat.seatNumber} is already available")

    def bookSeat(self, seat: Seat):
        if seat.status != SeatStatus.Available:
            raise SeatNotAvailableException(f"Seat {seat.seatNumber} is not available.")
        seat.bookSeats()


class SeatManager:
    def __init__(self):
        self.allSeats = []

    def addSeats(self, seats: List[Seat]):
        self.allSeats.extend(seats)

    def findBySeatType(self, type):
        seatTypes = []
        for seat in self.allSeats:
            if seat.seatType == type:
                seatTypes.append(seat)
        return seatTypes


class ConcertManager:
    def __init__(self):
        self.concert = []
        self.bookings = []
        self.users = []
        self.seatManager = SeatManager()

    def add_concert(self, concert):
        self.concert.append(concert)
        self.seatManager.addSeats(concert.seats)

    def add_user(self, user: User):
        self.users.append(user)

    def bookTicket(self, user: User, concert: Concert, seats: List[Seat]):
        selectedSeat = []
        total_price = 0
        if not any(u.id == user.id for u in self.users):
            raise SeatNotAvailableException(f"User {user.id} is not available")
        if not any(u.id == concert.id for u in self.concert):
            raise SeatNotAvailableException(f"concert {concert.id} is not available")
        for seat in concert.seats:
            if seat.seatNumber not in seats:
                raise SeatNotAvailableException(
                    f"Seat {seat.seatNumber} is not available."
                )
            if seat.seatNumber in seats:
                if seat.status != SeatStatus.Available:
                    raise SeatNotAvailableException(
                        f"Seat {seat.seatNumber} is not available."
                    )
                selectedSeat.append(seat)
                total_price += seat.price

        for seat in selectedSeat:
            if seat.status == SeatStatus.Reserved:
                if seat.is_hold_expired():
                    seat.release()
            else:
                raise SeatNotAvailableException(
                    f"Seat {seat.seatNumber} is currently on hold."
                )
            seat.bookSeat()
        booking = Booking(
            len(self.bookings) + 1, user, concert, selectedSeat, total_price
        )
        booking.bookingConfirm()
        self.bookings.append(booking)
        return booking

    def cancelTicket(self, seat: Seat):
        seat.release()

    def findBySeatType(self, seatType):
        return self.seatManager.findBySeatType(seatType)

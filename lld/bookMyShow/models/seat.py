import uuid

from ..utils.enums import SeatType, Status


class Seat:
    def __init__(self, seat_number, seat_type: SeatType = "NORMAL"):
        self.seat_id = str(uuid.uuid4())
        self.seat_number = seat_number
        self.seat_type = seat_type
        self.is_booked = Status.AVAIABLE

    def bookSeat(self):
        self.status = Status.BOOKED

    def bookCancelled(self):
        self.status = Status.AVAIABLE

    def bookHold(self):
        self.status = Status.HOLD

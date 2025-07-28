import uuid
from datetime import datetime


class Booking:
    def __init__(self, user_id, show_id, seat_ids):
        self.booking_id = str(uuid.uuid4())
        self.user_id = user_id
        self.show_id = show_id
        self.seat_ids = seat_ids  # List of seat_ids
        self.timestamp = datetime.now()

import uuid


class Screen:
    def __init__(self, screen_number):
        self.screen_id = str(uuid.uuid4())
        self.screen_number = screen_number
        self.seats = []  # List of Seat objects

    def addSeats(self, seat):
        self.seats.append(seat)

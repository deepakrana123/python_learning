import uuid


class Show:
    def __init__(self, movie_id, screen_id, start_time, end_time):
        self.show_id = str(uuid.uuid4())
        self.movie_id = movie_id
        self.screen_id = screen_id
        self.start_time = start_time  # datetime
        self.end_time = end_time
        self.seats = []  # List of Seat objects (copied from screen)
        self.occupancy = 0

    def getOccupancy(self):
        return self.occupancy

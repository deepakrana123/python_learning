from models.booking import Booking


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
        booked = []
        for seat in show.seats:
            if seat.seat_id in seat_ids:
                if seat.status != seat.status.BOOKED:
                    raise Exception("expections")
            seat.status = seat.status.BOOKED
            booked.append(seat.seat_number)
        booking = Booking(user.user_id, show.show_id, seat_ids)
        booked.append(booking)
        return booking

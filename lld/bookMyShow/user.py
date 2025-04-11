from datetime import datetime
from datetime import timedelta


class User:
    def __init__(self, id, email, name, password, role):
        self.email = email
        self.name = name
        self.password = password
        self.role = role
        self.id = id


class Theater:
    def __init__(self, id, address):
        self.id = id
        self.screens = []
        self.address = address

    def addScreen(self, screen):
        self.screens.append(screen)

    def get_address(self):
        return self.address


class Screen:
    def __init__(self, screenLayout, seats):
        self.screenLayout = screenLayout
        self.seats = seats

    def addMoreSeats(self, seat):
        self.seats.append(seat)


class Show:
    def __init__(
        self, show_id, screen, movie, threater, start_time, end_time, totalSeats
    ):
        self.movie = movie
        self.screen = screen
        self.threater = threater
        self.start_time = start_time
        self.end_time = end_time
        self.show_id = show_id
        self.seats = [
            Seat(seat.id, seat.seatType, Status.AVAILABLE) for seat in screen.seats
        ] * totalSeats
        self.totalSeats = totalSeats


class Movie:
    def __init__(self, movieName, movieLang, movieDuration):
        self.movieName = movieName
        self.movieLang = movieLang
        self.movieDuration = movieDuration
        self.totalShow = []

    def getMovieName(self):
        return self.movieName


from enum import Enum


class SeatType(Enum):
    VIP, SUBVIP, NORMAL = 1, 2, 3


class Status(Enum):
    AVAIABLE, RESERVED, BOOKED, HOLD = 1, 2, 3, 4


class Price:
    def __init__(self, seat):
        self.seat = seat
        self.totalPrice = 0

    def makePrice(self, peak=None, seatType=None):
        if peak:
            self.totalPrice += peak * self.seat.price
        if seatType == "VIP":
            self.totalPrice += 20 * self.seat.price
        return self.totalPrice


class Seat:
    def __init__(self, id, seatType, status, screenId, showId, price):
        self.id = id
        self.seaType = seatType
        self.status = status
        self.screenId = screenId
        self.showId = showId
        self.price = price

    def bookSeat(self):
        self.status = Status.BOOKED

    def bookCancelled(self):
        self.status = Status.AVAIABLE

    def bookHold(self):
        self.status = Status.HOLD

    def getPrice(self):
        return self.price


class CityFilter:
    @staticmethod
    def search(self, city, shows):
        city = city.lower()
        matching_shows = []
        for show in shows:
            if show.threater.getAddress.lower() == city:
                matching_shows.append(show)
        return matching_shows


class MovieFilter:
    @staticmethod
    def search(self, movieName, shows):
        movieName = movieName.lower()
        matching_shows = []
        for show in shows:
            if show.movie.getMovieName.lower() == movieName:
                matching_shows.append(show)
        return matching_shows


class Filter:
    _search = {
        "city": CityFilter,
        "movie": MovieFilter,
    }

    @staticmethod
    def getFilter(fiterValue, value, shows):
        return Filter._search.get(fiterValue, CityFilter)().search(value, shows)


import heapq


class Booking:
    def __init__(self, booking_id, user, show):
        self.user = user
        self.show = show
        self.selected_seats = []
        self.status = "CONFIRMED"
        self.timestamp = datetime.now()
        self.booking_id = booking_id
        self.seatsBooked = []

    def filter(self, shows, filters):
        f = Filter.getFilter("city", filters.city, shows)
        f1 = Filter.getFilter("movie", filters.movieName, f)
        return f1

    def bookSeats(self, totalSeat):
        if self.show.seats.totalSeats < totalSeat:
            raise Exception("Seats are less")
        for seat in self.show.seats[totalSeat + 1]:
            seat.bookHold()
            heapq.heappush(self.seatsBooked, (datetime.now() + timedelta(10), seat.id))

    def selfBookCancel(self, id):
        self.booking.seatsBooked = [
            (expiry, seatId)
            for (expiry, seatId) in self.booking.seatsBooked
            if seatId != id
        ]
        heapq.heapify(self.booking.seatsBooked)


import threading
import time


class TTLJobSchedular:
    def __init__(self, booking):
        self.interval = 5
        self.booking = booking

    def run(self):
        def check_expiry():
            while True:
                now = datetime.now()
                expired = []
                while self.booking.seatsBooked:
                    expriy, seatId = self.booking.seatsBooked[0]
                    if expriy < now:
                        for seat in self.booking.show.seats:
                            if seat.id == seatId:
                                seat.bookCancelled()
                            expired.append(seat_id)
                            heapq.heappop(self.booking.seatsBooked)
                    else:
                        break

                for seat_id in expired:
                    del self.booking.seatsBooked[seat_id]
                time.sleep(self.interval)

        thread = threading.Thread(target=check_expiry)
        thread.daemon = True
        thread.start()

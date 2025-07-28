# from datetime import datetime
# from datetime import timedelta
# from enum import Enum
# import threading
# import time


# class User:
#     def __init__(self, id, email, name, password, role):
#         self.email = email
#         self.name = name
#         self.password = password
#         self.role = role
#         self.id = id


# class Theater:
#     def __init__(self, id, address):
#         self.id = id
#         self.screens = []
#         self.address = address

#     def addScreen(self, screen):
#         self.screens.append(screen)

#     def get_address(self):
#         return self.address


# class Screen:
#     def __init__(self, screen_layout):
#         self.screen_layout = screen_layout
#         self.seats = []

#     def addMoreSeats(self, seat):
#         self.seats.append(seat)


# class Show:
#     def __init__(
#         self, show_id, screen, movie, threater, start_time, end_time, total_seats
#     ):
#         self.movie = movie
#         self.screen = screen
#         self.threater = threater
#         self.start_time = start_time
#         self.end_time = end_time
#         self.show_id = show_id
#         self.total_seats = total_seats
#         self.seats = []
#         for seat in screen.seats:
#             self.seats.append(
#                 Seat(
#                     seat.id,
#                     seat.seat_type,
#                     Status.AVAILABLE,
#                     seat.screen_id,
#                     show_id,
#                     0,
#                 )
#             )

#     def get_total_seats(self):
#         return self.totalSeats

#     def occupany(self):
#         booked_count = len(
#             [seat for seat in self.seats if seat.status == Status.BOOKED]
#         )
#         return (booked_count / self.total_seats) * 100 if self.total_seats else 0


# class Movie:
#     def __init__(self, name, language, duration):
#         self.name = name
#         self.language = language
#         self.duration = duration
#         self.totalShow = []

#     def get_movie_name(self):
#         return self.name


# class Seat:
#     def __init__(self, id, seat_type, status, screen_id, show_id, price):
#         self.id = id
#         self.seat_type = seat_type
#         self.status = status
#         self.screen_id = screen_id
#         self.show_id = show_id
#         self.price = price

#     def bookSeat(self):
#         self.status = Status.BOOKED

#     def bookCancelled(self):
#         self.status = Status.AVAIABLE

#     def bookHold(self):
#         self.status = Status.HOLD


# class Price:
#     def __init__(self, show, seat):
#         self.show = show
#         self.seat = seat
#         self.averagePrice = 250

#     def last_minute_surge(self):
#         date = datetime.now()
#         return 30 if (self.show.end_time - date).seconds < 1800 else 0

#     def early_morning_bird(self):
#         date = datetime.now()
#         return -30 if (self.show.end_time - date).seconds < 1800 else 0

#     def vip_charge(self):
#         return 20 if self.seat.seat_type == SeatType.VIP else 0

#     def occupancySurcharge(self):
#         length = self.show.occupany()
#         if length > 80:
#             return 40
#         elif length < 40:
#             return -40
#         return 0

#     def dynamicPriceStargey(self):
#         adjustments = (
#             self.last_minute_surge()
#             + self.early_morning_bird()
#             + self.occupancySurcharge()
#             + self.vip_charge()
#         )
#         return adjustments + self.averagePrice


# class CityFilter:
#     @staticmethod
#     def search(self, city, shows):
#         city = city.lower()
#         matching_shows = []
#         for show in shows:
#             if show.threater.getAddress.lower() == city:
#                 matching_shows.append(show)
#         return matching_shows


# class MovieFilter:
#     @staticmethod
#     def search(self, movieName, shows):
#         movieName = movieName.lower()
#         matching_shows = []
#         for show in shows:
#             if show.movie.getMovieName.lower() == movieName:
#                 matching_shows.append(show)
#         return matching_shows


# class Filter:
#     _search = {
#         "city": CityFilter,
#         "movie": MovieFilter,
#     }

#     @staticmethod
#     def getFilter(fiterValue, value, shows):
#         return Filter._search.get(fiterValue, CityFilter)().search(value, shows)


# import heapq


# class Booking:
#     def __init__(self, booking_id, user, show):
#         self.user = user
#         self.show = show
#         self.selected_seats = []
#         self.status = "CONFIRMED"
#         self.timestamp = datetime.now()
#         self.booking_id = booking_id
#         self.seatsBooked = []

#     def filter(self, shows, filters):
#         f = Filter.getFilter("city", filters.city, shows)
#         f1 = Filter.getFilter("movie", filters.movieName, f)
#         return f1

#     def bookSeats(self, seat_ids):
#         if self.show.seats.total_seats < seat_ids:
#             raise Exception("Seats are less")
#         for seat in self.show.seats:
#             if seat.id in seat_ids and seat.status == Status.AVAILABLE:
#                 seat.hold()
#                 seat.price = Price(self.show, seat).calculate_final_price()
#                 heapq.heappush(
#                     self.seats_booked, (datetime.now() + timedelta(seconds=30), seat.id)
#                 )
#                 self.selected_seats.append(seat)

#     def selfBookCancel(self, id):
#         self.booking.selected_seats = [
#             (expiry, seatId)
#             for (expiry, seatId) in self.booking.selected_seats
#             if seatId != id
#         ]
#         heapq.heapify(self.booking.selected_seats)


# class TTLJobSchedular:
#     def __init__(self, booking):
#         self.interval = 5
#         self.booking = booking

#     def run(self):
#         def check_expiry():
#             while True:
#                 now = datetime.now()
#                 while self.booking.selected_seats:
#                     expriy, seatId = self.booking.selected_seats[0]
#                     if expriy < now:
#                         for seat in self.booking.show.seats:
#                             if seat.id == seatId:
#                                 seat.bookCancelled()
#                                 break
#                         heapq.heappop(self.booking.selected_seats)
#                     else:
#                         break
#                 time.sleep(self.interval)

#         thread = threading.Thread(target=check_expiry)
#         thread.daemon = True
#         thread.start()

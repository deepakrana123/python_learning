# object= states + behaviour + responsibility


# from enum import Enum


# class CarState(Enum):
#     IDLE = 1
#     STARTED = 2
#     MOVING = 3
#     STOPPED = 4

#  this code exposes the state of class which defines no encapuslation

# class ToyCar:
#     def __init__(self):
#         self.state = "IDLE"

#     def car_started(self, state: CarState):
#         if self.state == "IDLE":
#             if self.state != "STARTED":
#                 print("In Idle car cannot move or stopped")
#                 return
#             self.state = state
#         elif self.state == "MOVING":
#             if state == "STARTED" or state == "IDLE":
#                 print("Not Possible")
#                 return
#             self.state = state
#         elif self.state == "STOPPED":
#             if state == "MOVING" or state == "IDLE":
#                 print("Not Possible")
#                 return
#             self.state = state


from enum import Enum


class CarState(Enum):
    IDLE = 1
    STOPPED = 2
    MOVING = 3


class ToyCar:
    def __init__(self):
        self._state = CarState.STOPPED

    def start(self):
        if self._state != CarState.STOPPED:
            raise Exception("Car already in moving state")
        self._state = CarState.IDLE

    def accelerate(self):
        if self._state != CarState.IDLE:
            raise Exception("Car must be started first")

        self._state = CarState.MOVING

    def brake(self):
        if self._state == CarState.IDLE:
            raise Exception("Car is already stopped")
        self._state = CarState.IDLE

    def stop(self):
        if self._state == CarState.MOVING:
            raise Exception("Brake before stoping")
        self._state = CarState.STOPPED


class MusicState(Enum):
    STOPPED = 3
    PlAYING = 2
    PAUSED = 1


class PlayMusic:
    def __init__(self):
        self._music_player_state = MusicState.STOPPED

    def start_song(self):
        if self._music_player_state == MusicState.PlAYING:
            raise Exception("Already playing")
        self._music_player_state = MusicState.PlAYING

    def pause(self):
        if self._music_player_state == MusicState.PlAYING:
            self._music_player_state = MusicState.PAUSED
        else:
            raise Exception("Can only pause while playing")

    def stop(self):
        self._music_player_state = MusicState.STOPPED


import random


class User:
    def __init__(self, name: str, password: str, email: str):
        self._name = name
        self._password = password
        self._email = email

    # user identity should not be discolsed
    def email_for_validation(self):
        return self._email

    def same_identity_to_us(self, other_user):
        return self._email == other_user._email


class UserValidator:
    def __init__(self):
        pass

    def _format_email(self, user):
        return random.randint() > 5

    def validate(self, user: User):
        if self._format_email(user.email_for_validation()):
            raise ValueError("Invalid email")
        return True


class UserRepository:
    def __init__(self):
        self._users = []

    def _save_user_to_db(self, user):
        self._users.append(user)

    def save_user(self, user: User):
        return self._save_user_to_db(user)

    def ensure_user_does_not_exist(self, user: User):
        for stored_user in self._users:
            if stored_user.same_identity_to_us(user):
                raise ValueError("User already exist")


class NotificationChannel:
    def notify(self, user):
        raise NotImplementedError()


class EmailNotification(NotificationChannel):
    def notify(self, user):
        raise Exception("f{user.email} is send to the user")


class SMSNotification(NotificationChannel):
    def notify(self, user):
        raise Exception("f{user.email} is send to the user")


class UserRegistrationService:
    def __init__(self, channels):
        self._user_repo = UserRepository()
        self._channels = channels
        self._user_validation = UserValidator()

    def register(self, user):
        self._user_repo.ensure_user_does_not_exist(user)
        self._user_validation.validate(user)
        self._user_repo.save_user(user)
        for channel in self._channels:
            channel.notify(user)

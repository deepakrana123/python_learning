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


class Email:
    def __init__(self, value: str):
        if "@" not in value:
            raise ValueError("Invalid Email")
        self._value = value

    def value(self):
        return self._value

    def __eq__(self, other):
        return isinstance(other, Email) and self._value == other._value


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
    def __init__(self, user_repo, Email, channels):
        self._user_repo = user_repo
        self._channels = channels
        self._user_validation = Email

    def register(self, user):
        self._user_repo.ensure_user_does_not_exist(user)
        self._user_validation.validate(user)
        self._user_repo.save_user(user)
        for channel in self._channels:
            channel.notify(user)


def build_user_registration_service():
    repo = UserRepository()
    Email = Email()

    channels = [
        EmailNotification(),
        SMSNotification(),
    ]

    return UserRegistrationService(user_repo=repo, Email=Email, channels=channels)


class BankAccount:
    def __init__(self, name: str, accountNumber: str, email: str, mobileNumber: str):
        self._name = name
        self._accountNumber = accountNumber
        self._email = email
        self._mobileNumber = mobileNumber


class BankAccountFactory:
    def create(
        self, name: str, account_number: str, email: str, mobile_number: str
    ) -> Bank:
        if not name:
            raise ValueError("Name empty nahi ho sakta")
        if not account_number:
            raise ValueError("Account Number nahi ho sakta")
        if not email:
            raise ValueError("Email nahi ho sakta")
        if not mobile_number:
            raise ValueError("Mobile nahi hai")
        if len(mobile_number) != 10:
            raise ValueError("Mobile Number nahi ho sakta")
        if "@" not in email:
            raise ValueError("Email galat hai")
        return Bank(name, account_number, email, mobile_number)


class DiscountStrategy:
    def discount(self, amount):
        raise NotImplementedError()


class DicountByCounpon(DiscountStrategy):
    def discount(self, amount):
        print(f"paid {amount} via UPI")


class DiscountByReferral(DiscountStrategy):
    def discount(self, amount):
        print(f"Paid {amount} via card")


class DiscountProcessor:
    def __init__(self, strategy: DiscountStrategy):
        self._strategy = strategy

    def process(self, amount):
        self._strategy.discount(amount)


class PlayerState:
    def play(self, player):
        raise NotImplementedError()

    def pause(self, player):
        raise NotImplementedError()

    def stop(self, player):
        raise NotImplementedError()


class PlayingState(PlayerState):
    def play(self, player):
        print("Already playing")

    def pause(self, player):
        player.state = PausedState()

    def stop(self, player):
        player.state = StoppedState()


class PausedState(PlayerState):
    def play(self, player):
        player.stater = PlayingState()

    def pause(self, player):
        print("Already paused")

    def stop(self, player):
        player.state = StoppedState()


class StoppedState(PlayerState):
    def play(self, player):
        player.stater = PlayingState()

    def pause(self, player):
        player.state = PausedState()
        print("Already paused")

    def stop(self, player):
        print("Already stopped")


class MusicPlayer:
    def __init__(self):
        self.state = StoppedState()

    def play(self):
        self.state.play(self)

    def pause(self):
        self.state.pause(self)

    def stop(self):
        self.state.stop(self)


class Observer:
    def update(self, data):
        pass


class OrderPlacedObserver(Observer):
    def update(self, order_id):
        print(f"Order placed:{order_id}")


class Order:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def place(self):
        for o in self._observers:
            o.update("Order123")


class BankAccount:
    def __init__(self, account_id, email, balance, kyc_done):
        self.account_id = account_id
        self.email = email
        self.balance = balance
        self.kyc_done = kyc_done


class BankAccountValdaition:
    def __init__(self, account_id, email, kyc_done):
        self._account_id = account_id
        self._kyc_done = kyc_done
        self._email = email
        self._balance = 0

    def with_account_id(self, account_id):
        self._account_id = account_id
        return self

    def with_email(self, email):
        if "@" not in email:
            raise ValueError("Invalid Email")
        self._email = email
        return self

    def with_initial_balance(self, balance):
        if balance < 0:
            raise ValueError("Negative balance not allowed")
        self._balance = balance
        return self

    def kyc_compeleted(self):
        self._kyc_done = True
        return self

    def build(self):
        if not self._account_id:
            raise ValueError("Account Id required")
        if not self._email:
            raise ValueError("Email required")
        return BankAccount(self._account_id, self._email, self._balance, self._kyc_done)


class Coffee:
    def cost(self):
        raise NotImplementedError()


class BasicCoffee(Coffee):
    def cost(self):
        return 50


class CoffeeDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee


class MilkDecorator(Coffee):
    def cost(self):
        return self._coffee.cost() + 10


class SugarDecorator(Coffee):
    def cost(self):
        return self._coffee.cost() + 5


class CharacterFlyweight:
    def __init__(self, char, font):
        self.char = char
        self.font = font

    def draw(self, position):
        print(self.char, self.font, position)


class CharacterFactory:
    _cache = {}

    def get(self, char, font):
        key = (char, font)
        if key not in self._cache:
            self._cache[key] = CharacterFlyweight
        return self._cache[key]


class Order:
    def __init__(self, user, items, total):
        self._user = user
        self._items = items
        self._total = total


class OrderBuilder:
    def __init__(self):
        self._user = None
        self._items = []

    def user(self, user):
        self._user = user
        return self

    def add_items(self, item):
        self._items.append(item)
        return self

    def build(self):
        if not self._user:
            raise ValueError("User required")
        if not self._items:
            raise ValueError("At least one items needed")
        total = sum(i.price for i in self._items)
        return Order(self._user, self._items, total)


class Send_Result:
    def __init__(self, success: bool, reason: str = ""):
        self.success = success
        self.reason = reason

    def is_success(self):
        return self.success


class RetryPolicy:
    def __init__(self, max_attempts: int):
        self.max_attempts = max_attempts


class NotificationChannel:
    def notify(self, message, user):
        raise NotImplementedError()


class EmailNotification(NotificationChannel):
    def __init__(self, retry_policy: RetryPolicy):
        self.retry_policy = retry_policy

    def notify(self, message, user) -> Send_Result:
        # raise Exception("f{message} is send to the user")
        attempts = 0
        while attempts < self.retry_policy.max_attempts:
            attempts += 1
            try:
                print(f"SMS attempt {attempts} to {user}")
                return Send_Result(True)
            except Exception:
                continue


class SMSNotification(NotificationChannel):
    def __init__(self, retry_policy: RetryPolicy):
        self.retry_policy = retry_policy

    def notify(self, message, user):
        # raise Exception("f{message} is send to the user")
        # def notify(self, message, user) -> Send_Result:
        # raise Exception("f{message} is send to the user")
        attempts = 0
        while attempts < self.retry_policy.max_attempts:
            attempts += 1
            try:
                print(f"SMS attempt {attempts} to {user}")
                return Send_Result(True)
            except Exception:
                continue


channels = {"SMS": SMSNotification, "EMAIL": EmailNotification}


class NotifcationService:
    def __int__(self, channels: dict[str, NotificationChannel]):
        self._channels = channels

    def _notify(self, message, channelMethod, user):
        channel = self._channels[channelMethod]
        return channel.send(message, user)


class RuleBook:
    def choose_channel(self):
        return ["SMS", "EMAIL"]


class NotificationOrceshator:
    def __init__(self, service: NotifcationService, rulebook: RuleBook):
        self._notification = set()
        self._service = service
        self._rulebook = rulebook

    def notify_user(self, user, message, channel, idempotency):
        if idempotency in self._notification:
            return "Duplicate suppressed"
        channels = self._rulebook.choose_channel(user)
        for channel in channels:
            result = self._service.notify(user, message, channel)
            if result.is_success():
                self._notification.add(idempotency)
                return "Notification send"
        return "All channels failed"

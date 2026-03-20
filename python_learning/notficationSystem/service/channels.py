from abc import ABC, abstractmethod
from domain.models import Notification


class NotificationChannel(ABC):
    @abstractmethod
    def send(self, notification: Notification):
        pass


class SMSChannel(NotificationChannel):
    def send(self, notification: Notification) -> bool:
        print(f"{notification.id}")
        pass


class EmailChannel(NotificationChannel):
    def send(self, notification: Notification) -> bool:
        print(f"{notification.id}")
        return True


class PushChannel(NotificationChannel):
    def send(self, notification: Notification) -> bool:
        print(f"{notification.id}")
        return True

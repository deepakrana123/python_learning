from abc import ABC
from datetime import datetime


class Notification(ABC):
    def __init__(self, notificationId, content):
        self.notificationId = notificationId
        self.content = content
        self.__created_on = datetime.date.today()

    def send_notification(self):
        None


class SmsNotification(Notification):
    def send_notification(self):
        print("through sms")


class MobileNotification(Notification):
    def send_notification(self):
        print("through mobile notfication")


class NotificationService:
    def send_order_notification(self, user, content):
        notifcation = MobileNotification(user, content)
        notifcation.send_notification()
        return notifcation

    def send_sms_notification(self, user, content):
        notifcation = SmsNotification(user, content)
        notifcation.send_notification()
        return notifcation

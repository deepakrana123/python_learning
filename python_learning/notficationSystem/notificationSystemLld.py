from enum import Enum
from typing import List, Dict


class ChannelType(Enum):
    SMS = "sms"
    EMAIL = "email"
    Push = "push"


class Notification:
    def __init__(
        self,
        notfication_id: str,
        user_id: str,
        template_id: str,
        channels: List[ChannelType],
        data: Dict[str, str],
    ):
        self.id = notfication_id
        self.user_id = user_id
        self.template_id = template_id
        self.channels = channels
        self.data = data


from abc import ABC, abstractmethod


class NotificationChannel(ABC):
    @abstractmethod
    def send(self, notification: Notification) -> bool:
        pass


class SMSChannel(NotificationChannel):
    def send(self, notification: Notification):
        print(f"Sending SMS to user {notification.user_id}")
        return True


class EmailChannel(NotificationChannel):
    def send(self, notification: Notification):
        print(f"Sending SMS to user {notification.user_id}")
        return True


class PushChannel(NotificationChannel):
    def send(self, notification: Notification):
        print(f"Sending SMS to user {notification.user_id}")
        return True


class ChannelFactory:
    @staticmethod
    def get_channel(channel_type: ChannelType) -> NotificationChannel:
        if channel_type == ChannelType.SMS:
            return SMSChannel()
        elif channel_type == ChannelType.Push:
            return PushChannel()
        elif channel_type == ChannelType.EMAIL:
            return EmailChannel()
        else:
            raise ValueError("Invalid channel")


class NotficationService:
    def __init__(self, max_retries: 3):
        self.max_retries = max_retries

    def send(self, notfication: Notification):
        for channel_type in notfication:
            channel = ChannelFactory.get_channel(channel_type)
            for _ in range(self.max_retries):
                success = channel.send(notfication)
                if success:
                    return True
            print(f"channel {channel} try for next one or fallback")
        return False

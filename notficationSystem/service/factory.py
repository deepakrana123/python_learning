from domain.models import ChannelType
from python_learning.notficationSystem.service.channelManager import (
    SMSChannel,
    EmailChannel,
    PushChannel,
)


class ChannelFactory:
    @staticmethod
    def send(channel_type: ChannelType, task):
        if channel_type == ChannelType.SMS:
            return SMSChannel(task)
        elif channel_type == ChannelType.EMAIL:
            return EmailChannel(task)
        elif channel_type == ChannelType.PUSH:
            return PushChannel(task)

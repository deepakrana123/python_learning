from domain.models import ChannelType
from service.channels import SMSChannel, EmailChannel, PushChannel


class ChannelFactory:
    @staticmethod
    def get(channel_type: ChannelType):
        if channel_type == ChannelType.SMS:
            return SMSChannel()
        elif channel_type == ChannelType.EMAIL:
            return EmailChannel()
        elif channel_type == ChannelType.PUSH:
            return PushChannel()

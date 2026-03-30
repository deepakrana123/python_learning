from .factory import ChannelFactory


class ChannelManager:
    def __init__(self, channelFactory: ChannelFactory):
        self.channel = channelFactory

    def send(self, task, current_channel):
        return self.channel.send(current_channel, task)

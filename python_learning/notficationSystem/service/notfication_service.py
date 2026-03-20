from service.factory import ChannelFactory


class NotificationService:
    def __init__(self, repo, max_retires):
        self.repo = repo
        self.max_retires = max_retires

    def process(self, task):
        notification = task["notification"]
        if self.repo.exists(notification):
            return
        channel_index = task["channel_index"]
        attempt = task["attempt"]

        if channel_index >= len(notification):
            print("DLQ queue")
            return

        channel_type = notification.channels[channel_index]
        channel = ChannelFactory.get(channel_type)

        success = channel.send(notification)

        if success:
            self.repo.save(notification.id)
            return True

        return False

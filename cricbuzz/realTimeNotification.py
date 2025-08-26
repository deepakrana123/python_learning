class Notification:
    def __init__(
        self, notif_id: str, user_id: str, message: str, notif_type: str, timestamp: str
    ):
        pass


class NotificationBatch:
    def __init__(self, notifications: List[Notification]):
        pass


class INotificationStore:
    def save(self, notification: Notification):
        pass

    def get_recent(self, user_id: str, limit: int = 100):
        pass


class IMessageBroker:
    def publish(self, topic: str, notification):
        pass

    def subscribe(self, topic: str, callback: str):
        pass


class IWebSoketGateway:
    def send(self, user_id: str, notification: Notification):
        pass

    def is_connected(self, user_id: str) -> bool:
        pass


class NotificationIngestionService:
    def __init__(self, broker: IMessageBroker):
        self.broker = broker

    def ingest(self, notification: Notification):
        self.broker.publish("notifications.all", notification)


class NotificationFanoutService:
    def __init__(self, store: INotificationStore, gateway: IWebSocketGateway):
        self.store = store
        self.gateway = gateway

    def on_notification(self, notification: Notification):
        self.store.save(notification)
        if self.gateway.is_connected(notification.user_id):
            self.gateway.send(notification.user_id, notification)


class NotificationSyncService:
    def __init__(self, store: INotificationStore):
        self.store = store

    def get_unread(self, user_id: str) -> List[Notification]:
        return self.store.get_recent(user_id)

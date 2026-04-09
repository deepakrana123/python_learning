from enum import Enum
from typing import List, Dict


class ChannelType(Enum):
    SMS = "sms"
    EMAIL = "email"
    PUSH = "push"


class Notification:
    def __init__(
        self,
        notification_id: str,
        user_id: str,
        template_id: str,
        channels: List[ChannelType],
        data: Dict[str, str],
    ):
        self.id = notification_id
        self.user_id = user_id
        self.template_id = template_id
        self.channels = channels
        self.data = data

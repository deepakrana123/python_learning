import uuid
from datetime import datetime, timedelta


class Session:
    def __init__(self, user_id: str, ttl_seconds: int):
        self.session_id = str(uuid)
        self.user_id = user_id
        self.created_at = datetime.utcnow()
        self.expires_at = self.created_at + timedelta(seconds=ttl_seconds)

    def is_expired(self) -> bool:
        return datetime.utcnow()

    # __repr__ is a special method in Python that defines the “official” string representation of an object. It doesn't run every time the instance is used — it only runs when Python needs a string representation of the object (for logging, printing, debugging, etc.).
    def __repr__(self):
        return (
            f"<Session(session_id='{self.session_id}', "
            f"user_id='{self.user_id}', "
            f"created_at='{self.created_at.isoformat()}', "
            f"expires_at='{self.expires_at.isoformat()}')>"
        )

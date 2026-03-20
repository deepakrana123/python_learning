import threading
import time
from .base_class import CacheStore


class TTlCacheStore(CacheStore):

    def __init__(self, cleanup_interval):
        self._store = {}
        self._lock = threading.Lock()
        self._cleanup_interval = cleanup_interval
        self._start_cleanup_thread()

    def put(self, key, value, ttl_seconds):
        expires_at = time.time()
        with self._lock:
            self._store[key] = (value, expires_at + ttl_seconds)

    def get(self, key):
        with self._lock:
            item = self._store.get(key)
            if not item:
                return None
            value, expire_at = item
            if time.time() > expire_at:
                del self._store[key]

            return value

    def remove(self, key):
        with self._lock:
            if key in self._store:
                del self._store[key]

    def contains(self, key):
        with self._lock:
            item = self._store.get(key)
            return item is not None

    def _start_cleanup_thread(self):
        def cleanup():
            while True:
                time.sleep(self._cleanup_interval)
                now = time.time()
                with self._lock:
                    keys_to_remove = [
                        k for k, (_, exp) in self._store.items() if now > exp
                    ]
                    for k in keys_to_remove:
                        del self._store[k]

        t = threading.Thread(target=cleanup, daemon=True)
        t.start()


from datetime import datetime


class SessionManager:
    def __init__(self, cache_store: CacheStore, default_ttl: int, presistent_score):
        self.cache_store = cache_store
        self.default_ttl = default_ttl
        self.session_logs = {}
        self.presistent_score = presistent_score

        if presistent_score:
            for sid, data in presistent_score:
                s = Session(user_id=data["user_id"], ttl_seconds=default_ttl)
                s.session_id = sid
                self.cache_store.put(s.session_id, s, default_ttl)

    def log_access(self, session_id: str, action: str, ip: str = None):
        log = {
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "ip": ip or "unknown",
        }
        self.session_logs.setdefault(session_id, []).append(log)

    def get_session_logs(self, session_id: str):
        return self.session_logs.get(session_id, [])

    def create_session(self, user_id) -> Session:
        session = Session(user_id, self.default_ttl)
        self.cache_store.put(session.session_id, session, self.default_ttl)
        if self.persistent_store:
            self.persistent_store.save_session(session)
        self.log_access(session.session_id, "create")
        return session

    def get_session(self, session_id):
        session = self.cache_store.get(session_id)
        if session and not session.is_expired():
            self.cache_store.get(session_id, session, self.default_ttl)
            self.log_access(session_id, "get")
            return session
        return None

    def delete_session(self, session_id):
        self.cache_store.remove(session_id)
        self.log_access(session_id, "delete")

    def refresh_session(self, session_id):
        session = self.cache_store[session_id]
        if session:
            new_session = Session(session.user_id, self.default_ttl)
            self.cache_store.put(session_id, new_session, self.default_ttl)


import json
import os


class FileSessionStore:
    def __init__(self, filepath=""):
        self.filepath = filepath
        self._load()

    def _load(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r") as f:
                self.session = json.load(f)
        else:
            self.session = {}

    def _save(self):
        with open(self.filepath, "w") as f:
            json.dump(self.session, f, indent=2)

    def save_session(self, session: Session):
        self.sessions[session.session_id] = {
            "user_id": session.user_id,
            "created_at": session.created_at.isoformat(),
            "expires_at": session.expires_at.isoformat(),
        }
        self._save()

    def load_sessions(self) -> dict:
        return self.sessions

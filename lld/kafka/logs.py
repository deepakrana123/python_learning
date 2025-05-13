import time
from enum import Enum
from datetime import datetime
import json
import threading


class ErrorType(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    DEBUG = "DEBUG"
    CRITICAL = "CRITICAL"


class LogsCollector:
    def __init__(self):
        self.centralMap = {}

    def _add(self, log_id, timestamp, error_type, message, source):
        if log_id in self.centralMap:
            raise Exception("Id already exist")
        else:
            self.centralMap[log_id] = {
                "timestamp": timestamp,
                "error_type": error_type,
                "message": message,
                "source": source,
            }

    def filter_error(self, error_type):
        error_logs = {
            log_id: log
            for log_id, log in self.centralMap.items()
            if log["error_type"] == error_type
        }
        if len(error_logs) > 0:
            return error_logs
        else:
            raise Exception("No logs found for this id")

    def filter_by_time(self, start_time, end_time):
        filtered_logs = {
            log_id: log
            for log_id, log in self.centralMap.items()
            if start_time <= log["timestamp"] <= end_time
        }
        if len(filtered_logs) > 0:
            return filtered_logs
        else:
            raise Exception("No logs found for this id")

    def filter_source(self, source):
        error_logs = {
            log_id: log
            for log_id, log in self.centralMap.items()
            if log["source"] == source
        }
        if len(error_logs) > 0:
            return error_logs
        else:
            raise Exception("No logs found for this id")

    def stroage_disk(self, file_path="logs.json"):
        with open(file_path, "w") as f:
            for log_id, log in self.centralMap.item():
                log_entry = {
                    "log_id": log_id,
                    "timestamp": log["timestamp"],
                    "error_type": log["error_type"],
                    "message": log["message"],
                    "source": log["source"],
                }
                f.write(json.dump(log_entry))
        pass

    def load_from_disk(self, file_path="logs.json"):
        with open(file_path, "r") as f:
            for line in f:
                log_entry = json.load(line.strip())
                log_id = log_entry["log_id"]
                self.centralMap[log_id] = {
                    "timestamp": datetime.fromisoformat(log_entry["timestamp"]),
                    "error_type": ErrorType(log_entry["error_type"]),
                    "message": log_entry["message"],
                    "source": log_entry["source"],
                }

    def _remove_memory(self, tle_minutes):
        now = datetime.now()
        ttl_cutoff = now - timedelta(minutes=tle_minutes)

        # Remove entries older than TLE
        expired_keys = [
            log_id
            for log_id, log in self.centralMap.items()
            if log["timestamp"] < ttl_cutoff
        ]

        for key in expired_keys:
            del self.centralMap[key]

        print(f"[CLEANUP] Removed {len(expired_keys)} expired logs at {now}")

        # Schedule next run
        self._schedule_cleanup(tle_minutes)

    def _schedule_cleanup(self, tle_minutes, interval_seconds=300):
        threading.Timer(interval_seconds, self._remove_memory, [tle_minutes]).start()

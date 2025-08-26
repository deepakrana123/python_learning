# domain models or object model for db


class Match:
    def __init__(self, match_id: str, teams: list, status: bool):
        pass


# scorevent is immutable
class ScoreEvent:
    def __init__(
        self,
        event_id: str,
        match_id: str,
        runs: str,
        wicket: str,
        overleft: str,
        commentary: str,
        timestamp: str,
    ):
        pass


# infrastructure interface for redis,kafka,web socket


class IScoreState:
    def save_match_state(self, match_id: str, state: dict):
        pass

    def get_match_state(self, match_id: str) -> dict:
        pass


class IEventPublisher:
    def publish_event(self, match_id: str, event: ScoreEvent):
        pass


class IClientNotifier:
    def notify_client(self, match_id: str, event: ScoreEvent):
        pass


#  core bussiness logic


class MatchStateService:
    def __init__(self, store: IScoreState, notifier: IClientNotifier):
        self.store = store
        self.notifier = notifier

    def handle_score_event(self, event: ScoreEvent):
        # get score , update orchestor , save and update ,notify client
        pass


class SyncService:
    def __init__(self, store: IScoreState):
        self.store = store

    def get_latest_state(self, match_id):
        return self.store.get_match_state(match_id)


class WebSocketHandler:
    def __init__(self):
        self.connected_clients = {}

    def register_client(self, match_id: str, client_id: str):
        pass

    def send_event(self, match_id: str, score: ScoreEvent):
        pass

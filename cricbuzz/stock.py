from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Tick:
    symbol: str
    price: float
    size: int
    ts: datetime
    seq: int


class ITickStore:
    def save_tick(self, tick: Tick) -> None: ...
    def get_latest(self, symbol: str) -> Tick | None: ...
    def get_history(self, symbol: str, limit: int) -> list[Tick]: ...


class IClientNotifier:
    def push_tick(self, client_id: str, tick: Tick) -> None: ...


class IMarketFeed:
    def subscribe(self, symbols: list[str], callback): ...


class TickIngestService:
    def __init__(self, store: ITickStore, publisher):
        self.store = store
        self.publisher = publisher

    def handle_tick(self, tick: Tick):
        # apply simple validation and ordering (drop older seq)
        last = self.store.get_latest(tick.symbol)
        if last is None or tick.seq > last.seq:
            self.store.save_tick(tick)
            self.publisher.publish_tick(tick)


class TickFanoutService:
    def __init__(self, notifier: IClientNotifier):
        self.notifier = notifier
        # mapping: symbol -> set(client_ids)
        self.subscriptions = {}

    def subscribe(self, client_id: str, symbol: str):
        self.subscriptions.setdefault(symbol, set()).add(client_id)

    def on_tick(self, tick: Tick):
        clients = self.subscriptions.get(tick.symbol, set())
        for cid in clients:
            self.notifier.push_tick(cid, tick)


# Use binary protocol (protobuf) over WS for speed and size.

# For very high throughput, use edge servers and partition by symbol.

# Use sequence numbers to detect out-of-order or missing ticks; provide replay via get_history.

# Consider rate-limiting or sampling for slow clients (send snapshots periodically).

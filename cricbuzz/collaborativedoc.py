from dataclasses import dataclass
from datetime import datetime


@dataclass
class DocMeta:
    doc_id: str
    title: str
    created_by: str
    created_at: str


@dataclass
class DocSnapshot:
    doc_id: str
    content: str
    version: str
    last_updated: datetime


@dataclass
class EditOperation:
    op_id: str
    doc_id: str
    user_id: str
    op_payload: dict
    base_version: int
    timestamp: datetime


class IDocStore:
    def save_snapshot(self, snapshot: DocSnapshot):
        None

    def get_snapshot(self, doc_id: str) -> DocSnapshot:
        None

    def append_opeations(self, op: EditOperation):
        None

    def get_operations_since(self, doc_id: str):
        None


class IConflictResolver:
    def apply_operation(self, snapshot: DocSnapshot):
        None


class IClientNotifier:
    def notify_edit(self, doct_id: str, op: EditOperation):
        None


class DocEditService:
    def __init__(
        self, store: IDocStore, resolver: IConflictResolver, notifier: IClientNotifier
    ):
        self.store = store
        self.resolver = resolver
        self.notifier = notifier

    def submit_edit(self, op: EditOperation):
        # 1. fetch current snapshot/version
        snapshot = self.store.get_snapshot(op.doc_id)
        # 2. resolve/apply (CRDT or OT)
        new_snapshot = self.resolver.apply_operation(snapshot, op)
        # 3. persist op & snapshot
        self.store.append_operation(op)
        self.store.save_snapshot(new_snapshot)
        # 4. notify clients (fan-out)
        self.notifier.notify_edit(op.doc_id, op)


class SyncService:
    def __init__(self, store: IDocStore):
        self.store = store

    def sync(self, doc_id: str, client_version: int):
        snapshot = self.store.get_snapshot(doc_id)
        ops = self.store.get_operations_since(doc_id, client_version)
        return snapshot, ops


# 2. CRDT (Conflict-free Replicated Data Types)
# Idea:
# # Mathematical data structures designed to merge automatically without needing a central server — as long as all operations eventually arrive, all replicas converge to the same state.
# 1. OT (Operational Transformation)
# Idea:
# Instead of sending the whole document, you send operations like “Insert abc at position 5” or “Delete from position 2 to 4”.
# If two people edit at the same time, OT transforms incoming operations based on the local operations that have already been applied — so both clients converge to the same state.

# Example:

# User A: Insert X at position 2

# User B: Insert Y at position 5 (original text length 10)
# If A's operation arrives after B's locally, B transforms their op to "position 6" so the insert still lands correctly.

# Pros:

# Well-suited for centralized servers — server resolves conflicts before broadcasting.

# Mature implementations (Google Docs uses OT).

# Works with sequential document editing.

# Cons:

# Complex transformation logic when you have many operation types.

# Requires central authority for total ordering (server bottleneck).

# Harder to scale in fully decentralized/offline scenarios.

# 2. CRDT (Conflict-free Replicated Data Types)
# Idea:
# Mathematical data structures designed to merge automatically without needing a central server — as long as all operations eventually arrive, all replicas converge to the same state.

# Example:
# In a CRDT text type, each character gets a unique identifier (position + ID). Inserts and deletes are applied in a way that’s commutative, associative, and idempotent — order doesn’t matter.

# Pros:

# Perfect for offline-first apps (Figma, peer-to-peer editors).

# No central transformation logic — any replica can accept edits.

# Easy horizontal scaling — merge logic is built into the data type.

# Cons:

# More metadata overhead (IDs per character).

# Implementation complexity (though libraries exist).

# Slightly higher bandwidth cost than OT.

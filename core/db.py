import os
import json
from typing import Optional, Dict, Any

from sqlalchemy import create_engine, Column, Integer, Boolean, Text
from sqlalchemy.orm import declarative_base, sessionmaker

# Lazy engine/session so the app can run without DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")
_engine = create_engine(DATABASE_URL) if DATABASE_URL else None
SessionLocal = sessionmaker(bind=_engine) if _engine else None
Base = declarative_base()


class StorageState(Base):
    __tablename__ = "storage_state"

    id = Column(Integer, primary_key=True)  # single row: id=1
    group_id = Column(Integer, nullable=True)
    archive_id = Column(Integer, nullable=True)
    forward_enabled = Column(Boolean, nullable=False, default=True)
    whitelist_json = Column(Text, nullable=False, default="[]")
    blacklist_json = Column(Text, nullable=False, default="[]")
    sections_json = Column(Text, nullable=False, default="{}")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "group_id": self.group_id,
            "archive_id": self.archive_id,
            "forward_enabled": bool(self.forward_enabled),
            "whitelist": json.loads(self.whitelist_json or "[]"),
            "blacklist": json.loads(self.blacklist_json or "[]"),
            "sections": json.loads(self.sections_json or "{}"),
        }

    def update_from(self, data: Dict[str, Any]) -> None:
        if "group_id" in data:
            self.group_id = data["group_id"]
        if "archive_id" in data:
            self.archive_id = data["archive_id"]
        if "forward_enabled" in data:
            self.forward_enabled = bool(data["forward_enabled"])
        if "whitelist" in data:
            self.whitelist_json = json.dumps(data["whitelist"])
        if "blacklist" in data:
            self.blacklist_json = json.dumps(data["blacklist"])
        if "sections" in data:
            self.sections_json = json.dumps(data["sections"])


def has_db() -> bool:
    return _engine is not None


def init_db() -> None:
    """
    Create tables and ensure the single StorageState row exists.
    No-op if DATABASE_URL is not set.
    """
    if not has_db():
        return
    Base.metadata.create_all(_engine)
    with SessionLocal() as session:
        state = session.get(StorageState, 1)
        if not state:
            state = StorageState(
                id=1,
                forward_enabled=True,
                whitelist_json="[]",
                blacklist_json="[]",
                sections_json="{}",
            )
            session.add(state)
        session.commit()


def _get_or_create_state(session) -> StorageState:
    state = session.get(StorageState, 1)
    if not state:
        state = StorageState(
            id=1,
            forward_enabled=True,
            whitelist_json="[]",
            blacklist_json="[]",
            sections_json="{}",
        )
        session.add(state)
        session.flush()
    return state


def get_state() -> Dict[str, Any]:
    """
    Return the storage state as a dictionary.
    If DATABASE_URL is not set, returns defaults.
    """
    if not has_db():
        return {
            "group_id": None,
            "archive_id": None,
            "forward_enabled": True,
            "whitelist": [],
            "blacklist": [],
            "sections": {},
        }
    with SessionLocal() as session:
        state = _get_or_create_state(session)
        return state.to_dict()


def update_state(**kwargs) -> None:
    """
    Update fields in the singleton storage state.
    No-op if DATABASE_URL is not set.
    """
    if not has_db():
        return
    with SessionLocal() as session:
        state = _get_or_create_state(session)
        state.update_from(kwargs)
        session.commit()


def get_sections() -> Dict[str, Dict[str, int]]:
    return get_state().get("sections", {})


def save_sections(mapping: Dict[str, Dict[str, int]]) -> None:
    update_state(sections=mapping)
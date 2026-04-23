from pydantic import BaseModel
from typing import Any


class ParseRequest(BaseModel):
    raw_input: str


class ParseResponse(BaseModel):
    success: bool
    source: str | None = None
    score: float | None = None
    data: dict | None = None
    error: Any | None = None

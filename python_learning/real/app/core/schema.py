from pydantic import BaseModel, Field


class DriverLocationEvent(BaseModel):
    driver_id: str
    ride_id: str
    lat: float
    lng: float
    seq: int = Field(..., description="Monotonic sequence number")
    ts: int

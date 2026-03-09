from pydantic import BaseModel
from typing import Optional


class Listing(BaseModel):
    source_name: str
    external_id: str
    url: str
    title: str
    vin: Optional[str] = None
    year: Optional[int] = None
    make: Optional[str] = None
    model: Optional[str] = None
    bid: Optional[float] = None
    buy_now: Optional[float] = None
    end_time: Optional[str] = None
    location: Optional[str] = None
    title_status: Optional[str] = None
    damage: Optional[str] = None
    image_count: Optional[int] = None

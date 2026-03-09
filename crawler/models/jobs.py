from pydantic import BaseModel, HttpUrl
from typing import Optional, Literal


class FetchJob(BaseModel):
    source_name: str
    source_type: Literal["api", "html", "custom"]
    url: HttpUrl
    method: Literal["GET", "POST"] = "GET"
    priority: int = 100
    parser_name: str
    user_site_id: Optional[str] = None
    headers: dict[str, str] = {}
    params: dict[str, str] = {}
    body: Optional[dict] = None

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

@dataclass
class Marker:
    lat: float
    lng: float
    popup: str | None = None
    data: dict[str, Any] = field(default_factory=dict)
    events: dict[str, str] = field(default_factory=dict)
    marker_id: str = field(default_factory=lambda: f"marker-{uuid4().hex}")
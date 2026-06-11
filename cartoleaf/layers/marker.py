from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4
from ..icons.base import CustomIcon
from ..settings import SUPPORTED_EVENTS

SUPPORTED_MARKER_EVENTS = SUPPORTED_EVENTS


@dataclass
class Marker:
    lat: float
    lng: float
    popup: str | None = None
    data: dict[str, Any] = field(default_factory=dict)
    events: dict[str, str] = field(default_factory=dict)
    marker_id: str = field(default_factory=lambda: f"marker-{uuid4().hex}")
    icon: CustomIcon | None = None

    def __post_init__(self):
        if not -90 <= self.lat <= 90:
            raise ValueError("Marker lat must be between -90 and 90.")

        if not -180 <= self.lng <= 180:
            raise ValueError("Marker lng must be between -180 and 180.")

        invalid_events = set(self.events) - SUPPORTED_MARKER_EVENTS

        if invalid_events:
            raise ValueError(
                f"Unsupported marker events: {invalid_events}. "
                f"Supported events are: {SUPPORTED_MARKER_EVENTS}."
            )
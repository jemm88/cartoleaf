from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4
from ..settings import SUPPORTED_EVENTS, POLYGEO_DEFAULT_STYLE


SUPPORTED_CIRCLE_EVENTS = SUPPORTED_EVENTS


@dataclass
class Circle:
    lat: float
    lng: float
    radius: float
    popup: str | None = None
    popup_html: str | None = None

    popup_open_on_hover: bool = False
    popup_close_on_hoverout: bool = False


    data: dict[str, Any] = field(default_factory=dict)
    events: dict[str, str] = field(default_factory=dict)
    circle_id: str = field(default_factory=lambda: f"circle-{uuid4().hex}")

    style: dict[str, Any] = field(default_factory=lambda: POLYGEO_DEFAULT_STYLE)

    def __post_init__(self):
        if not -90 <= self.lat <= 90:
            raise ValueError("Circle lat must be between -90 and 90.")

        if not -180 <= self.lng <= 180:
            raise ValueError("Circle lng must be between -180 and 180.")

        if self.radius <= 0:
            raise ValueError("Circle radius must be greater than 0 meters.")
        
        if self.popup is not None and self.popup_html is not None:
            raise ValueError("Use either popup or popup_html, not both.")

        if self.popup_html is not None and not isinstance(self.popup_html, str):
            raise TypeError("popup_html must be a string.")
        
        invalid_events = set(self.events) - SUPPORTED_CIRCLE_EVENTS

        if invalid_events:
            raise ValueError(
                f"Unsupported circle events: {invalid_events}. "
                f"Supported events are: {SUPPORTED_CIRCLE_EVENTS}."
            )
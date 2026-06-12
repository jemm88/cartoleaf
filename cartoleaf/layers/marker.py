from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4
from ..icons.base import CustomIcon
from ..settings import SUPPORTED_EVENTS
import json

SUPPORTED_MARKER_EVENTS = SUPPORTED_EVENTS

@dataclass
class Marker:
    lat: float
    lng: float
    popup: str | None = None
    popup_html: str | None = None
    popup_options: dict[str, Any] = field(default_factory=dict) #currently unused, reserved for future use

    popup_open_on_hover: bool = False
    popup_close_on_hoverout: bool = False

    data: dict[str, Any] = field(default_factory=dict)
    events: dict[str, str] = field(default_factory=dict)
    marker_id: str = field(default_factory=lambda: f"marker-{uuid4().hex}")
    icon: CustomIcon | None = None

    def __post_init__(self):
        if not -90 <= self.lat <= 90:
            raise ValueError("Marker lat must be between -90 and 90.")

        if not -180 <= self.lng <= 180:
            raise ValueError("Marker lng must be between -180 and 180.")

        if self.popup is not None and self.popup_html is not None:
            raise ValueError("Use either popup or popup_html, not both.")
        
        if self.popup_html is not None and not isinstance(self.popup_html, str):
            raise TypeError("popup_html must be a string.")
        
        if not isinstance(self.popup_options, dict):
            raise TypeError("popup_options must be a dictionary.")
    
        if not isinstance(self.popup_open_on_hover, bool):
            raise TypeError("popup_open_on_hover must be a boolean.")

        if not isinstance(self.popup_close_on_hoverout, bool):
            raise TypeError("popup_close_on_hoverout must be a boolean.")
        
        invalid_events = set(self.events) - SUPPORTED_MARKER_EVENTS

        if invalid_events:
            raise ValueError(
                f"Unsupported marker events: {invalid_events}. "
                f"Supported events are: {SUPPORTED_MARKER_EVENTS}."
            )
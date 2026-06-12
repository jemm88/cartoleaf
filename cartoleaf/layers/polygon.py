from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4
from ..settings import SUPPORTED_EVENTS, POLYGEO_DEFAULT_STYLE

SUPPORTED_POLYGON_EVENTS = SUPPORTED_EVENTS


@dataclass
class Polygon:
    coordinates: list[tuple[float, float]]
    popup: str | None = None
    popup_html: str | None = None
    popup_options: dict[str, Any] = field(default_factory=dict) #currently unused in templating, reserved for future use
    popup_open_on_hover: bool = False
    popup_close_on_hoverout: bool = False

    data: dict[str, Any] = field(default_factory=dict)
    events: dict[str, str] = field(default_factory=dict)
    polygon_id: str = field(default_factory=lambda: f"polygon-{uuid4().hex}")

    style: dict[str, Any] = field(default_factory=lambda: POLYGEO_DEFAULT_STYLE)

    def __post_init__(self):
        if len(self.coordinates) < 3:
            raise ValueError("Polygon requires at least 3 coordinate points.")

        for lat, lng in self.coordinates:
            if not -90 <= lat <= 90:
                raise ValueError("Polygon lat values must be between -90 and 90.")

            if not -180 <= lng <= 180:
                raise ValueError("Polygon lng values must be between -180 and 180.")

        if self.popup is not None and self.popup_html is not None:
            raise ValueError("Use either popup or popup_html, not both.")

        if self.popup_html is not None and not isinstance(self.popup_html, str):
            raise TypeError("popup_html must be a string.")

        invalid_events = set(self.events) - SUPPORTED_POLYGON_EVENTS

        if invalid_events:
            raise ValueError(
                f"Unsupported polygon events: {invalid_events}. "
                f"Supported events are: {SUPPORTED_POLYGON_EVENTS}."
            )
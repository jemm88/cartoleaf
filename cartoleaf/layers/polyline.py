from dataclasses import dataclass, field
from typing import Any
import json
import uuid

@dataclass
class Polyline:
    points: list[tuple[float, float]]
    style: dict[str, Any] = field(default_factory=dict)
    popup: str | None = None
    popup_html: str | None = None
    popup_open_on_hover: bool = False
    popup_close_on_hoverout: bool = False
    events: dict[str, str] = field(default_factory=dict)
    data: dict[str, Any] = field(default_factory=dict)
    polyline_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self):
        if len(self.points) < 2:
            raise ValueError("Polyline requires at least two points.")

        for lat, lng in self.points:
            if not -90 <= lat <= 90:
                raise ValueError("Latitude must be between -90 and 90.")
            if not -180 <= lng <= 180:
                raise ValueError("Longitude must be between -180 and 180.")
            
        if self.popup is not None and self.popup_html is not None:
            raise ValueError("Use either popup or popup_html, not both.")

        if self.popup_html is not None and not isinstance(self.popup_html, str):
            raise TypeError("popup_html must be a string.")
    @property
    def points_json(self):
        return json.dumps(self.points)

    @property
    def style_json(self):
        return json.dumps(self.style)

    @property
    def popup_json(self):
        return json.dumps(self.popup)
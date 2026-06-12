from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4
from ..settings import SUPPORTED_EVENTS, POLYGEO_DEFAULT_STYLE

SUPPORTED_GEOJSON_EVENTS = SUPPORTED_EVENTS


@dataclass
class GeoJson:
    data: dict[str, Any]
    popup_field: str | None = None

    popup_open_on_hover: bool = False
    popup_close_on_hoverout: bool = False

    events: dict[str, str] = field(default_factory=dict)
    geojson_id: str = field(default_factory=lambda: f"geojson-{uuid4().hex}")

    style: dict[str, Any] = field(default_factory=lambda: POLYGEO_DEFAULT_STYLE)

    def __post_init__(self):
        if not isinstance(self.data, dict):
            raise ValueError("GeoJson data must be a dictionary.")

        if self.data.get("type") not in {"Feature", "FeatureCollection"}:
            raise ValueError("GeoJson data must be a GeoJSON Feature or FeatureCollection.")
        
        if self.popup_field is not None and not isinstance(self.popup_field, str):
            raise TypeError("popup_field must be a string.")

        if not isinstance(self.popup_open_on_hover, bool):
            raise TypeError("popup_open_on_hover must be a boolean.")

        if not isinstance(self.popup_close_on_hoverout, bool):
            raise TypeError("popup_close_on_hoverout must be a boolean.")

        invalid_events = set(self.events) - SUPPORTED_GEOJSON_EVENTS

        if invalid_events:
            raise ValueError(
                f"Unsupported GeoJson events: {invalid_events}. "
                f"Supported events are: {SUPPORTED_GEOJSON_EVENTS}."
            )
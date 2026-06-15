from dataclasses import dataclass, field
from typing import Any
import json
import uuid
from ..settings import SUPPORTED_EVENTS, POLYGEO_DEFAULT_STYLE

SUPPORTED_POLYLINE_EVENTS = SUPPORTED_EVENTS

@dataclass
class Polyline:
    """
    Represents a line overlay on a CartoLeaf map.

    Polyline is used to draw a connected path between two or more latitude
    and longitude coordinate points. It is useful for routes, paths, trails,
    boundaries, connections, or movement lines.

    Parameters
    ----------
    points : list[tuple[float, float]]
        List of line points as (lat, lng) tuples. A polyline requires at
        least two coordinate points. Latitude values must be between -90
        and 90. Longitude values must be between -180 and 180.

    style : dict[str, Any], default=POLYGEO_DEFAULT_STYLE
        Leaflet path style options applied to the polyline, such as color,
        opacity, weight, and dashArray.

    popup : str | None, default=None
        Plain text popup content shown when the polyline is clicked.

    popup_html : str | None, default=None
        HTML popup content shown when the polyline is clicked.
        Use either popup or popup_html, not both.

    popup_open_on_hover : bool, default=False
        Whether the popup should open when the cursor enters the polyline.

    popup_close_on_hoverout : bool, default=False
        Whether the popup should close when the cursor leaves the polyline.

    events : dict[str, str], default={}
        Browser events emitted by the polyline. Event keys must be supported
        CartoLeaf events such as click, hoverin, or hoverout.

    data : dict[str, Any], default={}
        Custom metadata attached to the polyline. This is included in emitted
        browser events.

    polyline_id : str, default=auto-generated
        Unique ID for the polyline. If not provided, one is automatically
        generated.

    Raises
    ------
    ValueError
        If fewer than two points are provided, coordinate values are invalid,
        both popup and popup_html are provided, or unsupported events are used.

    TypeError
        If popup_html or hover options are not the expected types.
    """
    points: list[tuple[float, float]]
    style: dict[str, Any] = field(default_factory=lambda: POLYGEO_DEFAULT_STYLE)
    popup: str | None = None
    popup_html: str | None = None
    popup_open_on_hover: bool = False
    popup_close_on_hoverout: bool = False
    events: dict[str, str] = field(default_factory=dict)
    data: dict[str, Any] = field(default_factory=dict)
    polyline_id: str = field(default_factory=lambda: f"polyline-{uuid.uuid4().hex}")

    def __post_init__(self):
        if len(self.points) < 2:
            raise ValueError("Polyline requires at least two points.")

        for lat, lng in self.points:
            if not -90 <= lat <= 90:
                raise ValueError("Polyline lat values must be between -90 and 90.")
            if not -180 <= lng <= 180:
                raise ValueError("Polyline lng values must be between -180 and 180.")

        if self.popup is not None and self.popup_html is not None:
            raise ValueError("Use either popup or popup_html, not both.")

        if self.popup_html is not None and not isinstance(self.popup_html, str):
            raise TypeError("popup_html must be a string.")

        if not isinstance(self.popup_open_on_hover, bool):
            raise TypeError("popup_open_on_hover must be a boolean.")

        if not isinstance(self.popup_close_on_hoverout, bool):
            raise TypeError("popup_close_on_hoverout must be a boolean.")

        invalid_events = set(self.events) - SUPPORTED_POLYLINE_EVENTS

        if invalid_events:
            raise ValueError(
                f"Unsupported polyline events: {invalid_events}. "
                f"Supported events are: {SUPPORTED_POLYLINE_EVENTS}."
            )

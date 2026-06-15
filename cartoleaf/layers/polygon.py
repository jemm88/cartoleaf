from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4
from ..settings import SUPPORTED_EVENTS, POLYGEO_DEFAULT_STYLE

SUPPORTED_POLYGON_EVENTS = SUPPORTED_EVENTS


@dataclass
class Polygon:
    """
    Represents a polygon overlay on a CartoLeaf map.

    Polygon is used to draw a custom area using a list of latitude and
    longitude coordinate pairs. It supports styling, plain text popups,
    HTML popups, hover popup behavior, custom browser events, and custom
    metadata.

    Parameters
    ----------
    coordinates : list[tuple[float, float]]
        List of polygon points as (lat, lng) tuples. A polygon requires at
        least three coordinate points. Latitude values must be between -90
        and 90. Longitude values must be between -180 and 180.

    popup : str | None, default=None
        Plain text popup content shown when the polygon is clicked.

    popup_html : str | None, default=None
        HTML popup content shown when the polygon is clicked.
        Use either popup or popup_html, not both.

    popup_options : dict[str, Any], default={}
        Reserved for future popup configuration support.

    popup_open_on_hover : bool, default=False
        Whether the popup should open when the cursor enters the polygon.

    popup_close_on_hoverout : bool, default=False
        Whether the popup should close when the cursor leaves the polygon.

    data : dict[str, Any], default={}
        Custom metadata attached to the polygon. This is included in emitted
        browser events.

    events : dict[str, str], default={}
        Browser events emitted by the polygon. Event keys must be supported
        CartoLeaf events such as click, hoverin, or hoverout.

    polygon_id : str, default=auto-generated
        Unique ID for the polygon. If not provided, one is automatically
        generated.

    style : dict[str, Any], default=POLYGEO_DEFAULT_STYLE
        Leaflet path style options applied to the polygon, such as color,
        fillColor, fillOpacity, opacity, and weight.

    Raises
    ------
    ValueError
        If fewer than three coordinates are provided, coordinate values are
        invalid, both popup and popup_html are provided, or unsupported events
        are used.

    TypeError
        If popup_html is provided but is not a string.
    """
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
        
        if not isinstance(self.popup_options, dict):
            raise TypeError("popup_options must be a dictionary.")

        if not isinstance(self.popup_open_on_hover, bool):
            raise TypeError("popup_open_on_hover must be a boolean.")

        if not isinstance(self.popup_close_on_hoverout, bool):
            raise TypeError("popup_close_on_hoverout must be a boolean.")

        invalid_events = set(self.events) - SUPPORTED_POLYGON_EVENTS

        if invalid_events:
            raise ValueError(
                f"Unsupported polygon events: {invalid_events}. "
                f"Supported events are: {SUPPORTED_POLYGON_EVENTS}."
            )
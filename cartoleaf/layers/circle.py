from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4
from ..settings import SUPPORTED_EVENTS, POLYGEO_DEFAULT_STYLE


SUPPORTED_CIRCLE_EVENTS = SUPPORTED_EVENTS


@dataclass
class Circle:
    """
    Represents a circular area overlay on a CartoLeaf map.

    Circle is used to draw a radius-based area around a latitude and
    longitude coordinate. The radius is measured in meters, following
    Leaflet's circle behavior.

    Parameters
    ----------
    lat : float
        Latitude of the circle center. Must be between -90 and 90.

    lng : float
        Longitude of the circle center. Must be between -180 and 180.

    radius : float
        Radius of the circle in meters. Must be greater than 0.

    popup : str | None, default=None
        Plain text popup content shown when the circle is clicked.

    popup_html : str | None, default=None
        HTML popup content shown when the circle is clicked.
        Use either popup or popup_html, not both.

    popup_options : dict[str, Any], default={}
        Reserved for future popup configuration support.

    popup_open_on_hover : bool, default=False
        Whether the popup should open when the cursor enters the circle.

    popup_close_on_hoverout : bool, default=False
        Whether the popup should close when the cursor leaves the circle.

    data : dict[str, Any], default={}
        Custom metadata attached to the circle. This is included in emitted
        browser events.

    events : dict[str, str], default={}
        Browser events emitted by the circle. Event keys must be supported
        CartoLeaf events such as click, hoverin, or hoverout.

    circle_id : str, default=auto-generated
        Unique ID for the circle. If not provided, one is automatically
        generated.

    style : dict[str, Any], default=POLYGEO_DEFAULT_STYLE
        Leaflet circle style options, such as color, fillColor, fillOpacity,
        opacity, and weight.

    Raises
    ------
    ValueError
        If lat, lng, radius, popup configuration, or events are invalid.

    TypeError
        If popup_html is provided but is not a string.
    """
    lat: float
    lng: float
    radius: float
    popup: str | None = None
    popup_html: str | None = None
    popup_options: dict[str, Any] = field(default_factory=dict) #currently unused in templating, reserved for future use
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
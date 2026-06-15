from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4
from ..settings import SUPPORTED_EVENTS, POLYGEO_DEFAULT_STYLE

SUPPORTED_GEOJSON_EVENTS = SUPPORTED_EVENTS


@dataclass
class GeoJson:
    """
    Represents a GeoJSON layer on a CartoLeaf map.

    GeoJson is used to render GeoJSON Feature or FeatureCollection data
    as a Leaflet GeoJSON layer. It supports styling, property-based popups,
    hover popup behavior, browser event emission, and custom metadata through
    the underlying GeoJSON properties.

    Parameters
    ----------
    data : dict[str, Any]
        GeoJSON data to render. Must be a dictionary with type "Feature"
        or "FeatureCollection".

    popup_field : str | None, default=None
        Name of the GeoJSON feature property to display as popup content.
        If provided, each feature will use feature.properties[popup_field]
        as its popup value.

    popup_open_on_hover : bool, default=False
        Whether the popup should open when the cursor enters a GeoJSON feature.

    popup_close_on_hoverout : bool, default=False
        Whether the popup should close when the cursor leaves a GeoJSON feature.

    events : dict[str, str], default={}
        Browser events emitted by GeoJSON features. Event keys must be
        supported CartoLeaf events such as click, hoverin, or hoverout.

    geojson_id : str, default=auto-generated
        Unique ID for the GeoJSON layer. If not provided, one is automatically
        generated.

    style : dict[str, Any], default=POLYGEO_DEFAULT_STYLE
        Leaflet path style options applied to the GeoJSON layer, such as color,
        fillColor, fillOpacity, opacity, and weight.

    Raises
    ------
    ValueError
        If data is not a valid GeoJSON Feature or FeatureCollection, or if
        unsupported events are provided.

    TypeError
        If popup_field or hover options are not the expected types.
    """
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
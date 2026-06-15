from dataclasses import dataclass


@dataclass
class CustomIcon:
    """
    Defines a custom Leaflet divIcon for use with CartoLeaf markers.

    CustomIcon is the base icon class used to create marker pins with
    custom HTML, sizing, anchoring, popup positioning, and optional CSS
    classes. It is intended for users who want more control over marker
    appearance than the default Leaflet marker.

    Parameters
    ----------
    html : str
        The HTML content rendered inside the marker icon.

    icon_size : tuple[int, int], default=(33, 33)
        The width and height of the icon in pixels.

    icon_anchor : tuple[int, int], default=(16, 33)
        The pixel coordinate within the icon that is anchored to the map
        location. For a pin-shaped marker, this is usually the bottom
        center point of the icon.

    popup_anchor : tuple[int, int], default=(0, -27)
        The pixel offset from the icon anchor where the popup should open.

    class_name : str, default=""
        Optional CSS class name applied to the Leaflet divIcon container.
        This can be used for custom styling.
    """

    html: str
    icon_size: tuple[int, int] = (33, 33)
    icon_anchor: tuple[int, int] = (16, 33)
    popup_anchor: tuple[int, int] = (0, -27)
    class_name: str = ""
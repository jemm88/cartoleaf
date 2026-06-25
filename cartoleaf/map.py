import json
from pathlib import Path
from jinja2 import Template

from .layers.marker import Marker
from .layers.polygon import Polygon
from .layers.geojson import GeoJson
from .layers.circle import Circle
from .layers.polyline import Polyline

from .templates.dependencies import HTML_DEPENDENCIES
from .templates.container import HTML_MAP
from .templates.script import HTML_SCRIPT
from .templates.emission import HTML_EMISSION


class Map:
    """
    Main CartoLeaf map object.

    Map is the primary entry point for creating and rendering a CartoLeaf map.
    It stores map configuration, manages layers such as markers, polygons,
    circles, polylines, and GeoJSON layers, and renders the final Leaflet HTML.

    Parameters
    ----------
    center : tuple[float, float], default=(1.3521, 103.8198)
        Initial map center as a (lat, lng) tuple.

    zoom : int, default=12
        Initial map zoom level.

    max_zoom : int, default=19
        Maximum zoom level for the tile layer.

    min_zoom : int | None, default=None
        Minimum zoom level the user is allowed to zoom out to. When ``None``
        Leaflet's default (no explicit minimum) is used.

    max_bounds : tuple[tuple[float, float], tuple[float, float]] | None, default=None
        Optional geographic bounds the map cannot be panned outside of, given
        as two ``(lat, lng)`` corners ``((south, west), (north, east))``. This
        prevents, for example, scrolling from Singapore all the way to Tokyo.
        When ``None`` the map can be panned freely.

    max_bounds_viscosity : float, default=1.0
        How solid ``max_bounds`` feels when dragging against it, from ``0.0``
        (no resistance, bounces back) to ``1.0`` (a hard, immovable edge). Only
        applies when ``max_bounds`` is set.

    map_id : str, default="cartoleaf-map"
        HTML element ID used for the map container.

    height : str, default="500px"
        CSS height of the map container.

    fit_bounds : bool, default=False
        Whether the map should automatically fit its bounds to added layers.

    fit_bounds_padding : tuple[int, int], default=(30, 30)
        Padding applied when fitting bounds, as (x, y) pixels.

    allow_multiple_popups : bool, default=False
        Whether multiple popups can remain open at the same time.

    tile_url : str, default=OpenStreetMap tile URL
        Leaflet tile URL template.

    attribution : str, default=OpenStreetMap attribution
        Attribution text shown on the map.

    include_bootstrap_icons : bool, default=False
        Whether to include Bootstrap Icons in the rendered dependencies.

    Attributes
    ----------
    markers : list[Marker]
        Markers added to the map.

    polygons : list[Polygon]
        Polygons added to the map.

    geojson_layers : list[GeoJson]
        GeoJSON layers added to the map.

    circles : list[Circle]
        Circles added to the map.

    polylines : list[Polyline]
        Polylines added to the map.
    """
    def __init__(
        self,
        center: tuple[float, float] = (1.3521, 103.8198),
        zoom: int = 12,
        max_zoom: int = 19,
        min_zoom: int | None = None,
        map_id: str = "cartoleaf-map",
        height: str = "500px",
        fit_bounds: bool = False,
        fit_bounds_padding: tuple[int, int] = (30, 30),
        max_bounds: tuple[tuple[float, float], tuple[float, float]] | None = None,
        max_bounds_viscosity: float = 1.0,
        allow_multiple_popups: bool = False,

        tile_url: str = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        attribution: str = '&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
        include_bootstrap_icons: bool = False,


    ):
        self.center = center
        self.zoom = zoom
        self.max_zoom = max_zoom
        self.min_zoom = min_zoom
        self.map_id = map_id
        self.height = height
        self.fit_bounds = fit_bounds
        self.fit_bounds_padding = fit_bounds_padding
        self.max_bounds = max_bounds
        self.max_bounds_viscosity = max_bounds_viscosity
        self.allow_multiple_popups = allow_multiple_popups
        
        self.tile_url = tile_url
        self.attribution = attribution
        self.include_bootstrap_icons = include_bootstrap_icons
        

        self.markers: list[Marker] = []
        self.polygons: list[Polygon] = []
        self.geojson_layers: list[GeoJson] = []
        self.circles: list[Circle] = []
        self.polylines: list[Polyline] = []


    def add_marker(self, marker: Marker) -> None:
        self.markers.append(marker)

    def add_markers(self, markers: list[Marker]) -> None:
        self.markers.extend(markers)

    def add_polygon(self, polygon: Polygon) -> None:
        self.polygons.append(polygon)

    def add_polygons(self, polygons: list[Polygon]) -> None:
        self.polygons.extend(polygons)

    def add_circle(self, circle: Circle) -> None:
        self.circles.append(circle)

    def add_circles(self, circles: list[Circle]) -> None:
        self.circles.extend(circles)

    def add_geojson(self, geojson: GeoJson) -> None:
        self.geojson_layers.append(geojson)

    def add_geojsons(self, geojson_layers: list[GeoJson]) -> None:
        self.geojson_layers.extend(geojson_layers)

    def add_polyline(self, polyline: Polyline) -> None:
        self.polylines.append(polyline)
    
    def add_polylines(self, polylines: list[Polyline]) -> None:
        self.polylines.extend(polylines)

    @property
    def default_popup_options_json(self) -> str:
        options = {}

        if self.allow_multiple_popups:
            options.update({
                "autoClose": False,
                "closeOnClick": False,
            })

        return json.dumps(options)


    @property
    def map_options_json(self) -> str:
        options = {}

        if self.allow_multiple_popups:
            options["closePopupOnClick"] = False

        if self.min_zoom is not None:
            options["minZoom"] = self.min_zoom

        if self.max_bounds is not None:
            southwest, northeast = self.max_bounds
            options["maxBounds"] = [list(southwest), list(northeast)]
            options["maxBoundsViscosity"] = self.max_bounds_viscosity

        return json.dumps(options)



    def _get_context(self) -> dict:
        prepared_markers = []

        for index, marker in enumerate(self.markers, start=1):
            prepared_marker = {
                "var_name": f"marker{index}",
                "marker_id": marker.marker_id,
                "marker_id_json": json.dumps(marker.marker_id),
                "lat": marker.lat,
                "lng": marker.lng,
                "popup": marker.popup,
                "popup_json": json.dumps(marker.popup),
                "popup_html": marker.popup_html,
                "popup_html_json": json.dumps(marker.popup_html),
                "popup_options_json": json.dumps(marker.popup_options),
                "popup_open_on_hover": marker.popup_open_on_hover,
                "popup_close_on_hoverout": marker.popup_close_on_hoverout,
                "data_json": json.dumps(marker.data),
                "events": marker.events,
                "icon": None,
            }

            if marker.icon:
                prepared_marker["icon"] = {
                    "html_json": json.dumps(marker.icon.html),
                    "icon_size": list(marker.icon.icon_size),
                    "icon_anchor": list(marker.icon.icon_anchor),
                    "popup_anchor": list(marker.icon.popup_anchor),
                    "class_name_json": json.dumps(marker.icon.class_name),
                }

            prepared_markers.append(prepared_marker)



        prepared_polygons = []

        for index, polygon in enumerate(self.polygons, start=1):
            
            new_polygon = {
                "var_name": f"polygon{index}",
                "polygon_id": polygon.polygon_id,
                "polygon_id_json": json.dumps(polygon.polygon_id),
                "coordinates_json": json.dumps(polygon.coordinates),
                "popup": polygon.popup,
                "popup_json": json.dumps(polygon.popup),
                "popup_html": polygon.popup_html,
                "popup_html_json": json.dumps(polygon.popup_html),
                "popup_options_json": json.dumps(polygon.popup_options),
                "popup_open_on_hover": polygon.popup_open_on_hover,
                "popup_close_on_hoverout": polygon.popup_close_on_hoverout,
                "data_json": json.dumps(polygon.data),
                "events": polygon.events,
                "style_json": json.dumps(polygon.style),
                        }
            prepared_polygons.append(new_polygon)



        prepared_circles = []

        for index, circle in enumerate(self.circles, start=1):
            new_circle = {
                "var_name": f"circle{index}",
                "circle_id": circle.circle_id,
                "circle_id_json": json.dumps(circle.circle_id),
                "lat": circle.lat,
                "lng": circle.lng,
                "radius": circle.radius,
                "popup": circle.popup,
                "popup_json": json.dumps(circle.popup),
                "popup_html": circle.popup_html,
                "popup_html_json": json.dumps(circle.popup_html),
                "popup_options_json": json.dumps(circle.popup_options),
                "popup_open_on_hover": circle.popup_open_on_hover,
                "popup_close_on_hoverout": circle.popup_close_on_hoverout,
                "data_json": json.dumps(circle.data),
                "events": circle.events,
                "style_json": json.dumps(circle.style),
            }
            prepared_circles.append(new_circle)


        prepared_polylines = []
        for index, polyline in enumerate(self.polylines, start=1):
            new_polyline = {
                "var_name": f"polyline{index}",
                "polyline_id": polyline.polyline_id,
                "polyline_id_json": json.dumps(polyline.polyline_id),
                "points_json": json.dumps(polyline.points),
                "popup": polyline.popup,
                "popup_json": json.dumps(polyline.popup),
                "popup_html": polyline.popup_html,
                "popup_html_json": json.dumps(polyline.popup_html),
                "popup_open_on_hover": polyline.popup_open_on_hover,
                "popup_close_on_hoverout": polyline.popup_close_on_hoverout,
                "data_json": json.dumps(polyline.data),
                "events": polyline.events,
                "style_json": json.dumps(polyline.style),
            }
            prepared_polylines.append(new_polyline)


        prepared_geojson_layers = []

        for index, geojson in enumerate(self.geojson_layers, start=1):
            new_geojson = {
                "var_name": f"geojsonLayer{index}",
                "geojson_id": geojson.geojson_id,
                "geojson_id_json": json.dumps(geojson.geojson_id),
                "data_json": json.dumps(geojson.data),
                "popup_field": geojson.popup_field,
                "popup_field_json": json.dumps(geojson.popup_field),
                "popup_open_on_hover": geojson.popup_open_on_hover,
                "popup_close_on_hoverout": geojson.popup_close_on_hoverout,
                "events": geojson.events,
                "style_json": json.dumps(geojson.style),
            }
            
            prepared_geojson_layers.append(new_geojson)

    # Main context output
        return {
            "map_id": self.map_id,
            "height": self.height,
            "fit_bounds": self.fit_bounds,
            "fit_bounds_padding": list(self.fit_bounds_padding),
            "center_lat": self.center[0],
            "center_lng": self.center[1],
            "zoom": self.zoom,
            "max_zoom": self.max_zoom,
            "default_popup_options_json":self.default_popup_options_json,
            "map_options_json":self.map_options_json,
            "tile_url": self.tile_url,
            "attribution": json.dumps(self.attribution),
            "markers": prepared_markers,
            "circles": prepared_circles,
            "polygons": prepared_polygons,
            "polylines": prepared_polylines,
            "geojson_layers": prepared_geojson_layers,
            "include_bootstrap_icons": self.include_bootstrap_icons,
        }

    def render_dependencies(self) -> str:
        return Template(HTML_DEPENDENCIES).render(**self._get_context())

    def render_map(self) -> str:
        return Template(HTML_MAP).render(**self._get_context())

    def render_script(self) -> str:
        return Template(HTML_SCRIPT).render(**self._get_context())

    def render_emission(self) -> str:
        return Template(HTML_EMISSION).render(**self._get_context())

    def render(self, split: bool = False) -> str | dict[str, str]:
        parts = {
            "dependencies": self.render_dependencies(),
            "map": self.render_map(),
            "script": self.render_script(),
            "emission": self.render_emission(),
        }

        if split:
            return parts

        return "\n".join(parts.values())
    
    def render_full_html(self, title: str = "Cartoleaf Map") -> str:
        return f"""
            <!DOCTYPE html>
            <html>
            <head>
            <meta charset="utf-8">
            <title>{title}</title>
            {self.render_dependencies()}
            </head>
            <body>
            {self.render_map()}
            {self.render_script()}
            {self.render_emission()}
            </body>
            </html>
            """

    def save(self, path: str | Path, title: str = "CartoLeaf Map") -> None:
        Path(path).write_text(self.render_full_html(title=title), encoding="utf-8")
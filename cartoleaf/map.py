import json
from pathlib import Path
from jinja2 import Template

from .layers.marker import Marker
from .layers.polygon import Polygon
from .layers.geojson import GeoJson
from .layers.circle import Circle

from .templates.dependencies import HTML_DEPENDENCIES
from .templates.container import HTML_MAP
from .templates.script import HTML_SCRIPT
from .templates.emission import HTML_EMISSION


class Map:
    def __init__(
        self,
        center: tuple[float, float] = (1.3521, 103.8198),
        zoom: int = 12,
        map_id: str = "cartoleaf-map",
        height: str = "500px",
        fit_bounds: bool = False,
        fit_bounds_padding: tuple[int, int] = (30, 30),
        
        tile_url: str = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        attribution: str = '&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
        include_bootstrap_icons: bool = False,


    ):
        self.center = center
        self.zoom = zoom
        self.map_id = map_id
        self.height = height
        self.fit_bounds = fit_bounds
        self.fit_bounds_padding = fit_bounds_padding
        self.tile_url = tile_url
        self.attribution = attribution
        self.include_bootstrap_icons = include_bootstrap_icons

        self.markers: list[Marker] = []
        self.polygons: list[Polygon] = []
        self.geojson_layers: list[GeoJson] = []
        self.circles: list[Circle] = []


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
                "data_json": json.dumps(circle.data),
                "events": circle.events,
                "style_json": json.dumps(circle.style),
            }
            prepared_circles.append(new_circle)


        prepared_geojson_layers = []

        for index, geojson in enumerate(self.geojson_layers, start=1):
            new_geojson = {
                "var_name": f"geojsonLayer{index}",
                "geojson_id": geojson.geojson_id,
                "geojson_id_json": json.dumps(geojson.geojson_id),
                "data_json": json.dumps(geojson.data),
                "popup_field": geojson.popup_field,
                "popup_field_json": json.dumps(geojson.popup_field),
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
            "tile_url": self.tile_url,
            "attribution": json.dumps(self.attribution),
            "markers": prepared_markers,
            "circles": prepared_circles,
            "polygons": prepared_polygons,
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

    def save(self, path: str | Path) -> None:
        html = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <meta charset="utf-8">
            <title>Cartoleaf Map</title>
            {self.render_dependencies()}
            </head>
            <body>
            {self.render_map()}

            {self.render_script()}
            {self.render_emission()}
            </body>
            </html>
            """
        Path(path).write_text(html, encoding="utf-8")
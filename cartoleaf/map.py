import json
from pathlib import Path
from jinja2 import Template

from .layers.marker import Marker
from .layers.polygon import Polygon
from .layers.geojson import GeoJson
from .layers.circle import Circle

HTML_DEPENDENCIES = """
<link
  rel="stylesheet"
  href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
{% if include_bootstrap_icons %}
<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css"
/>
{% endif %}
"""


HTML_MAP = """
<div id="{{ map_id }}" style="height: {{ height }};"></div>
"""


HTML_SCRIPT = """
<script>
(function () {
  const map = L.map("{{ map_id }}").setView([{{ center_lat }}, {{ center_lng }}], {{ zoom }});

  L.tileLayer("{{ tile_url }}", {
    maxZoom: 19,
    attribution: {{ attribution | safe }}
  }).addTo(map);

// Initialize global storage for markers, polygons, and geojson layers
window.cartoleaf = window.cartoleaf || {};
window.cartoleaf.markers = window.cartoleaf.markers || {};
window.cartoleaf.circles = window.cartoleaf.circles || {};
window.cartoleaf.polygons = window.cartoleaf.polygons || {};
window.cartoleaf.geojsonLayers = window.cartoleaf.geojsonLayers || {};

//Marker rendering
  {% for marker in markers %}

  {% if marker.icon %}
  const icon{{ loop.index }} = L.divIcon({
    html: {{ marker.icon.html_json | safe }},
    iconSize: {{ marker.icon.icon_size | tojson }},
    iconAnchor: {{ marker.icon.icon_anchor | tojson }},
    popupAnchor: {{ marker.icon.popup_anchor | tojson }},
    className: {{ marker.icon.class_name_json | safe }}
  });

  const {{ marker.var_name }} = L.marker(
    [{{ marker.lat }}, {{ marker.lng }}],
    { icon: icon{{ loop.index }} }
  ).addTo(map);

  {% else %}
  const {{ marker.var_name }} = L.marker([{{ marker.lat }}, {{ marker.lng }}]).addTo(map);
  {% endif %}

  window.cartoleaf.markers[{{ marker.marker_id_json | safe }}] = {{ marker.var_name }};

//Marker popup binding
  {% if marker.popup %}
  {{ marker.var_name }}.bindPopup({{ marker.popup_json | safe }});
  {% endif %}

  {% endfor %}

//Polygon rendering
  {% for polygon in polygons %}
  const {{ polygon.var_name }} = L.polygon(
    {{ polygon.coordinates_json | safe }},
    {{ polygon.style_json | safe }}
  ).addTo(map);

  window.cartoleaf.polygons[{{ polygon.polygon_id_json | safe }}] = {{ polygon.var_name }};

  {% if polygon.popup %}
  {{ polygon.var_name }}.bindPopup({{ polygon.popup_json | safe }});
  {% endif %}

  {% endfor %}

  //GeoJSON rendering
  {% for geojson in geojson_layers %}
  const {{ geojson.var_name }} = L.geoJSON(
    {{ geojson.data_json | safe }},
    {
      style: {{ geojson.style_json | safe }},
      onEachFeature: function (feature, layer) {
        {% if geojson.popup_field %}
        if (feature.properties && feature.properties[{{ geojson.popup_field_json | safe }}]) {
          layer.bindPopup(String(feature.properties[{{ geojson.popup_field_json | safe }}]));
        }
        {% endif %}
      }
    }
  ).addTo(map);

  window.cartoleaf.geojsonLayers[{{ geojson.geojson_id_json | safe }}] = {{ geojson.var_name }};

  {% endfor %}

  
  // Circle rendering
{% for circle in circles %}
const {{ circle.var_name }} = L.circle(
  [{{ circle.lat }}, {{ circle.lng }}],
  {
    radius: {{ circle.radius }},
    ...{{ circle.style_json | safe }}
  }
).addTo(map);

window.cartoleaf.circles[{{ circle.circle_id_json | safe }}] = {{ circle.var_name }};

{% if circle.popup %}
{{ circle.var_name }}.bindPopup({{ circle.popup_json | safe }});
{% endif %}

{% endfor %}


// Fit bounds if enabled
{% if fit_bounds %}
const cartoleafBounds = [];

{% for marker in markers %}
cartoleafBounds.push([{{ marker.lat }}, {{ marker.lng }}]);
{% endfor %}

{% for polygon in polygons %}
cartoleafBounds.push(...{{ polygon.coordinates_json | safe }});
{% endfor %}

{% for circle in circles %}
const circleBounds{{ loop.index }} = {{ circle.var_name }}.getBounds();
if (circleBounds{{ loop.index }}.isValid()) {
  cartoleafBounds.push(circleBounds{{ loop.index }}.getSouthWest());
  cartoleafBounds.push(circleBounds{{ loop.index }}.getNorthEast());
}
{% endfor %}

{% for geojson in geojson_layers %}
try {
  const geojsonBounds{{ loop.index }} = {{ geojson.var_name }}.getBounds();
  if (geojsonBounds{{ loop.index }}.isValid()) {
    cartoleafBounds.push(geojsonBounds{{ loop.index }}.getSouthWest());
    cartoleafBounds.push(geojsonBounds{{ loop.index }}.getNorthEast());
  }
} catch (error) {}
{% endfor %}

if (cartoleafBounds.length > 0) {
  map.fitBounds(cartoleafBounds, {
    padding: {{ fit_bounds_padding | tojson }}
  });
}
{% endif %}

})();
</script>
"""


HTML_EMISSION = """
<script>
(function () {
  const eventAliases = {
    click: "click",
    hoverin: "mouseover",
    hoverout: "mouseout"
  };

  // Utility function to emit custom events with consistent payload structure
  function emitCartoleafEvent(eventName, objectId, eventType, data) {
    document.dispatchEvent(new CustomEvent(eventName, {
      detail: {
        object_id: objectId,
        event_type: eventType,
        data: data
      }
    }));
  }

  // Marker events
  {% for marker in markers %}
  {% set marker_index = loop.index %}
  const markerObj{{ marker_index }} = window.cartoleaf.markers[{{ marker.marker_id_json | safe }}];

  {% for event_name, emitted_event in marker.events.items() %}
  if (eventAliases[{{ event_name | tojson }}]) {
    markerObj{{ marker_index }}.on(
      eventAliases[{{ event_name | tojson }}],
      function (e) {
        {% if event_name == "hoverin" %}
        this.openPopup();
        {% endif %}

        {% if event_name == "hoverout" %}
        this.closePopup();
        {% endif %}

        emitCartoleafEvent(
          {{ emitted_event | tojson }},
          {{ marker.marker_id_json | safe }},
          {{ event_name | tojson }},
          {
            type: "marker",
            id: {{ marker.marker_id_json | safe }},
            lat: {{ marker.lat }},
            lng: {{ marker.lng }},
            data: {{ marker.data_json | safe }}
          }
        );
      }
    );
  }
  {% endfor %}
  {% endfor %}


  // Polygon events
  {% for polygon in polygons %}
  {% set polygon_index = loop.index %}
  const polygonObj{{ polygon_index }} = window.cartoleaf.polygons[{{ polygon.polygon_id_json | safe }}];

  {% for event_name, emitted_event in polygon.events.items() %}
  if (eventAliases[{{ event_name | tojson }}]) {
    polygonObj{{ polygon_index }}.on(
      eventAliases[{{ event_name | tojson }}],
      function (e) {
        {% if event_name == "hoverin" %}
        this.openPopup();
        {% endif %}

        {% if event_name == "hoverout" %}
        this.closePopup();
        {% endif %}

        emitCartoleafEvent(
          {{ emitted_event | tojson }},
          {{ polygon.polygon_id_json | safe }},
          {{ event_name | tojson }},
          {
            type: "polygon",
            id: {{ polygon.polygon_id_json | safe }},
            coordinates: {{ polygon.coordinates_json | safe }},
            data: {{ polygon.data_json | safe }}
          }
        );
      }
    );
  }
  {% endfor %}
  {% endfor %}


  // Circle events
    {% for circle in circles %}
    {% set circle_index = loop.index %}
    const circleObj{{ circle_index }} = window.cartoleaf.circles[{{ circle.circle_id_json | safe }}];

    {% for event_name, emitted_event in circle.events.items() %}
    if (eventAliases[{{ event_name | tojson }}]) {
    circleObj{{ circle_index }}.on(
        eventAliases[{{ event_name | tojson }}],
        function (e) {
        {% if event_name == "hoverin" %}
        this.openPopup();
        {% endif %}

        {% if event_name == "hoverout" %}
        this.closePopup();
        {% endif %}

        emitCartoleafEvent(
            {{ emitted_event | tojson }},
            {{ circle.circle_id_json | safe }},
            {{ event_name | tojson }},
            {
            type: "circle",
            id: {{ circle.circle_id_json | safe }},
            lat: {{ circle.lat }},
            lng: {{ circle.lng }},
            radius: {{ circle.radius }},
            data: {{ circle.data_json | safe }}
            }
        );
        }
    );
    }
    {% endfor %}
    {% endfor %}


  // GeoJSON events
  {% for geojson in geojson_layers %}
  {% set geojson_index = loop.index %}
  const geojsonObj{{ geojson_index }} = window.cartoleaf.geojsonLayers[{{ geojson.geojson_id_json | safe }}];

  {% for event_name, emitted_event in geojson.events.items() %}
  if (eventAliases[{{ event_name | tojson }}]) {
    geojsonObj{{ geojson_index }}.on(
      eventAliases[{{ event_name | tojson }}],
      function (e) {
        const feature = e.layer && e.layer.feature
          ? e.layer.feature
          : null;

        emitCartoleafEvent(
          {{ emitted_event | tojson }},
          {{ geojson.geojson_id_json | safe }},
          {{ event_name | tojson }},
          {
            type: "geojson",
            id: {{ geojson.geojson_id_json | safe }},
            feature: feature
          }
        );
      }
    );
  }
  {% endfor %}
  {% endfor %}
})();
</script>
"""


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
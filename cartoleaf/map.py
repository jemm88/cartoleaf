import json
from pathlib import Path
from jinja2 import Template

from .marker import Marker


HTML_DEPENDENCIES = """
<link
  rel="stylesheet"
  href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
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

  window.cartoleaf = window.cartoleaf || {};
  window.cartoleaf.markers = window.cartoleaf.markers || {};

  {% for marker in markers %}
  const {{ marker.var_name }} = L.marker([{{ marker.lat }}, {{ marker.lng }}]).addTo(map);

  window.cartoleaf.markers[{{ marker.marker_id_json | safe }}] = {{ marker.var_name }};

  {% if marker.popup %}
  {{ marker.var_name }}.bindPopup({{ marker.popup_json | safe }});
  {% endif %}
  {% endfor %}
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

  function emitCartoleafEvent(eventName, markerId, eventType, data) {
    document.dispatchEvent(new CustomEvent(eventName, {
      detail: {
        marker_id: markerId,
        event_type: eventType,
        data: data
      }
    }));
  }

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
          {{ marker.data_json | safe }}
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
        tile_url: str = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        attribution: str = '&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
    ):
        self.center = center
        self.zoom = zoom
        self.map_id = map_id
        self.height = height
        self.tile_url = tile_url
        self.attribution = attribution
        self.markers: list[Marker] = []

    def add_marker(self, marker: Marker) -> None:
        self.markers.append(marker)

    def _get_context(self) -> dict:
        prepared_markers = []

        for index, marker in enumerate(self.markers, start=1):
            prepared_markers.append({
                "var_name": f"marker{index}",
                "marker_id": marker.marker_id,
                "marker_id_json": json.dumps(marker.marker_id),
                "lat": marker.lat,
                "lng": marker.lng,
                "popup": marker.popup,
                "popup_json": json.dumps(marker.popup),
                "data_json": json.dumps(marker.data),
                "events": marker.events,
            })

        return {
            "map_id": self.map_id,
            "height": self.height,
            "center_lat": self.center[0],
            "center_lng": self.center[1],
            "zoom": self.zoom,
            "tile_url": self.tile_url,
            "attribution": json.dumps(self.attribution),
            "markers": prepared_markers,
        }

    def render_dependencies(self) -> str:
        return Template(HTML_DEPENDENCIES).render()

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
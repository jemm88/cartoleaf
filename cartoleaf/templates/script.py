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


HTML_SCRIPT = """
<script>
(function () {

// Initialize global storage for maps, markers, polygons, and geojson layers
window.cartoleaf = window.cartoleaf || {};
window.cartoleaf.maps = window.cartoleaf.maps || {};
window.cartoleaf.markers = window.cartoleaf.markers || {};
window.cartoleaf.circles = window.cartoleaf.circles || {};
window.cartoleaf.polygons = window.cartoleaf.polygons || {};
window.cartoleaf.geojsonLayers = window.cartoleaf.geojsonLayers || {};
window.cartoleaf.polylines = window.cartoleaf.polylines || {};

  const cartoleafMapId = "{{ map_id }}";

  // Remove a previously-rendered map and prune all of its layer references from
  // the global registries, so nothing leaks once it (and its layers) are gone.
  function cartoleafDestroyMap(deadMap) {
    for (const id in (deadMap.markers || {})) { delete window.cartoleaf.markers[id]; }
    for (const id in (deadMap.circles || {})) { delete window.cartoleaf.circles[id]; }
    for (const id in (deadMap.polygons || {})) { delete window.cartoleaf.polygons[id]; }
    for (const id in (deadMap.polylines || {})) { delete window.cartoleaf.polylines[id]; }
    for (const id in (deadMap.geojsonLayers || {})) { delete window.cartoleaf.geojsonLayers[id]; }
    // The container may already be detached (e.g. an htmx swap removed it), in
    // which case remove() can throw — never let that abort the new map build.
    try { deadMap.remove(); } catch (cartoleafRemoveError) {}
  }

  // If a map was previously rendered under this same id, tear it down first so a
  // new one can be created safely on the same container (a stable-id re-render).
  if (window.cartoleaf.maps[cartoleafMapId]) {
    cartoleafDestroyMap(window.cartoleaf.maps[cartoleafMapId]);
    delete window.cartoleaf.maps[cartoleafMapId];
  }

  const map = L.map(cartoleafMapId, {{ map_options_json | safe }}).setView([{{ center_lat }}, {{ center_lng }}], {{ zoom }});

  // Expose the map and give it its own per-map layer registries so the layers it
  // owns can be looked up (and pruned on teardown) independently of other maps
  // sharing the same global registries.
  window.cartoleaf.maps[cartoleafMapId] = map;
  map.markers = {};
  map.circles = {};
  map.polygons = {};
  map.polylines = {};
  map.geojsonLayers = {};

  // Prune any previously-rendered maps whose container has since been removed
  // from the document (for example replaced by an htmx swap). This frees the
  // dead Leaflet instances and keeps the registry from growing without bound
  // when maps are rendered with unique ids — the recommended pattern for swaps,
  // since reusing one id across an htmx swap can race the old/new containers.
  for (const cartoleafOtherId in window.cartoleaf.maps) {
    const cartoleafOther = window.cartoleaf.maps[cartoleafOtherId];
    if (cartoleafOther && cartoleafOther !== map &&
        (!cartoleafOther._container || !document.body.contains(cartoleafOther._container))) {
      cartoleafDestroyMap(cartoleafOther);
      delete window.cartoleaf.maps[cartoleafOtherId];
    }
  }

  const cartoleafDefaultPopupOptions = {{ default_popup_options_json | safe }};

  L.tileLayer("{{ tile_url }}", {
    maxZoom: {{ max_zoom }},
    attribution: {{ attribution | safe }}
  }).addTo(map);

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
  map.markers[{{ marker.marker_id_json | safe }}] = {{ marker.var_name }};

  //Marker popup binding
    {% if marker.popup_html %}
    {{ marker.var_name }}.bindPopup(
      {{ marker.popup_html_json | safe }},
  {
    ...cartoleafDefaultPopupOptions,
    ...{{ marker.popup_options_json | safe }}
  }
    );
    {% elif marker.popup %}
    {{ marker.var_name }}.bindPopup(
      {{ marker.popup_json | safe }},
  {
    ...cartoleafDefaultPopupOptions,
    ...{{ marker.popup_options_json | safe }}
  }
    );
    {% endif %}

  // Marker popup hover behavior
    {% if marker.popup or marker.popup_html %}
      {% if marker.popup_open_on_hover %}
      {{ marker.var_name }}.on("mouseover", function () {
        this.openPopup();
      });
      {% endif %}

      {% if marker.popup_close_on_hoverout %}
      {{ marker.var_name }}.on("mouseout", function () {
        this.closePopup();
      });
      {% endif %}
    {% endif %}


  //Ending Marker rendering loop
  {% endfor %}
  

//Polygon rendering
  {% for polygon in polygons %}
  const {{ polygon.var_name }} = L.polygon(
    {{ polygon.coordinates_json | safe }},
    {{ polygon.style_json | safe }}
  ).addTo(map);

  window.cartoleaf.polygons[{{ polygon.polygon_id_json | safe }}] = {{ polygon.var_name }};
  map.polygons[{{ polygon.polygon_id_json | safe }}] = {{ polygon.var_name }};

  //Polygon popup binding
    {% if polygon.popup_html %}
    {{ polygon.var_name }}.bindPopup(
      {{ polygon.popup_html_json | safe }},
  {
    ...cartoleafDefaultPopupOptions,
    ...{{ polygon.popup_options_json | safe }}
  }
    );
    {% elif polygon.popup %}
    {{ polygon.var_name }}.bindPopup(
      {{ polygon.popup_json | safe }},
  {
    ...cartoleafDefaultPopupOptions,
    ...{{ polygon.popup_options_json | safe }}
  }
    );
    {% endif %}

  // polygon popup hover behavior
    {% if polygon.popup or polygon.popup_html %}
      {% if polygon.popup_open_on_hover %}
      {{ polygon.var_name }}.on("mouseover", function () {
        this.openPopup();
      });
      {% endif %}

      {% if polygon.popup_close_on_hoverout %}
      {{ polygon.var_name }}.on("mouseout", function () {
        this.closePopup();
      });
      {% endif %}
    {% endif %}

  {% endfor %}


// Polyline rendering
{% for polyline in polylines %}
const polyline{{ loop.index }} = L.polyline(
  {{ polyline.points_json | safe }},
  {{ polyline.style_json | safe }}
).addTo(map);

{% if polyline.popup %}
polyline{{ loop.index }}.bindPopup({{ polyline.popup_json | safe }});
{% endif %}

{% if polyline.popup_html %}
polyline{{ loop.index }}.bindPopup({{ polyline.popup_html_json | safe }});
{% endif %}

{% if polyline.popup or polyline.popup_html %}
  {% if polyline.popup_open_on_hover %}
  polyline{{ loop.index }}.on("mouseover", function () {
    this.openPopup();
  });
  {% endif %}

  {% if polyline.popup_close_on_hoverout %}
  polyline{{ loop.index }}.on("mouseout", function () {
    this.closePopup();
  });
  {% endif %}
{% endif %}

window.cartoleaf.polylines[{{ polyline.polyline_id_json | safe }}] = polyline{{ loop.index }};
map.polylines[{{ polyline.polyline_id_json | safe }}] = polyline{{ loop.index }};
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
        layer.bindPopup(
          String(feature.properties[{{ geojson.popup_field_json | safe }}]),
          {
            ...cartoleafDefaultPopupOptions
          }
        );
      }
      {% endif %}

      {% if geojson.popup_field %}
        {% if geojson.popup_open_on_hover %}
        layer.on("mouseover", function () {
          this.openPopup();
        });
        {% endif %}

        {% if geojson.popup_close_on_hoverout %}
        layer.on("mouseout", function () {
          this.closePopup();
        });
        {% endif %}
      {% endif %}

    }
  }
).addTo(map);

window.cartoleaf.geojsonLayers[{{ geojson.geojson_id_json | safe }}] = {{ geojson.var_name }};
map.geojsonLayers[{{ geojson.geojson_id_json | safe }}] = {{ geojson.var_name }};

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
map.circles[{{ circle.circle_id_json | safe }}] = {{ circle.var_name }};

  //circle popup binding
    {% if circle.popup_html %}
    {{ circle.var_name }}.bindPopup(
      {{ circle.popup_html_json | safe }},
  {
    ...cartoleafDefaultPopupOptions,
    ...{{ circle.popup_options_json | safe }}
  }
    );
    {% elif circle.popup %}
    {{ circle.var_name }}.bindPopup(
      {{ circle.popup_json | safe }},
  {
    ...cartoleafDefaultPopupOptions,
    ...{{ circle.popup_options_json | safe }}
  }
    );
    {% endif %}

  // circle popup hover behavior
    {% if circle.popup or circle.popup_html %}
      {% if circle.popup_open_on_hover %}
      {{ circle.var_name }}.on("mouseover", function () {
        this.openPopup();
      });
      {% endif %}

      {% if circle.popup_close_on_hoverout %}
      {{ circle.var_name }}.on("mouseout", function () {
        this.closePopup();
      });
      {% endif %}
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

  // Recalculate the map size once the container has settled in the DOM. When the
  // map is initialized into a container that was just inserted or resized (for
  // example on an htmx swap), Leaflet may cache an incorrect size, leaving tiles
  // and overlays misaligned. invalidateSize() recomputes it and repositions
  // everything. Deferred to the next frame so layout is final when it runs.
  if (typeof requestAnimationFrame === "function") {
    requestAnimationFrame(function () { map.invalidateSize(false); });
  } else {
    setTimeout(function () { map.invalidateSize(false); }, 0);
  }

})();
</script>
"""


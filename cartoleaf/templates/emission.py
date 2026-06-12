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

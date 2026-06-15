# Events

CartoLeaf layers can emit browser events when users interact with them.

This allows a Python-generated map to communicate with the surrounding page. For example, clicking a marker can update a sidebar, highlight a table row, filter a list, or trigger custom frontend logic.

## Overview

Events are configured using the `events` parameter on supported layer objects.

```python
Marker(
    lat=1.3521,
    lng=103.8198,
    popup="Clickable marker",
    events={
        "click": "marker-clicked",
    },
)
```

This means:

```text
When the marker is clicked, CartoLeaf emits a browser event named "marker-clicked".
```

You can then listen for that event in JavaScript:

```html
<script>
window.addEventListener("marker-clicked", function (event) {
  console.log(event.detail);
});
</script>
```

## Supported Event Aliases

CartoLeaf uses simple event aliases that map to Leaflet browser events.

| CartoLeaf Event | Leaflet Event | Description                                 |
| --------------- | ------------- | ------------------------------------------- |
| `click`         | `click`       | Triggered when the layer is clicked.        |
| `hoverin`       | `mouseover`   | Triggered when the cursor enters the layer. |
| `hoverout`      | `mouseout`    | Triggered when the cursor leaves the layer. |

## Supported Layers

Events are supported on:

* `Marker`
* `Circle`
* `Polygon`
* `Polyline`
* `GeoJson`

## Basic Marker Event

```python
from cartoleaf import Map, Marker

m = Map(
    center=(1.3521, 103.8198),
    zoom=12,
)

m.add_marker(
    Marker(
        lat=1.3521,
        lng=103.8198,
        popup="Singapore",
        data={
            "name": "Singapore",
            "type": "city",
        },
        events={
            "click": "marker-clicked",
        },
    )
)

m.save("map.html")
```

Listen for the event in the browser:

```html
<script>
window.addEventListener("marker-clicked", function (event) {
  console.log(event.detail);
});
</script>
```

## Event Detail

When CartoLeaf emits an event, it includes a `detail` payload.

For most layers, the event detail includes:

| Field        | Description                                                          |
| ------------ | -------------------------------------------------------------------- |
| `id`         | The layer ID, such as `marker_id`, `circle_id`, or `polygon_id`.     |
| `event_type` | The CartoLeaf event type, such as `click`, `hoverin`, or `hoverout`. |
| `data`       | Custom metadata passed through the layer's `data` parameter.         |

Example:

```python
Marker(
    lat=1.3521,
    lng=103.8198,
    data={
        "name": "Singapore",
        "category": "city",
    },
    events={
        "click": "marker-clicked",
    },
)
```

JavaScript listener:

```html
<script>
window.addEventListener("marker-clicked", function (event) {
  console.log(event.detail.id);
  console.log(event.detail.event_type);
  console.log(event.detail.data);
});
</script>
```

## Using Custom Data

The `data` parameter is useful for passing application-specific information to the browser.

```python
Marker(
    lat=1.3521,
    lng=103.8198,
    popup="Singapore",
    data={
        "name": "Singapore",
        "region": "Central",
        "population_group": "city",
    },
    events={
        "click": "location-selected",
    },
)
```

In the browser:

```html
<script>
window.addEventListener("location-selected", function (event) {
  const data = event.detail.data;

  console.log("Selected:", data.name);
  console.log("Region:", data.region);
});
</script>
```

## Hover Events

Use `hoverin` and `hoverout` for mouse hover interactions.

```python
Marker(
    lat=1.3521,
    lng=103.8198,
    popup="Hover marker",
    data={
        "name": "Singapore",
    },
    events={
        "hoverin": "marker-hover-in",
        "hoverout": "marker-hover-out",
    },
)
```

In the browser:

```html
<script>
window.addEventListener("marker-hover-in", function (event) {
  console.log("Hover in:", event.detail);
});

window.addEventListener("marker-hover-out", function (event) {
  console.log("Hover out:", event.detail);
});
</script>
```

## Events with Circles

```python
from cartoleaf import Circle

Circle(
    lat=1.3521,
    lng=103.8198,
    radius=500,
    popup="500m radius",
    data={
        "name": "Coverage Area",
        "radius_m": 500,
    },
    events={
        "click": "circle-clicked",
    },
)
```

## Events with Polygons

```python
from cartoleaf import Polygon

Polygon(
    coordinates=[
        (1.35, 103.81),
        (1.36, 103.82),
        (1.34, 103.83),
    ],
    popup="Sample polygon",
    data={
        "name": "Sample Area",
        "type": "zone",
    },
    events={
        "click": "polygon-clicked",
    },
)
```

## Events with Polylines

```python
from cartoleaf import Polyline

Polyline(
    points=[
        (1.3521, 103.8198),
        (1.3000, 103.8500),
    ],
    popup="Sample route",
    data={
        "name": "Route A",
        "type": "walking-route",
    },
    events={
        "click": "polyline-clicked",
    },
)
```

## Events with GeoJSON

GeoJSON events are emitted from individual GeoJSON features.

```python
from cartoleaf import GeoJson

GeoJson(
    data=geojson_data,
    popup_field="name",
    events={
        "click": "geojson-clicked",
    },
)
```

In the browser:

```html
<script>
window.addEventListener("geojson-clicked", function (event) {
  console.log(event.detail);
});
</script>
```

For GeoJSON layers, the event detail includes information from the interacted feature.

## Practical Example: Updating a Sidebar

CartoLeaf events can be used to connect map interactions to other DOM elements.

```python
m.add_marker(
    Marker(
        lat=1.3521,
        lng=103.8198,
        popup="Singapore",
        data={
            "name": "Singapore",
            "description": "Selected location",
        },
        events={
            "click": "location-selected",
        },
    )
)
```

Example HTML:

```html
<div id="sidebar">
  <h2 id="location-name">No location selected</h2>
  <p id="location-description"></p>
</div>

<script>
window.addEventListener("location-selected", function (event) {
  const data = event.detail.data;

  document.getElementById("location-name").textContent = data.name;
  document.getElementById("location-description").textContent = data.description;
});
</script>
```

When the marker is clicked, the sidebar updates using the marker's custom `data`.

## Event Names

Event names are user-defined strings.

```python
events={
    "click": "my-custom-event-name",
}
```

Use names that are descriptive and unlikely to conflict with other browser events.

Recommended examples:

```python
events={
    "click": "marker-selected",
}
```

```python
events={
    "click": "location-clicked",
}
```

```python
events={
    "hoverin": "area-hovered",
    "hoverout": "area-unhovered",
}
```

## Notes

* Event keys must be supported CartoLeaf event aliases.
* Event values are the browser event names that CartoLeaf will emit.
* Custom data should be JSON-serializable.
* Use `window.addEventListener()` or `document.addEventListener()` to listen for emitted events.
* Events are useful when the map needs to interact with tables, sidebars, filters, charts, cards, or other frontend components.

## Next Steps

Continue with:

* [Rendering](rendering.md)
* [Markers](markers.md)
* [Layer Styling](layer-styling.md)
* [Map](map.md)

# CartoLeaf

CartoLeaf is a lightweight Python library for generating interactive Leaflet.js maps from Python.

It is designed for developers who want the convenience of defining maps in Python, while still keeping the generated map as part of the surrounding web page DOM. This makes it easier to integrate Leaflet maps into dashboards, static pages, server-rendered apps, and custom frontend workflows.

Unlike tools that render maps inside an iframe, CartoLeaf generates HTML and JavaScript that can interact directly with the page. Map objects can emit browser events, expose layer references, and communicate with other DOM elements.

[![PyPI version](https://img.shields.io/pypi/v/cartoleaf.svg)](https://pypi.org/project/cartoleaf/)
[![Python versions](https://img.shields.io/pypi/pyversions/cartoleaf.svg)](https://pypi.org/project/cartoleaf/)
[![License](https://img.shields.io/pypi/l/cartoleaf.svg)](https://pypi.org/project/cartoleaf/)

## Why CartoLeaf?

CartoLeaf is built for cases where you want more control over how a Python-generated map interacts with the rest of your web application.

It is useful when you want to:

* Generate interactive Leaflet.js maps from Python
* Avoid writing repetitive Leaflet JavaScript by hand
* Keep the map directly accessible in the page DOM
* Emit browser events from map objects
* Connect map interactions to other frontend components
* Add simple maps to dashboards, static pages, server-rendered apps, and custom frontend workflows
* Render markers, circles, polygons, polylines, and GeoJSON layers with minimal setup

CartoLeaf is not intended to replace full GIS tools. It is designed as a lightweight bridge between Python and Leaflet.js for practical web map generation.

## Features

* Generate interactive Leaflet maps from Python
* Render maps directly into the page instead of an iframe
* Add markers, circles, polygons, polylines, and GeoJSON layers
* Add text or HTML popups
* Customize map layer styles
* Support click and hover interactions
* Emit browser `CustomEvent` events from map objects
* Store Leaflet layer references on `window.cartoleaf`
* Integrate map interactions with the surrounding DOM
* Lightweight and dependency-minimal
* Works well with static HTML, server-rendered apps, dashboards, and custom frontend workflows


## Installation

```bash
pip install cartoleaf
```

For local development:

```bash
git clone https://github.com/your-username/cartoleaf.git
cd cartoleaf
pip install -e .
```

## Quick Start

```python
from cartoleaf import Map, Marker, Circle, Polygon, Polyline

m = Map(
    center=(1.3521, 103.8198),
    zoom=12,
)

m.add_marker(
    Marker(
        lat=1.3521,
        lng=103.8198,
        popup="Singapore"
    )
)

m.add_circle(
    Circle(
        lat=1.3521,
        lng=103.8198,
        radius=500,
        popup="500m radius",
        style={
            "color": "#2879e4",
            "fillColor": "#2879e4",
            "fillOpacity": 0.2,
        },
    )
)

m.add_polyline(
    Polyline(
        points=[
            (1.3521, 103.8198),
            (1.3000, 103.8500),
        ],
        popup="Sample route",
        style={
            "color": "#2879e4",
            "weight": 4,
            "opacity": 0.8,
        },
    )
)

m.save("map.html")
```

Open `map.html` in your browser to view the generated map.

## Basic Usage

### Create a Map

```python
from cartoleaf import Map

m = Map(
    center=(1.3521, 103.8198),
    zoom=12,
    height="600px",
)
```

### Add a Marker

```python
from cartoleaf import Marker

m.add_marker(
    Marker(
        lat=1.3521,
        lng=103.8198,
        popup="Singapore"
    )
)
```

### Add a Circle

```python
from cartoleaf import Circle

m.add_circle(
    Circle(
        lat=1.3521,
        lng=103.8198,
        radius=500,
        popup="500m radius",
        style={
            "color": "blue",
            "fillColor": "blue",
            "fillOpacity": 0.2,
        },
    )
)
```

### Add a Polygon

```python
from cartoleaf import Polygon

m.add_polygon(
    Polygon(
        coordinates=[
            (1.35, 103.81),
            (1.36, 103.82),
            (1.34, 103.83),
        ],
        popup="Sample polygon",
        style={
            "color": "green",
            "fillOpacity": 0.3,
        },
    )
)
```

### Add a Polyline

```python
from cartoleaf import Polyline

m.add_polyline(
    Polyline(
        points=[
            (1.3521, 103.8198),
            (1.3000, 103.8500),
            (1.2800, 103.8600),
        ],
        popup="Sample path",
        style={
            "color": "#2879e4",
            "weight": 4,
        },
    )
)
```

### Add GeoJSON

```python
from cartoleaf import GeoJson

geojson_data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {
                "name": "Sample Area"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [103.81, 1.35],
                    [103.82, 1.36],
                    [103.83, 1.34],
                    [103.81, 1.35],
                ]]
            }
        }
    ]
}

m.add_geojson(
    GeoJson(
        data=geojson_data,
        popup_field="name",
        style={
            "color": "purple",
            "fillOpacity": 0.2,
        },
    )
)
```

## DOM Interaction and Browser Events

CartoLeaf is designed to make map interactions available to the surrounding page.

Map objects can emit browser events that other JavaScript code can listen for.

```python
m.add_marker(
    Marker(
        lat=1.3521,
        lng=103.8198,
        popup="Clickable marker",
        events={
            "click": "marker_clicked"
        },
        data={
            "name": "Singapore"
        }
    )
)
```

Listen for the event in the browser:

```html
<script>
window.addEventListener("marker_clicked", function (e) {
  console.log("Marker clicked:", e.detail);
});
</script>
```

This allows you to connect map interactions to other UI elements, such as tables, cards, filters, sidebars, charts, or custom application logic.

Supported event aliases include:

```python
{
    "click": "click",
    "hoverin": "mouseover",
    "hoverout": "mouseout",
}
```

## Leaflet Layer References

CartoLeaf stores generated Leaflet objects on `window.cartoleaf`, making them accessible from normal browser JavaScript.

Examples:

```javascript
window.cartoleaf.markers
window.cartoleaf.circles
window.cartoleaf.polygons
window.cartoleaf.polylines
window.cartoleaf.geojsonLayers
```

This makes it possible to inspect or interact with generated Leaflet layers after the map has rendered.

## Popups

CartoLeaf supports both plain text popups and HTML popups.

### Text Popup

```python
Marker(
    lat=1.3521,
    lng=103.8198,
    popup="Singapore"
)
```

### HTML Popup

```python
Marker(
    lat=1.3521,
    lng=103.8198,
    popup_html="<strong>Singapore</strong><br>Central location"
)
```

Use either `popup` or `popup_html`, not both.

## Hover Popups

You can configure popups to open on hover and close when the cursor leaves the object.

```python
Marker(
    lat=1.3521,
    lng=103.8198,
    popup="Hover popup",
    popup_open_on_hover=True,
    popup_close_on_hoverout=True,
)
```

This pattern is also supported for other supported map layers.

## Styling

Layer styles are passed as dictionaries and mapped to Leaflet style options.

```python
Polygon(
    coordinates=[
        (1.35, 103.81),
        (1.36, 103.82),
        (1.34, 103.83),
    ],
    style={
        "color": "#2879e4",
        "weight": 3,
        "opacity": 0.9,
        "fillColor": "#2879e4",
        "fillOpacity": 0.25,
    },
)
```

Common style options include:

```python
{
    "color": "#2879e4",
    "weight": 3,
    "opacity": 0.8,
    "fillColor": "#2879e4",
    "fillOpacity": 0.2,
}
```

## Server-rendered Example via Flask

Using Cartoleaf inside a Flask app.

```python
from flask import Flask, render_template_string
from cartoleaf import Map, Marker

app = Flask(__name__)

@app.route("/")
def index():
    m = Map(
        center=(1.3521, 103.8198),
        zoom=12,
    )

    m.add_marker(
        Marker(
            lat=1.3521,
            lng=103.8198,
            popup="Singapore"
        )
    )

    return render_template_string(m.render())

if __name__ == "__main__":
    app.run(debug=True)
```

## Coordinate Format

CartoLeaf uses the standard latitude/longitude format:

```python
(lat, lng)
```

Example:

```python
(1.3521, 103.8198)
```

Latitude must be between `-90` and `90`.

Longitude must be between `-180` and `180`.

## Supported Layers

| Layer      | Description                                  |
| ---------- | -------------------------------------------- |
| `Marker`   | A point marker on the map                    |
| `Circle`   | A circular area with a radius in meters      |
| `Polygon`  | A closed shape made from multiple points     |
| `Polyline` | A connected line made from multiple points   |
| `GeoJson`  | A GeoJSON Feature or FeatureCollection layer |

## CartoLeaf vs iframe-based map output

CartoLeaf is designed for situations where the map should be part of the page, not isolated from it.

This is useful when you want map interactions to affect other DOM elements, or when other frontend components need to interact with map layers.

Instead of treating the map as a self-contained iframe, CartoLeaf aims to generate Leaflet output that can participate in the rest of your application.

## Roadmap


1. Additional tile provider options
2. Map-level popup defaults
3. More marker presets
4. HTMX integration examples and event helpers
5. Framework-agnostic integration examples for static HTML, Django, Flask, FastAPI, and server-rendered apps
6. Layer groups
7. Layer toggles
8. Drawing/editing tools
9. Routing integration with OSM-based services such as OSRM

## License

MIT License.

## Status

CartoLeaf is currently in early development.

Version `0.1` includes core map generation features, basic Leaflet layer support, styling, popups, and browser event emission.

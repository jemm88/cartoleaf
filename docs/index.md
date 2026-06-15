# CartoLeaf

CartoLeaf is a lightweight Python library for generating interactive Leaflet.js maps from Python.

It is designed for developers who want the convenience of defining maps in Python while keeping the generated map directly accessible in the surrounding web page DOM.

Unlike iframe-based map outputs, CartoLeaf generates HTML and JavaScript that can interact with the rest of your page. This makes it useful for dashboards, static pages, server-rendered apps, and custom frontend workflows.

## Why CartoLeaf?

Use CartoLeaf when you want to:

* Generate Leaflet.js maps from Python
* Add markers, circles, polygons, polylines, and GeoJSON layers
* Render maps directly into the page instead of an iframe
* Use text or HTML popups
* Style map layers with simple Python dictionaries
* Emit browser events from map objects
* Connect map interactions to other DOM elements
* Integrate maps into Flask, Django, FastAPI, dashboards, static HTML pages or custom frontend workflows

CartoLeaf is not intended to replace full GIS tools. It is designed as a lightweight bridge between Python and Leaflet.js for practical web map generation.

## Quick Example

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
        popup="Singapore"
    )
)

m.save("map.html")
```

Open `map.html` in your browser to view the generated map.

## Core Concepts

CartoLeaf maps are built around a few simple objects:

| Object       | Description                                                    |
| ------------ | -------------------------------------------------------------- |
| `Map`        | Main map object used to configure, add layers, and render HTML |
| `Marker`     | A point marker on the map                                      |
| `Circle`     | A circular area with a radius in meters                        |
| `Polygon`    | A closed shape made from multiple points                       |
| `Polyline`   | A connected line made from multiple points                     |
| `GeoJson`    | A GeoJSON Feature or FeatureCollection layer                   |
| `CustomIcon` | A custom marker icon using HTML and CSS                        |

## Documentation

Start here:

* [Quick Start](quickstart.md)
* [Map](map.md)
* [Markers](markers.md)
* [Circles](circles.md)
* [Polygons](polygons.md)
* [Polylines](polylines.md)
* [GeoJSON](geojson.md)
* [Custom Icons](custom-icons.md)
* [Events](events.md)
* [Rendering](rendering.md)
* [Layer Styling](layer-styling.md)
* [Web Frameworks](web-frameworks.md)

## Installation

```bash
pip install cartoleaf
```

For local development:

```bash
git clone https://github.com/jemm88/cartoleaf.git
cd cartoleaf
pip install -e .
```

## Status

CartoLeaf is currently in early development.

Version `0.1` includes core map generation features, basic Leaflet layer support, styling, popups, and browser event emission.

# Quick Start

This guide walks through creating your first CartoLeaf map, adding a few layers, and saving the result as an HTML file.

## Installation

Install CartoLeaf from PyPI:

```bash
pip install cartoleaf
```

For local development, clone the repository:

```bash
git clone https://github.com/jemm88/cartoleaf.git
cd cartoleaf
pip install -e .
```

## Create a Basic Map

Start by importing `Map` and `Marker`.

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

## Add More Layers

CartoLeaf supports markers, circles, polygons, polylines, and GeoJSON layers.

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

m.save("map.html")
```

## Coordinate Format

CartoLeaf uses latitude and longitude coordinates in this format:

```python
(lat, lng)
```

Example:

```python
(1.3521, 103.8198)
```

Latitude must be between `-90` and `90`.

Longitude must be between `-180` and `180`.

## Add HTML Popups

Use `popup` for plain text and `popup_html` for HTML content.

```python
Marker(
    lat=1.3521,
    lng=103.8198,
    popup_html="<strong>Singapore</strong><br>Central location"
)
```

Use either `popup` or `popup_html`, not both.

## Open Popups on Hover

Popups can open when the cursor enters a map object and close when the cursor leaves.

```python
Marker(
    lat=1.3521,
    lng=103.8198,
    popup="Hover popup",
    popup_open_on_hover=True,
    popup_close_on_hoverout=True,
)
```

This pattern is also supported by other supported layer types.

## Render Without Saving

If you want the generated HTML as a string instead of writing it to a file, use `render()`.

```python
html = m.render()
```

This returns the map dependencies, container, script, and event emission script as a single HTML string.

## Render as Separate Parts

For server-rendered apps, use `render(split=True)`.

```python
parts = m.render(split=True)

dependencies = parts["dependencies"]
map_html = parts["map"]
script = parts["script"]
emission = parts["emission"]
```

This is useful when your web framework separates content into `<head>`, body, and script sections.

## Next Steps

After creating your first map, continue with:

* [Map](map.md)
* [Markers](markers.md)
* [Circles](circles.md)
* [Polygons](polygons.md)
* [Polylines](polylines.md)
* [GeoJSON](geojson.md)
* [Events](events.md)
* [Rendering](rendering.md)

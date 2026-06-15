# Map

The `Map` class is the main entry point for creating and rendering a CartoLeaf map.

A `Map` stores the map configuration, manages added layers, and generates the final Leaflet HTML and JavaScript.

## Basic Usage

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

## Parameters

| Parameter                 | Type                  | Default                   | Description                                                          |
| ------------------------- | --------------------- | ------------------------- | -------------------------------------------------------------------- |
| `center`                  | `tuple[float, float]` | `(1.3521, 103.8198)`      | Initial map center as `(lat, lng)`.                                  |
| `zoom`                    | `int`                 | `12`                      | Initial map zoom level.                                              |
| `max_zoom`                | `int`                 | `19`                      | Maximum zoom level for the tile layer.                               |
| `map_id`                  | `str`                 | `"cartoleaf-map"`         | HTML element ID used for the map container.                          |
| `height`                  | `str`                 | `"500px"`                 | CSS height of the map container.                                     |
| `fit_bounds`              | `bool`                | `False`                   | Whether the map should automatically fit its bounds to added layers. |
| `fit_bounds_padding`      | `tuple[int, int]`     | `(30, 30)`                | Padding used when fitting bounds, as `(x, y)` pixels.                |
| `allow_multiple_popups`   | `bool`                | `False`                   | Whether multiple popups can remain open at the same time.            |
| `tile_url`                | `str`                 | OpenStreetMap tile URL    | Leaflet tile URL template.                                           |
| `attribution`             | `str`                 | OpenStreetMap attribution | Attribution text displayed on the map.                               |
| `include_bootstrap_icons` | `bool`                | `False`                   | Whether to include Bootstrap Icons in the rendered dependencies.     |

## Map Center

The `center` parameter controls the initial map location.

```python
m = Map(
    center=(1.3521, 103.8198),
    zoom=12,
)
```

CartoLeaf uses the standard latitude and longitude format:

```python
(lat, lng)
```

Latitude must be between `-90` and `90`.

Longitude must be between `-180` and `180`.

## Map Height

The `height` parameter controls the CSS height of the map container.

```python
m = Map(
    center=(1.3521, 103.8198),
    zoom=12,
    height="600px",
)
```

You can use any valid CSS height value:

```python
height="500px"
height="80vh"
height="100%"
```

## Adding Layers

A `Map` can contain markers, circles, polygons, polylines, and GeoJSON layers.

```python
m.add_marker(marker)
m.add_circle(circle)
m.add_polygon(polygon)
m.add_polyline(polyline)
m.add_geojson(geojson)
```

You can also add multiple layers at once:

```python
m.add_markers(markers)
m.add_circles(circles)
m.add_polygons(polygons)
m.add_polylines(polylines)
m.add_geojsons(geojson_layers)
```

## Markers

```python
from cartoleaf import Marker

marker = Marker(
    lat=1.3521,
    lng=103.8198,
    popup="Singapore"
)

m.add_marker(marker)
```

## Circles

```python
from cartoleaf import Circle

circle = Circle(
    lat=1.3521,
    lng=103.8198,
    radius=500,
    popup="500m radius"
)

m.add_circle(circle)
```

## Polygons

```python
from cartoleaf import Polygon

polygon = Polygon(
    coordinates=[
        (1.35, 103.81),
        (1.36, 103.82),
        (1.34, 103.83),
    ],
    popup="Sample polygon"
)

m.add_polygon(polygon)
```

## Polylines

```python
from cartoleaf import Polyline

polyline = Polyline(
    points=[
        (1.3521, 103.8198),
        (1.3000, 103.8500),
    ],
    popup="Sample path"
)

m.add_polyline(polyline)
```

## GeoJSON Layers

```python
from cartoleaf import GeoJson

geojson = GeoJson(
    data=my_geojson_data,
    popup_field="name"
)

m.add_geojson(geojson)
```

## Rendering

CartoLeaf provides several rendering methods depending on how you want to use the generated map.

### `render()`

Returns the dependencies, map container, script, and event emission script as a single HTML string.

```python
html = m.render()
```

This is useful when you want to insert the entire rendered map into a page or return it directly from a route.

### `render(split=True)`

Returns the rendered map as separate parts.

```python
parts = m.render(split=True)

dependencies = parts["dependencies"]
map_html = parts["map"]
script = parts["script"]
emission = parts["emission"]
```

This is useful for web frameworks where dependencies, body content, and scripts need to be placed in different sections of a template.

### `render_full_html()`

Returns a complete standalone HTML document.

```python
html = m.render_full_html(title="My CartoLeaf Map")
```

This includes the HTML document structure, dependencies, map container, script, and event emission script.

### `save()`

Writes a standalone HTML map file.

```python
m.save("map.html")
```

The generated file can be opened directly in a browser.

## Custom Tile Layers

By default, CartoLeaf uses OpenStreetMap tiles.

You can pass a custom Leaflet tile URL and attribution.

```python
m = Map(
    center=(1.3521, 103.8198),
    zoom=12,
    tile_url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    attribution="&copy; OpenStreetMap contributors",
)
```

## Multiple Popups

By default, Leaflet closes the current popup when another popup opens.

Set `allow_multiple_popups=True` to allow multiple popups to remain open at the same time.

```python
m = Map(
    center=(1.3521, 103.8198),
    zoom=12,
    allow_multiple_popups=True,
)
```

## Fit Bounds

Set `fit_bounds=True` to automatically fit the map view around added layers.

```python
m = Map(
    center=(1.3521, 103.8198),
    zoom=12,
    fit_bounds=True,
    fit_bounds_padding=(30, 30),
)
```

This is useful when you want the map to automatically frame all visible layers.

## Bootstrap Icons

If your custom marker icons use Bootstrap Icons, set `include_bootstrap_icons=True`.

```python
from cartoleaf import Map, Marker, custom_pin_icon, bootstrap_icon

m = Map(
    center=(1.3521, 103.8198),
    zoom=12,
    include_bootstrap_icons=True,
)

icon = custom_pin_icon(
    background_color="#2879e4",
    text_color="#fff",
    inner_html=bootstrap_icon("house"),
)

m.add_marker(
    Marker(
        lat=1.3521,
        lng=103.8198,
        popup="Home",
        icon=icon,
    )
)
```

## Next Steps

Continue with:

* [Markers](markers.md)
* [Circles](circles.md)
* [Polygons](polygons.md)
* [Polylines](polylines.md)
* [GeoJSON](geojson.md)
* [Rendering](rendering.md)

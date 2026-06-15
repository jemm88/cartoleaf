# Polygons

The `Polygon` class is used to draw a closed shape on a CartoLeaf map.

A polygon is defined by a list of latitude and longitude coordinate pairs. This is useful for drawing custom areas such as zones, boundaries, districts, catchment areas, or manually defined regions.

## Basic Usage

```python
from cartoleaf import Map, Polygon

m = Map(
    center=(1.3521, 103.8198),
    zoom=12,
)

polygon = Polygon(
    coordinates=[
        (1.35, 103.81),
        (1.36, 103.82),
        (1.34, 103.83),
    ],
    popup="Sample polygon",
)

m.add_polygon(polygon)

m.save("map.html")
```

## Parameters

| Parameter                 | Type                        | Default                 | Description                                                           |
| ------------------------- | --------------------------- | ----------------------- | --------------------------------------------------------------------- |
| `coordinates`             | `list[tuple[float, float]]` | Required                | Polygon points as `(lat, lng)` pairs. Requires at least three points. |
| `popup`                   | `str \| None`               | `None`                  | Plain text popup content.                                             |
| `popup_html`              | `str \| None`               | `None`                  | HTML popup content. Use either `popup` or `popup_html`, not both.     |
| `popup_options`           | `dict[str, Any]`            | `{}`                    | Reserved for future popup configuration support.                      |
| `popup_open_on_hover`     | `bool`                      | `False`                 | Opens the popup when the cursor enters the polygon.                   |
| `popup_close_on_hoverout` | `bool`                      | `False`                 | Closes the popup when the cursor leaves the polygon.                  |
| `data`                    | `dict[str, Any]`            | `{}`                    | Custom metadata included in emitted browser events.                   |
| `events`                  | `dict[str, str]`            | `{}`                    | Event mapping for supported browser interactions.                     |
| `polygon_id`              | `str`                       | Auto-generated          | Unique polygon identifier.                                            |
| `style`                   | `dict[str, Any]`            | `POLYGEO_DEFAULT_STYLE` | Leaflet style options applied to the polygon.                         |

## Coordinate Format

Polygon coordinates should be provided as `(lat, lng)` tuples.

```python
coordinates=[
    (1.35, 103.81),
    (1.36, 103.82),
    (1.34, 103.83),
]
```

A polygon requires at least three coordinate points.

Latitude values must be between `-90` and `90`.

Longitude values must be between `-180` and `180`.

## Styling Polygons

Polygon styles follow Leaflet path style options.

```python
polygon = Polygon(
    coordinates=[
        (1.35, 103.81),
        (1.36, 103.82),
        (1.34, 103.83),
    ],
    popup="Styled polygon",
    style={
        "color": "#2879e4",
        "fillColor": "#2879e4",
        "fillOpacity": 0.2,
        "weight": 2,
    },
)
```

Common style options include:

| Style Option  | Description                             |
| ------------- | --------------------------------------- |
| `color`       | Stroke color of the polygon outline.    |
| `fillColor`   | Fill color of the polygon.              |
| `fillOpacity` | Opacity of the polygon fill.            |
| `opacity`     | Opacity of the polygon outline.         |
| `weight`      | Width of the polygon outline in pixels. |

For more details, see [Layer Styling](layer-styling.md).

## Plain Text Popups

Use `popup` for simple text content.

```python
Polygon(
    coordinates=[
        (1.35, 103.81),
        (1.36, 103.82),
        (1.34, 103.83),
    ],
    popup="Sample polygon",
)
```

## HTML Popups

Use `popup_html` for richer popup content.

```python
Polygon(
    coordinates=[
        (1.35, 103.81),
        (1.36, 103.82),
        (1.34, 103.83),
    ],
    popup_html="<strong>Sample Area</strong><br>Custom polygon",
)
```

Use either `popup` or `popup_html`, not both.

## Hover Popups

You can configure polygon popups to open when the cursor enters the polygon and close when the cursor leaves.

```python
Polygon(
    coordinates=[
        (1.35, 103.81),
        (1.36, 103.82),
        (1.34, 103.83),
    ],
    popup="Hover popup",
    popup_open_on_hover=True,
    popup_close_on_hoverout=True,
)
```

## Polygon Events

Polygons can emit browser events when users interact with them.

```python
Polygon(
    coordinates=[
        (1.35, 103.81),
        (1.36, 103.82),
        (1.34, 103.83),
    ],
    data={
        "name": "Sample Area",
        "type": "custom-zone",
    },
    events={
        "click": "polygon-clicked",
        "hoverin": "polygon-hovered",
    },
)
```

In the browser, listen for the emitted event:

```html
<script>
window.addEventListener("polygon-clicked", function (event) {
  console.log(event.detail);
});
</script>
```

The emitted event detail includes the polygon ID, event type, and custom data.

## Adding Multiple Polygons

Use `add_polygons()` to add multiple polygons at once.

```python
from cartoleaf import Map, Polygon

m = Map(
    center=(1.3521, 103.8198),
    zoom=12,
)

polygons = [
    Polygon(
        coordinates=[
            (1.35, 103.81),
            (1.36, 103.82),
            (1.34, 103.83),
        ],
        popup="Polygon A",
    ),
    Polygon(
        coordinates=[
            (1.30, 103.80),
            (1.31, 103.82),
            (1.29, 103.83),
        ],
        popup="Polygon B",
    ),
]

m.add_polygons(polygons)

m.save("map.html")
```

## Validation

CartoLeaf validates polygon inputs when a `Polygon` is created.

The following will raise an error:

```python
Polygon(
    coordinates=[
        (1.35, 103.81),
        (1.36, 103.82),
    ],
)
```

A polygon requires at least three coordinate points.

The following will also raise an error:

```python
Polygon(
    coordinates=[
        (1.35, 103.81),
        (1.36, 103.82),
        (1.34, 103.83),
    ],
    popup="Text popup",
    popup_html="<strong>HTML popup</strong>",
)
```

Use either `popup` or `popup_html`, not both.

## Next Steps

Continue with:

* [Polylines](polylines.md)
* [GeoJSON](geojson.md)
* [Layer Styling](layer-styling.md)
* [Events](events.md)
* [Map](map.md)

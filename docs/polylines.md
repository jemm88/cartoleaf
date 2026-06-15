# Polylines

The `Polyline` class is used to draw a connected line on a CartoLeaf map.

A polyline is defined by two or more latitude and longitude coordinate pairs. This is useful for drawing routes, paths, trails, connections, boundaries, or movement lines.

## Basic Usage

```python
from cartoleaf import Map, Polyline

m = Map(
    center=(1.3521, 103.8198),
    zoom=12,
)

polyline = Polyline(
    points=[
        (1.3521, 103.8198),
        (1.3000, 103.8500),
        (1.2800, 103.8600),
    ],
    popup="Sample path",
)

m.add_polyline(polyline)

m.save("map.html")
```

## Parameters

| Parameter                 | Type                        | Default        | Description                                                          |
| ------------------------- | --------------------------- | -------------- | -------------------------------------------------------------------- |
| `points`                  | `list[tuple[float, float]]` | Required       | Polyline points as `(lat, lng)` pairs. Requires at least two points. |
| `style`                   | `dict[str, Any]`            | `{}`           | Leaflet style options applied to the polyline.                       |
| `popup`                   | `str \| None`               | `None`         | Plain text popup content.                                            |
| `popup_html`              | `str \| None`               | `None`         | HTML popup content. Use either `popup` or `popup_html`, not both.    |
| `popup_open_on_hover`     | `bool`                      | `False`        | Opens the popup when the cursor enters the polyline.                 |
| `popup_close_on_hoverout` | `bool`                      | `False`        | Closes the popup when the cursor leaves the polyline.                |
| `events`                  | `dict[str, str]`            | `{}`           | Event mapping for supported browser interactions.                    |
| `data`                    | `dict[str, Any]`            | `{}`           | Custom metadata included in emitted browser events.                  |
| `polyline_id`             | `str`                       | Auto-generated | Unique polyline identifier.                                          |

## Point Format

Polyline points should be provided as `(lat, lng)` tuples.

```python
points=[
    (1.3521, 103.8198),
    (1.3000, 103.8500),
    (1.2800, 103.8600),
]
```

A polyline requires at least two coordinate points.

Latitude values must be between `-90` and `90`.

Longitude values must be between `-180` and `180`.

## Styling Polylines

Polyline styles follow Leaflet path style options.

```python
polyline = Polyline(
    points=[
        (1.3521, 103.8198),
        (1.3000, 103.8500),
        (1.2800, 103.8600),
    ],
    popup="Styled path",
    style={
        "color": "#2879e4",
        "weight": 4,
        "opacity": 0.8,
    },
)
```

Common style options include:

| Style Option | Description                              |
| ------------ | ---------------------------------------- |
| `color`      | Stroke color of the line.                |
| `weight`     | Width of the line in pixels.             |
| `opacity`    | Opacity of the line.                     |
| `dashArray`  | Dash pattern for dashed or dotted lines. |

For more details, see [Layer Styling](layer-styling.md).

## Dashed Lines

Use `dashArray` to create dashed or dotted lines.

```python
polyline = Polyline(
    points=[
        (1.3521, 103.8198),
        (1.3000, 103.8500),
    ],
    style={
        "color": "#2879e4",
        "weight": 3,
        "dashArray": "6, 6",
    },
)
```

## Plain Text Popups

Use `popup` for simple text content.

```python
Polyline(
    points=[
        (1.3521, 103.8198),
        (1.3000, 103.8500),
    ],
    popup="Sample path",
)
```

## HTML Popups

Use `popup_html` for richer popup content.

```python
Polyline(
    points=[
        (1.3521, 103.8198),
        (1.3000, 103.8500),
    ],
    popup_html="<strong>Route A</strong><br>Estimated distance: 6km",
)
```

Use either `popup` or `popup_html`, not both.

## Hover Popups

You can configure polyline popups to open when the cursor enters the line and close when the cursor leaves.

```python
Polyline(
    points=[
        (1.3521, 103.8198),
        (1.3000, 103.8500),
    ],
    popup="Hover popup",
    popup_open_on_hover=True,
    popup_close_on_hoverout=True,
)
```

## Polyline Events

Polylines can emit browser events when users interact with them.

```python
Polyline(
    points=[
        (1.3521, 103.8198),
        (1.3000, 103.8500),
    ],
    data={
        "name": "Route A",
        "type": "walking-route",
    },
    events={
        "click": "polyline-clicked",
        "hoverin": "polyline-hovered",
    },
)
```

In the browser, listen for the emitted event:

```html
<script>
window.addEventListener("polyline-clicked", function (event) {
  console.log(event.detail);
});
</script>
```

The emitted event detail includes the polyline ID, event type, and custom data.

## Adding Multiple Polylines

Use `add_polylines()` to add multiple polylines at once.

```python
from cartoleaf import Map, Polyline

m = Map(
    center=(1.3521, 103.8198),
    zoom=12,
)

polylines = [
    Polyline(
        points=[
            (1.3521, 103.8198),
            (1.3000, 103.8500),
        ],
        popup="Polyline A",
    ),
    Polyline(
        points=[
            (1.3100, 103.8200),
            (1.2900, 103.8600),
        ],
        popup="Polyline B",
    ),
]

m.add_polylines(polylines)

m.save("map.html")
```

## Validation

CartoLeaf validates polyline inputs when a `Polyline` is created.

The following will raise an error:

```python
Polyline(
    points=[
        (1.3521, 103.8198),
    ],
)
```

A polyline requires at least two coordinate points.

The following will also raise an error:

```python
Polyline(
    points=[
        (1.3521, 103.8198),
        (1.3000, 103.8500),
    ],
    popup="Text popup",
    popup_html="<strong>HTML popup</strong>",
)
```

Use either `popup` or `popup_html`, not both.

## Next Steps

Continue with:

* [GeoJSON](geojson.md)
* [Layer Styling](layer-styling.md)
* [Events](events.md)
* [Map](map.md)

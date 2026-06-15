# Circles

The `Circle` class is used to draw a circular area on a CartoLeaf map.

A circle is defined by a center coordinate and a radius in meters. This is useful for visualising coverage zones, distance buffers, walking areas, service areas, or search radii.

## Basic Usage

```python
from cartoleaf import Map, Circle

m = Map(
    center=(1.3521, 103.8198),
    zoom=13,
)

circle = Circle(
    lat=1.3521,
    lng=103.8198,
    radius=500,
    popup="500m radius"
)

m.add_circle(circle)

m.save("map.html")
```

## Parameters

| Parameter                 | Type             | Default                 | Description                                                       |
| ------------------------- | ---------------- | ----------------------- | ----------------------------------------------------------------- |
| `lat`                     | `float`          | Required                | Latitude of the circle center. Must be between `-90` and `90`.    |
| `lng`                     | `float`          | Required                | Longitude of the circle center. Must be between `-180` and `180`. |
| `radius`                  | `float`          | Required                | Radius of the circle in meters. Must be greater than `0`.         |
| `popup`                   | `str \| None`    | `None`                  | Plain text popup content.                                         |
| `popup_html`              | `str \| None`    | `None`                  | HTML popup content. Use either `popup` or `popup_html`, not both. |
| `popup_options`           | `dict[str, Any]` | `{}`                    | Reserved for future popup configuration support.                  |
| `popup_open_on_hover`     | `bool`           | `False`                 | Opens the popup when the cursor enters the circle.                |
| `popup_close_on_hoverout` | `bool`           | `False`                 | Closes the popup when the cursor leaves the circle.               |
| `data`                    | `dict[str, Any]` | `{}`                    | Custom metadata included in emitted browser events.               |
| `events`                  | `dict[str, str]` | `{}`                    | Event mapping for supported browser interactions.                 |
| `circle_id`               | `str`            | Auto-generated          | Unique circle identifier.                                         |
| `style`                   | `dict[str, Any]` | `POLYGEO_DEFAULT_STYLE` | Leaflet style options applied to the circle.                      |

## Coordinate Format

Circles use latitude and longitude coordinates for the center point.

```python
Circle(
    lat=1.3521,
    lng=103.8198,
    radius=500,
)
```

Latitude must be between `-90` and `90`.

Longitude must be between `-180` and `180`.

## Radius

The `radius` value is measured in meters.

```python
Circle(
    lat=1.3521,
    lng=103.8198,
    radius=500,
)
```

This creates a circle with a 500 metre radius around the center point.

The radius must be greater than `0`.

## Styling Circles

Circle styles follow Leaflet path style options.

```python
circle = Circle(
    lat=1.3521,
    lng=103.8198,
    radius=500,
    popup="Styled circle",
    style={
        "color": "#2879e4",
        "fillColor": "#2879e4",
        "fillOpacity": 0.2,
        "weight": 2,
    },
)
```

Common style options include:

| Style Option  | Description                            |
| ------------- | -------------------------------------- |
| `color`       | Stroke color of the circle outline.    |
| `fillColor`   | Fill color of the circle.              |
| `fillOpacity` | Opacity of the circle fill.            |
| `opacity`     | Opacity of the circle outline.         |
| `weight`      | Width of the circle outline in pixels. |

For more details, see [Layer Styling](layer-styling.md).

## Plain Text Popups

Use `popup` for simple text content.

```python
Circle(
    lat=1.3521,
    lng=103.8198,
    radius=500,
    popup="500m radius"
)
```

## HTML Popups

Use `popup_html` for richer popup content.

```python
Circle(
    lat=1.3521,
    lng=103.8198,
    radius=500,
    popup_html="<strong>Coverage Area</strong><br>Radius: 500m"
)
```

Use either `popup` or `popup_html`, not both.

## Hover Popups

You can configure circle popups to open when the cursor enters the circle and close when the cursor leaves.

```python
Circle(
    lat=1.3521,
    lng=103.8198,
    radius=500,
    popup="Hover popup",
    popup_open_on_hover=True,
    popup_close_on_hoverout=True,
)
```

## Circle Events

Circles can emit browser events when users interact with them.

```python
Circle(
    lat=1.3521,
    lng=103.8198,
    radius=500,
    data={
        "name": "Singapore",
        "radius_m": 500,
    },
    events={
        "click": "circle-clicked",
        "hoverin": "circle-hovered",
    },
)
```

In the browser, listen for the emitted event:

```html
<script>
window.addEventListener("circle-clicked", function (event) {
  console.log(event.detail);
});
</script>
```

The emitted event detail includes the circle ID, event type, and custom data.

## Adding Multiple Circles

Use `add_circles()` to add multiple circles at once.

```python
from cartoleaf import Map, Circle

m = Map(
    center=(1.3521, 103.8198),
    zoom=12,
)

circles = [
    Circle(
        lat=1.3521,
        lng=103.8198,
        radius=500,
        popup="Circle A",
    ),
    Circle(
        lat=1.3000,
        lng=103.8500,
        radius=750,
        popup="Circle B",
    ),
]

m.add_circles(circles)

m.save("map.html")
```

## Validation

CartoLeaf validates circle inputs when a `Circle` is created.

The following will raise an error:

```python
Circle(
    lat=1.3521,
    lng=103.8198,
    radius=0,
)
```

The radius must be greater than `0`.

The following will also raise an error:

```python
Circle(
    lat=1.3521,
    lng=103.8198,
    radius=500,
    popup="Text popup",
    popup_html="<strong>HTML popup</strong>",
)
```

Use either `popup` or `popup_html`, not both.

## Next Steps

Continue with:

* [Polygons](polygons.md)
* [Polylines](polylines.md)
* [Layer Styling](layer-styling.md)
* [Events](events.md)
* [Map](map.md)

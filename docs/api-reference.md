# API Reference

This page provides a compact reference for CartoLeaf's main classes and helper functions.

For full usage examples, see the individual documentation pages linked in each section.

## `Map`

The main CartoLeaf map object.

Use `Map` to configure the map, add layers, and render the final HTML output.

```python
from cartoleaf import Map

m = Map(
    center=(1.3521, 103.8198),
    zoom=12,
)
```

### Parameters

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

### Layer Methods

| Method                         | Description                             |
| ------------------------------ | --------------------------------------- |
| `add_marker(marker)`           | Add a `Marker` to the map.              |
| `add_markers(markers)`         | Add multiple markers to the map.        |
| `add_circle(circle)`           | Add a `Circle` to the map.              |
| `add_circles(circles)`         | Add multiple circles to the map.        |
| `add_polygon(polygon)`         | Add a `Polygon` to the map.             |
| `add_polygons(polygons)`       | Add multiple polygons to the map.       |
| `add_polyline(polyline)`       | Add a `Polyline` to the map.            |
| `add_polylines(polylines)`     | Add multiple polylines to the map.      |
| `add_geojson(geojson)`         | Add a `GeoJson` layer to the map.       |
| `add_geojsons(geojson_layers)` | Add multiple GeoJSON layers to the map. |

### Rendering Methods

| Method                                    | Description                                 |
| ----------------------------------------- | ------------------------------------------- |
| `render()`                                | Return the rendered map as one HTML string. |
| `render(split=True)`                      | Return rendered parts as a dictionary.      |
| `render_full_html(title="Cartoleaf Map")` | Return a complete standalone HTML document. |
| `save(path)`                              | Save the map as an HTML file.               |

See [Map](map.md) and [Rendering](rendering.md).

---

## `Marker`

Represents a point marker on the map.

```python
from cartoleaf import Marker

marker = Marker(
    lat=1.3521,
    lng=103.8198,
    popup="Singapore",
)
```

### Parameters

| Parameter                 | Type                 | Default        | Description                                                       |
| ------------------------- | -------------------- | -------------- | ----------------------------------------------------------------- |
| `lat`                     | `float`              | Required       | Latitude of the marker. Must be between `-90` and `90`.           |
| `lng`                     | `float`              | Required       | Longitude of the marker. Must be between `-180` and `180`.        |
| `popup`                   | `str \| None`        | `None`         | Plain text popup content.                                         |
| `popup_html`              | `str \| None`        | `None`         | HTML popup content. Use either `popup` or `popup_html`, not both. |
| `popup_options`           | `dict[str, Any]`     | `{}`           | Reserved for future popup configuration support.                  |
| `popup_open_on_hover`     | `bool`               | `False`        | Opens the popup when the cursor enters the marker.                |
| `popup_close_on_hoverout` | `bool`               | `False`        | Closes the popup when the cursor leaves the marker.               |
| `data`                    | `dict[str, Any]`     | `{}`           | Custom metadata included in emitted browser events.               |
| `events`                  | `dict[str, str]`     | `{}`           | Event mapping for supported browser interactions.                 |
| `marker_id`               | `str`                | Auto-generated | Unique marker identifier.                                         |
| `icon`                    | `CustomIcon \| None` | `None`         | Optional custom marker icon.                                      |

See [Markers](markers.md), [Custom Icons](custom-icons.md), and [Events](events.md).

---

## `Circle`

Represents a circular area on the map.

The radius is measured in meters.

```python
from cartoleaf import Circle

circle = Circle(
    lat=1.3521,
    lng=103.8198,
    radius=500,
    popup="500m radius",
)
```

### Parameters

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

See [Circles](circles.md), [Layer Styling](layer-styling.md), and [Events](events.md).

---

## `Polygon`

Represents a closed shape on the map.

```python
from cartoleaf import Polygon

polygon = Polygon(
    coordinates=[
        (1.35, 103.81),
        (1.36, 103.82),
        (1.34, 103.83),
    ],
    popup="Sample polygon",
)
```

### Parameters

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

See [Polygons](polygons.md), [Layer Styling](layer-styling.md), and [Events](events.md).

---

## `Polyline`

Represents a connected line on the map.

```python
from cartoleaf import Polyline

polyline = Polyline(
    points=[
        (1.3521, 103.8198),
        (1.3000, 103.8500),
    ],
    popup="Sample route",
)
```

### Parameters

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

See [Polylines](polylines.md), [Layer Styling](layer-styling.md), and [Events](events.md).

---

## `GeoJson`

Represents a GeoJSON layer on the map.

CartoLeaf currently supports top-level GeoJSON objects of type `Feature` or `FeatureCollection`.

```python
from cartoleaf import GeoJson

geojson = GeoJson(
    data=geojson_data,
    popup_field="name",
)
```

### Parameters

| Parameter                 | Type             | Default                 | Description                                                |
| ------------------------- | ---------------- | ----------------------- | ---------------------------------------------------------- |
| `data`                    | `dict[str, Any]` | Required                | GeoJSON data. Must be a `Feature` or `FeatureCollection`.  |
| `popup_field`             | `str \| None`    | `None`                  | Feature property name to use as popup content.             |
| `popup_open_on_hover`     | `bool`           | `False`                 | Opens the popup when the cursor enters a GeoJSON feature.  |
| `popup_close_on_hoverout` | `bool`           | `False`                 | Closes the popup when the cursor leaves a GeoJSON feature. |
| `events`                  | `dict[str, str]` | `{}`                    | Event mapping for supported browser interactions.          |
| `geojson_id`              | `str`            | Auto-generated          | Unique GeoJSON layer identifier.                           |
| `style`                   | `dict[str, Any]` | `POLYGEO_DEFAULT_STYLE` | Leaflet style options applied to the GeoJSON layer.        |

See [GeoJSON](geojson.md), [Layer Styling](layer-styling.md), and [Events](events.md).

---

## `CustomIcon`

Represents a custom marker icon.

`CustomIcon` is the lower-level icon class used when you want direct control over marker HTML, size, anchor position, popup anchor, and CSS class.

```python
from cartoleaf import CustomIcon

icon = CustomIcon(
    html="<div class='my-marker'>A</div>",
    icon_size=(33, 33),
    icon_anchor=(16, 33),
    popup_anchor=(0, -27),
    class_name="my-custom-icon",
)
```

### Parameters

| Parameter      | Type              | Default    | Description                                                            |
| -------------- | ----------------- | ---------- | ---------------------------------------------------------------------- |
| `html`         | `str`             | Required   | HTML content rendered inside the marker icon.                          |
| `icon_size`    | `tuple[int, int]` | `(33, 33)` | Width and height of the icon in pixels.                                |
| `icon_anchor`  | `tuple[int, int]` | `(16, 33)` | Pixel coordinate within the icon that is anchored to the map location. |
| `popup_anchor` | `tuple[int, int]` | `(0, -27)` | Pixel offset from the icon anchor where the popup opens.               |
| `class_name`   | `str`             | `""`       | Optional CSS class added to the Leaflet icon container.                |

See [Custom Icons](custom-icons.md).

---

## `custom_pin_icon()`

Creates a pin-shaped custom marker icon.

This is the recommended helper for most custom marker pins.

```python
from cartoleaf import custom_pin_icon

icon = custom_pin_icon(
    background_color="#2879e4",
    text_color="#fff",
    inner_text="A",
)
```

### Parameters

| Parameter          | Type          | Default     | Description                                                                              |
| ------------------ | ------------- | ----------- | ---------------------------------------------------------------------------------------- |
| `background_color` | `str`         | `"#693"`    | Background color of the pin. Accepts any valid CSS color value.                          |
| `text_color`       | `str`         | `"#fff"`    | Text or icon color inside the pin.                                                       |
| `inner_text`       | `str`         | `""`        | Plain text displayed inside the pin.                                                     |
| `inner_html`       | `str \| None` | `None`      | Custom HTML displayed inside the pin. Takes precedence over `inner_text`.                |
| `name_type`        | `str`         | `"default"` | Name used to generate CSS class names for the icon. Useful for avoiding style conflicts. |
| `inner_circle`     | `bool`        | `False`     | Whether to place the inner content inside a circular background.                         |
| `icon_wh`          | `int`         | `33`        | Width and height of the icon in pixels.                                                  |
| `inner_bg`         | `str`         | `"#fff"`    | Background color of the inner circle when `inner_circle=True`.                           |
| `font_size`        | `int`         | `15`        | Font size of the inner content in pixels.                                                |
| `font_weight`      | `int`         | `400`       | Font weight of the inner content.                                                        |
| `inner_wh`         | `int`         | `70`        | Width and height of the inner circle as a percentage of the pin size.                    |

### Returns

| Type         | Description                                                    |
| ------------ | -------------------------------------------------------------- |
| `CustomIcon` | A custom marker icon that can be passed to `Marker(icon=...)`. |

See [Custom Icons](custom-icons.md).

---

## `bootstrap_icon()`

Returns Bootstrap Icons HTML for use inside custom marker pins.

```python
from cartoleaf import bootstrap_icon

html = bootstrap_icon("house")
```

This returns:

```html
<i class="bi bi-house"></i>
```

Use it with `custom_pin_icon()`:

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

For Bootstrap icons to display correctly, set `include_bootstrap_icons=True` on the map.

See [Custom Icons](custom-icons.md).

---

## Coordinate Order

Most CartoLeaf layer classes use:

```python
(lat, lng)
```

This applies to:

* `Marker`
* `Circle`
* `Polygon`
* `Polyline`
* `Map.center`

GeoJSON follows the GeoJSON standard and uses:

```python
[lng, lat]
```

See [GeoJSON](geojson.md).

## Event Aliases

Supported event aliases include:

| CartoLeaf Event | Leaflet Event |
| --------------- | ------------- |
| `click`         | `click`       |
| `hoverin`       | `mouseover`   |
| `hoverout`      | `mouseout`    |

See [Events](events.md).

## Popup Types

| Option                    | Description                             |
| ------------------------- | --------------------------------------- |
| `popup`                   | Plain text popup content.               |
| `popup_html`              | Custom HTML popup content.              |
| `popup_field`             | GeoJSON property used as popup content. |
| `popup_open_on_hover`     | Opens popup on hover.                   |
| `popup_close_on_hoverout` | Closes popup when cursor leaves.        |

See [Popups](popups.md).

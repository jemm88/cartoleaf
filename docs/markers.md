# Markers

The `Marker` class is used to place a point marker on a CartoLeaf map.

Markers support plain text popups, HTML popups, hover popup behavior, browser events, custom metadata, and custom icons.

## Basic Usage

```python
from cartoleaf import Map, Marker

m = Map(
    center=(1.3521, 103.8198),
    zoom=12,
)

marker = Marker(
    lat=1.3521,
    lng=103.8198,
    popup="Singapore"
)

m.add_marker(marker)

m.save("map.html")
```

## Parameters

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

## Coordinate Format

Markers use latitude and longitude coordinates.

```python
Marker(
    lat=1.3521,
    lng=103.8198,
)
```

Latitude must be between `-90` and `90`.

Longitude must be between `-180` and `180`.

## Plain Text Popups

Use `popup` for simple text content.

```python
Marker(
    lat=1.3521,
    lng=103.8198,
    popup="Singapore"
)
```

## HTML Popups

Use `popup_html` for richer popup content.

```python
Marker(
    lat=1.3521,
    lng=103.8198,
    popup_html="<strong>Singapore</strong><br>Central location"
)
```

Use either `popup` or `popup_html`, not both.

## Hover Popups

You can configure marker popups to open when the cursor enters the marker and close when the cursor leaves.

```python
Marker(
    lat=1.3521,
    lng=103.8198,
    popup="Hover popup",
    popup_open_on_hover=True,
    popup_close_on_hoverout=True,
)
```

You can also open on hover without closing automatically.

```python
Marker(
    lat=1.3521,
    lng=103.8198,
    popup="Hover popup",
    popup_open_on_hover=True,
)
```

## Custom Icons

Markers can use custom icons created with `CustomIcon` or helper functions such as `custom_pin_icon()`.

```python
from cartoleaf import Map, Marker, custom_pin_icon

m = Map(
    center=(1.3521, 103.8198),
    zoom=12,
)

icon = custom_pin_icon(
    background_color="#2879e4",
    text_color="#fff",
    inner_text="A",
)

m.add_marker(
    Marker(
        lat=1.3521,
        lng=103.8198,
        popup="Custom marker",
        icon=icon,
    )
)
```

For more details, see [Custom Icons](custom-icons.md).

## Marker Events

Markers can emit browser events when users interact with them.

```python
Marker(
    lat=1.3521,
    lng=103.8198,
    popup="Clickable marker",
    data={
        "name": "Singapore",
        "type": "city",
    },
    events={
        "click": "marker-clicked",
        "hoverin": "marker-hovered",
    },
)
```

In the browser, listen for the emitted event:

```html
<script>
window.addEventListener("marker-clicked", function (event) {
  console.log(event.detail);
});
</script>
```

The emitted event detail includes the marker ID, event type, and custom data.

## Adding Multiple Markers

Use `add_markers()` to add multiple markers at once.

```python
from cartoleaf import Map, Marker

m = Map(
    center=(1.3521, 103.8198),
    zoom=12,
)

markers = [
    Marker(
        lat=1.3521,
        lng=103.8198,
        popup="Marker A",
    ),
    Marker(
        lat=1.3000,
        lng=103.8500,
        popup="Marker B",
    ),
]

m.add_markers(markers)

m.save("map.html")
```

## Validation

CartoLeaf validates marker inputs when a `Marker` is created.

The following will raise an error:

```python
Marker(
    lat=100,
    lng=103.8198,
)
```

Latitude must be between `-90` and `90`.

The following will also raise an error:

```python
Marker(
    lat=1.3521,
    lng=103.8198,
    popup="Text popup",
    popup_html="<strong>HTML popup</strong>",
)
```

Use either `popup` or `popup_html`, not both.

## Next Steps

Continue with:

* [Custom Icons](custom-icons.md)
* [Events](events.md)
* [Circles](circles.md)
* [Map](map.md)

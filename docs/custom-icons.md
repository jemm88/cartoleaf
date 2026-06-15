# Custom Icons

CartoLeaf supports custom marker icons through the `CustomIcon` class and the `custom_pin_icon()` helper.

Use custom icons when you want marker pins with custom colors, text, HTML, or Bootstrap icons.

## Basic Custom Pin

The easiest way to create a custom marker pin is to use `custom_pin_icon()`.

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

m.save("map.html")
```

## `custom_pin_icon()`

`custom_pin_icon()` creates a pin-shaped marker icon using inline HTML and CSS.

```python
custom_pin_icon(
    background_color="#2879e4",
    text_color="#fff",
    inner_text="A",
)
```

## Parameters

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

## Text Pins

Use `inner_text` for simple text labels.

```python
icon = custom_pin_icon(
    background_color="#2879e4",
    text_color="#fff",
    inner_text="1",
)
```

This is useful for numbered markers, labels, or simple category indicators.

## Pins with Inner Circle

Set `inner_circle=True` to place the inner content inside a circular background.

```python
icon = custom_pin_icon(
    background_color="#2879e4",
    text_color="#2879e4",
    inner_text="A",
    inner_circle=True,
    inner_bg="#fff",
)
```

This creates a pin with a colored outer body and a separate circular inner area.

## HTML Pins

Use `inner_html` when you want to pass custom HTML.

```python
icon = custom_pin_icon(
    background_color="#2879e4",
    text_color="#fff",
    inner_html="<strong>A</strong>",
)
```

When `inner_html` is provided, it is used instead of `inner_text`.

## Bootstrap Icons

CartoLeaf includes a small `bootstrap_icon()` helper.

```python
from cartoleaf import bootstrap_icon

bootstrap_icon("house")
```

This returns:

```html
<i class="bi bi-house"></i>
```

Use it inside `custom_pin_icon()` like this:

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

## `CustomIcon`

`CustomIcon` is the lower-level icon class used by CartoLeaf markers.

It gives you direct control over the HTML, icon size, anchor point, popup anchor, and CSS class.

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

Then pass the icon to a marker:

```python
from cartoleaf import Marker

marker = Marker(
    lat=1.3521,
    lng=103.8198,
    popup="Custom icon",
    icon=icon,
)
```

## `CustomIcon` Parameters

| Parameter      | Type              | Default    | Description                                                            |
| -------------- | ----------------- | ---------- | ---------------------------------------------------------------------- |
| `html`         | `str`             | Required   | HTML content rendered inside the marker icon.                          |
| `icon_size`    | `tuple[int, int]` | `(33, 33)` | Width and height of the icon in pixels.                                |
| `icon_anchor`  | `tuple[int, int]` | `(16, 33)` | Pixel coordinate within the icon that is anchored to the map location. |
| `popup_anchor` | `tuple[int, int]` | `(0, -27)` | Pixel offset from the icon anchor where the popup opens.               |
| `class_name`   | `str`             | `""`       | Optional CSS class added to the Leaflet icon container.                |

## Icon Anchor

The `icon_anchor` controls which point of the icon is attached to the map coordinate.

For pin-shaped icons, this is usually the bottom center of the icon.

```python
icon_anchor=(16, 33)
```

For a `33 x 33` icon, this means the bottom center of the icon is attached to the marker coordinate.

## Popup Anchor

The `popup_anchor` controls where the popup opens relative to the icon anchor.

```python
popup_anchor=(0, -27)
```

This places the popup above the marker.

## When to Use Each Option

| Option              | Use case                                                         |
| ------------------- | ---------------------------------------------------------------- |
| `custom_pin_icon()` | Recommended for most custom pin markers.                         |
| `bootstrap_icon()`  | Use Bootstrap Icons inside custom pins.                          |
| `CustomIcon`        | Use when you need full control over the marker HTML and anchors. |

## Next Steps

Continue with:

* [Markers](markers.md)
* [Events](events.md)
* [Layer Styling](layer-styling.md)
* [Map](map.md)

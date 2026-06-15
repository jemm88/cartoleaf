# Layer Styling

CartoLeaf supports styling for map layers that are rendered as Leaflet path objects.

This includes:

* `Circle`
* `Polygon`
* `Polyline`
* `GeoJson`

Styles are passed as Python dictionaries and forwarded to the underlying Leaflet layer.

CartoLeaf does not define a separate styling language. Instead, it relies on Leaflet's path style options, so users familiar with Leaflet can use the same option names in Python.

When you pass a `style` dictionary to a CartoLeaf layer, CartoLeaf forwards those values to the underlying Leaflet layer. This means most standard Leaflet path options can be used directly, such as `color`, `weight`, `opacity`, `fillColor`, `fillOpacity`, and `dashArray`.

## Basic Usage

```python
from cartoleaf import Circle

circle = Circle(
    lat=1.3521,
    lng=103.8198,
    radius=500,
    style={
        "color": "#2879e4",
        "fillColor": "#2879e4",
        "fillOpacity": 0.2,
        "weight": 2,
    },
)
```

## Common Style Options

| Option        | Description                                |
| ------------- | ------------------------------------------ |
| `color`       | Stroke color of the layer outline or line. |
| `weight`      | Stroke width in pixels.                    |
| `opacity`     | Stroke opacity.                            |
| `fillColor`   | Fill color for filled shapes.              |
| `fillOpacity` | Fill opacity for filled shapes.            |
| `dashArray`   | Dash pattern for dashed or dotted lines.   |
| `lineCap`     | Shape used at the end of a line.           |
| `lineJoin`    | Shape used at line corners.                |

The table below lists commonly used options, but it is not exhaustive. CartoLeaf relies on Leaflet's supported path options, so additional Leaflet options may also work depending on the layer type.

For the full list of supported path options, refer to the Leaflet `Path` documentation and the relevant Leaflet layer documentation.

## Circle Styling

Circles support both stroke and fill styling.

```python
from cartoleaf import Circle

circle = Circle(
    lat=1.3521,
    lng=103.8198,
    radius=500,
    popup="Styled circle",
    style={
        "color": "#2879e4",
        "weight": 2,
        "opacity": 0.9,
        "fillColor": "#2879e4",
        "fillOpacity": 0.2,
    },
)
```

## Polygon Styling

Polygons also support both stroke and fill styling.

```python
from cartoleaf import Polygon

polygon = Polygon(
    coordinates=[
        (1.35, 103.81),
        (1.36, 103.82),
        (1.34, 103.83),
    ],
    popup="Styled polygon",
    style={
        "color": "#2879e4",
        "weight": 2,
        "opacity": 0.9,
        "fillColor": "#2879e4",
        "fillOpacity": 0.25,
    },
)
```

## Polyline Styling

Polylines are line-only layers, so fill options do not apply.

```python
from cartoleaf import Polyline

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

## Dashed Polylines

Use `dashArray` to create dashed or dotted lines.

```python
from cartoleaf import Polyline

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

## GeoJSON Styling

GeoJSON layers use the same path style options.

```python
from cartoleaf import GeoJson

geojson = GeoJson(
    data=geojson_data,
    popup_field="name",
    style={
        "color": "#2879e4",
        "weight": 2,
        "opacity": 0.9,
        "fillColor": "#2879e4",
        "fillOpacity": 0.2,
    },
)
```

The style is applied to the GeoJSON layer.

## CSS Color Values

Style values can use any valid CSS color format.

```python
style={
    "color": "blue",
}
```

```python
style={
    "color": "#2879e4",
}
```

```python
style={
    "color": "rgb(40, 121, 228)",
}
```

## Fill Options

Fill options apply to filled shapes such as `Circle`, `Polygon`, and polygon-based `GeoJson` features.

```python
style={
    "fillColor": "#2879e4",
    "fillOpacity": 0.2,
}
```

For `Polyline`, fill options are ignored because a polyline does not have an area.

## Stroke Options

Stroke options control the outline or line.

```python
style={
    "color": "#2879e4",
    "weight": 3,
    "opacity": 0.8,
}
```

These options apply to circles, polygons, polylines, and GeoJSON path features.

## Recommended Defaults

A simple default style:

```python
style={
    "color": "#2879e4",
    "weight": 2,
    "opacity": 0.9,
    "fillColor": "#2879e4",
    "fillOpacity": 0.2,
}
```

A route or path style:

```python
style={
    "color": "#2879e4",
    "weight": 4,
    "opacity": 0.8,
}
```

A dashed boundary style:

```python
style={
    "color": "#2879e4",
    "weight": 3,
    "dashArray": "6, 6",
}
```

## Next Steps

Continue with:

* [Circles](circles.md)
* [Polygons](polygons.md)
* [Polylines](polylines.md)
* [GeoJSON](geojson.md)
* [Events](events.md)

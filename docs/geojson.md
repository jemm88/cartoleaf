# GeoJSON

The `GeoJson` class is used to render GeoJSON data on a CartoLeaf map.

GeoJSON layers are useful when you already have geographic data in GeoJSON format, such as boundaries, regions, districts, zones, or custom shapes.

CartoLeaf currently supports GeoJSON objects with the following top-level types:

* `Feature`
* `FeatureCollection`

## Basic Usage

```python
from cartoleaf import Map, GeoJson

geojson_data = {
    "type": "Feature",
    "properties": {
        "name": "Sample Area"
    },
    "geometry": {
        "type": "Polygon",
        "coordinates": [[
            [103.81, 1.35],
            [103.82, 1.36],
            [103.83, 1.34],
            [103.81, 1.35],
        ]]
    }
}

m = Map(
    center=(1.3521, 103.8198),
    zoom=12,
)

geojson = GeoJson(
    data=geojson_data,
    popup_field="name",
)

m.add_geojson(geojson)

m.save("map.html")
```

## Parameters

| Parameter                 | Type             | Default                 | Description                                                |
| ------------------------- | ---------------- | ----------------------- | ---------------------------------------------------------- |
| `data`                    | `dict[str, Any]` | Required                | GeoJSON data. Must be a `Feature` or `FeatureCollection`.  |
| `popup_field`             | `str \| None`    | `None`                  | Feature property name to use as popup content.             |
| `popup_open_on_hover`     | `bool`           | `False`                 | Opens the popup when the cursor enters a GeoJSON feature.  |
| `popup_close_on_hoverout` | `bool`           | `False`                 | Closes the popup when the cursor leaves a GeoJSON feature. |
| `events`                  | `dict[str, str]` | `{}`                    | Event mapping for supported browser interactions.          |
| `geojson_id`              | `str`            | Auto-generated          | Unique GeoJSON layer identifier.                           |
| `style`                   | `dict[str, Any]` | `POLYGEO_DEFAULT_STYLE` | Leaflet style options applied to the GeoJSON layer.        |

## GeoJSON Coordinate Format

GeoJSON uses longitude and latitude coordinate order:

```python
[lng, lat]
```

Example:

```python
[103.8198, 1.3521]
```

This is different from CartoLeaf `Marker`, `Circle`, `Polygon`, and `Polyline` coordinates, which use:

```python
(lat, lng)
```

This difference follows the GeoJSON standard.

## Feature Example

A single GeoJSON `Feature` can be rendered directly.

```python
geojson_data = {
    "type": "Feature",
    "properties": {
        "name": "Sample Area"
    },
    "geometry": {
        "type": "Polygon",
        "coordinates": [[
            [103.81, 1.35],
            [103.82, 1.36],
            [103.83, 1.34],
            [103.81, 1.35],
        ]]
    }
}
```

Add it to the map:

```python
m.add_geojson(
    GeoJson(
        data=geojson_data,
        popup_field="name",
    )
)
```

## FeatureCollection Example

Most real-world GeoJSON files are `FeatureCollection` objects.

```python
geojson_data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {
                "name": "Area A"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [103.81, 1.35],
                    [103.82, 1.36],
                    [103.83, 1.34],
                    [103.81, 1.35],
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "name": "Area B"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [103.84, 1.31],
                    [103.86, 1.32],
                    [103.85, 1.30],
                    [103.84, 1.31],
                ]]
            }
        }
    ]
}
```

Add it to the map:

```python
m.add_geojson(
    GeoJson(
        data=geojson_data,
        popup_field="name",
    )
)
```

## Property-Based Popups

Use `popup_field` to display a value from each GeoJSON feature's `properties`.

```python
GeoJson(
    data=geojson_data,
    popup_field="name",
)
```

Given this feature:

```json
{
  "type": "Feature",
  "properties": {
    "name": "Central Region"
  },
  "geometry": {
    "type": "Point",
    "coordinates": [103.8198, 1.3521]
  }
}
```

The popup will display:

```text
Central Region
```

If the property is missing from a feature, no popup is bound for that feature.

## Styling GeoJSON Layers

GeoJSON styles follow Leaflet path style options.

```python
geojson = GeoJson(
    data=geojson_data,
    popup_field="name",
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
| `color`       | Stroke color of the feature outline.    |
| `fillColor`   | Fill color of the feature.              |
| `fillOpacity` | Opacity of the feature fill.            |
| `opacity`     | Opacity of the feature outline.         |
| `weight`      | Width of the feature outline in pixels. |

For more details, see [Layer Styling](layer-styling.md).

## Hover Popups

You can configure GeoJSON popups to open when the cursor enters a feature and close when the cursor leaves.

```python
GeoJson(
    data=geojson_data,
    popup_field="name",
    popup_open_on_hover=True,
    popup_close_on_hoverout=True,
)
```

## GeoJSON Events

GeoJSON layers can emit browser events when users interact with features.

```python
GeoJson(
    data=geojson_data,
    events={
        "click": "geojson-clicked",
        "hoverin": "geojson-hovered",
    },
)
```

In the browser, listen for the emitted event:

```html
<script>
window.addEventListener("geojson-clicked", function (event) {
  console.log(event.detail);
});
</script>
```

The emitted event detail includes the GeoJSON layer ID, event type, and feature properties.

## Adding Multiple GeoJSON Layers

Use `add_geojsons()` to add multiple GeoJSON layers at once.

```python
from cartoleaf import Map, GeoJson

m = Map(
    center=(1.3521, 103.8198),
    zoom=12,
)

geojson_layers = [
    GeoJson(
        data=area_a_geojson,
        popup_field="name",
    ),
    GeoJson(
        data=area_b_geojson,
        popup_field="name",
    ),
]

m.add_geojsons(geojson_layers)

m.save("map.html")
```

## Validation

CartoLeaf validates GeoJSON inputs when a `GeoJson` object is created.

The following will raise an error:

```python
GeoJson(
    data={
        "type": "GeometryCollection",
        "geometries": [],
    }
)
```

CartoLeaf currently expects the top-level GeoJSON object to be a `Feature` or `FeatureCollection`.

The following will also raise an error:

```python
GeoJson(
    data=geojson_data,
    popup_field=123,
)
```

`popup_field` must be a string if provided.

## Next Steps

Continue with:

* [Layer Styling](layer-styling.md)
* [Events](events.md)
* [Polygons](polygons.md)
* [Map](map.md)

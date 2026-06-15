# Web Frameworks

CartoLeaf can be used inside server-rendered web applications because it generates normal HTML and JavaScript instead of iframe-based map output.

This makes it suitable for frameworks such as Flask, Django, FastAPI with Jinja2, and other server-rendered Python applications.

## Overview

CartoLeaf maps can be rendered in two main ways:

| Method               | Use case                                                                                |
| -------------------- | --------------------------------------------------------------------------------------- |
| `render()`           | Return the full rendered map as a single HTML string.                                   |
| `render(split=True)` | Split the rendered output into dependencies, map container, scripts, and event helpers. |

For web frameworks, `render(split=True)` is usually preferred because it gives you control over where each part is placed in your template.

## Rendering Parts

When you call:

```python
parts = m.render(split=True)
```

CartoLeaf returns:

```python
{
    "dependencies": "...",
    "map": "...",
    "script": "...",
    "emission": "...",
}
```

| Part           | Where it usually goes | Description                                                          |
| -------------- | --------------------- | -------------------------------------------------------------------- |
| `dependencies` | `<head>`              | Leaflet CSS, Leaflet JavaScript, and optional external dependencies. |
| `map`          | `<body>`              | The map container element.                                           |
| `script`       | End of `<body>`       | JavaScript that creates the Leaflet map and layers.                  |
| `emission`     | End of `<body>`       | JavaScript helpers used for CartoLeaf browser events.                |

## Flask

### Returning the Full Rendered Map

For a simple Flask route, you can return `m.render()` directly.

```python
from flask import Flask
from cartoleaf import Map, Marker

app = Flask(__name__)

@app.route("/")
def index():
    m = Map(
        center=(1.3521, 103.8198),
        zoom=12,
    )

    m.add_marker(
        Marker(
            lat=1.3521,
            lng=103.8198,
            popup="Singapore",
        )
    )

    return m.render()

if __name__ == "__main__":
    app.run(debug=True)
```

This is the simplest approach, but it gives you less control over page layout.

### Using a Flask Template

For normal Flask applications, use `render(split=True)` and pass the parts into your template.

```python
from flask import Flask, render_template
from cartoleaf import Map, Marker

app = Flask(__name__)

@app.route("/")
def index():
    m = Map(
        center=(1.3521, 103.8198),
        zoom=12,
    )

    m.add_marker(
        Marker(
            lat=1.3521,
            lng=103.8198,
            popup="Singapore",
        )
    )

    cartoleaf = m.render(split=True)

    return render_template(
        "index.html",
        cartoleaf=cartoleaf,
    )

if __name__ == "__main__":
    app.run(debug=True)
```

Template:

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>CartoLeaf Flask Example</title>

  {{ cartoleaf.dependencies | safe }}
</head>
<body>
  <h1>Map</h1>

  {{ cartoleaf.map | safe }}

  {{ cartoleaf.script | safe }}
  {{ cartoleaf.emission | safe }}
</body>
</html>
```

## Django

In Django, create the map in your view and pass the rendered parts to the template.

```python
from django.shortcuts import render
from cartoleaf import Map, Marker

def index(request):
    m = Map(
        center=(1.3521, 103.8198),
        zoom=12,
    )

    m.add_marker(
        Marker(
            lat=1.3521,
            lng=103.8198,
            popup="Singapore",
        )
    )

    cartoleaf = m.render(split=True)

    return render(
        request,
        "index.html",
        {
            "cartoleaf": cartoleaf,
        },
    )
```

Template:

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>CartoLeaf Django Example</title>

  {{ cartoleaf.dependencies|safe }}
</head>
<body>
  <h1>Map</h1>

  {{ cartoleaf.map|safe }}

  {{ cartoleaf.script|safe }}
  {{ cartoleaf.emission|safe }}
</body>
</html>
```

## FastAPI with Jinja2

CartoLeaf can also be used with FastAPI and Jinja2 templates.

```python
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from cartoleaf import Map, Marker

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def index(request: Request):
    m = Map(
        center=(1.3521, 103.8198),
        zoom=12,
    )

    m.add_marker(
        Marker(
            lat=1.3521,
            lng=103.8198,
            popup="Singapore",
        )
    )

    cartoleaf = m.render(split=True)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "cartoleaf": cartoleaf,
        },
    )
```

Template:

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>CartoLeaf FastAPI Example</title>

  {{ cartoleaf.dependencies | safe }}
</head>
<body>
  <h1>Map</h1>

  {{ cartoleaf.map | safe }}

  {{ cartoleaf.script | safe }}
  {{ cartoleaf.emission | safe }}
</body>
</html>
```

## Template Placement

A typical template should place CartoLeaf output like this:

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">

  {{ cartoleaf.dependencies | safe }}
</head>
<body>
  {{ cartoleaf.map | safe }}

  {{ cartoleaf.script | safe }}
  {{ cartoleaf.emission | safe }}
</body>
</html>
```

The important point is that the rendered HTML should not be escaped.

In Jinja2-based templates, use:

```html
{{ cartoleaf.map | safe }}
```

Without `| safe`, the generated HTML may appear as text instead of being rendered as HTML.

## Using Events with Frontend Components

CartoLeaf events can be used to connect map interactions to the surrounding page.

Python:

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
        popup="Singapore",
        data={
            "name": "Singapore",
            "description": "Selected location",
        },
        events={
            "click": "location-selected",
        },
    )
)

cartoleaf = m.render(split=True)
```

HTML:

```html
<div id="sidebar">
  <h2 id="location-name">No location selected</h2>
  <p id="location-description"></p>
</div>

{{ cartoleaf.map | safe }}

{{ cartoleaf.script | safe }}
{{ cartoleaf.emission | safe }}

<script>
window.addEventListener("location-selected", function (event) {
  const data = event.detail.data;

  document.getElementById("location-name").textContent = data.name;
  document.getElementById("location-description").textContent = data.description;
});
</script>
```

This pattern can be used to update sidebars, cards, tables, filters, charts, or other frontend components.

## Multiple Maps on One Page

If you render more than one map on the same page, give each map a unique `map_id`.

```python
map_a = Map(
    center=(1.3521, 103.8198),
    zoom=12,
    map_id="map-a",
)

map_b = Map(
    center=(1.3000, 103.8500),
    zoom=12,
    map_id="map-b",
)
```

Each map should have a unique HTML element ID to avoid conflicts.

## Notes

* Use `render(split=True)` for most web framework integrations.
* Place `dependencies` in the page `<head>`.
* Place `map`, `script`, and `emission` in the page body.
* Use `| safe` in Jinja2-style templates so the generated HTML is rendered correctly.
* Use unique `map_id` values when rendering multiple maps on the same page.
* CartoLeaf events can be used to connect map interactions to the surrounding DOM.

## Next Steps

Continue with:

* [Rendering](rendering.md)
* [Events](events.md)
* [Map](map.md)
* [Popups](popups.md)

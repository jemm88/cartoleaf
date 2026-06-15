# Rendering

CartoLeaf generates HTML and JavaScript that can be embedded into a web page or saved as a standalone HTML file.

The `Map` class provides several rendering methods depending on how you want to use the generated map.

## Overview

| Method               | Description                       | Use case                                                           |
| -------------------- | --------------------------------- | ------------------------------------------------------------------ |
| `render()`           | Returns one combined HTML string. | Simple embedding or returning directly from a route.               |
| `render(split=True)` | Returns separate rendered parts.  | Server-rendered templates with separate head/body/script sections. |
| `render_full_html()` | Returns a complete HTML document. | Creating a standalone page manually.                               |
| `save()`             | Writes a complete HTML file.      | Exporting a map to an `.html` file.                                |

## `render()`

Use `render()` to generate the map as a single HTML string.

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
    )
)

html = m.render()
```

This returns the map dependencies, map container, map script, and event emission script as one string.

This is useful when you want to insert the entire rendered map into a page.

## Returning a Map from Flask

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

## `render(split=True)`

Use `render(split=True)` when you need the rendered map split into separate parts.

```python
parts = m.render(split=True)
```

This returns a dictionary:

```python
{
    "dependencies": "...",
    "map": "...",
    "script": "...",
    "emission": "...",
}
```

## Split Rendering Example

```python
parts = m.render(split=True)

dependencies = parts["dependencies"]
map_html = parts["map"]
script = parts["script"]
emission = parts["emission"]
```

This is useful when your web framework separates the page into different sections.

For example:

* dependencies go in `<head>`
* map container goes in `<body>`
* scripts go near the end of `<body>`

## Template Example

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  {{ dependencies | safe }}
</head>
<body>
  {{ map_html | safe }}

  {{ script | safe }}
  {{ emission | safe }}
</body>
</html>
```

## Flask Template Example

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

    parts = m.render(split=True)

    return render_template(
        "index.html",
        dependencies=parts["dependencies"],
        map_html=parts["map"],
        script=parts["script"],
        emission=parts["emission"],
    )
```

Template:

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  {{ dependencies | safe }}
</head>
<body>
  {{ map_html | safe }}

  {{ script | safe }}
  {{ emission | safe }}
</body>
</html>
```

## `render_full_html()`

Use `render_full_html()` to generate a complete standalone HTML document.

```python
html = m.render_full_html(title="My CartoLeaf Map")
```

This includes:

* `<!DOCTYPE html>`
* `<html>`
* `<head>`
* map dependencies
* map container
* map script
* event emission script

Example:

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
    )
)

html = m.render_full_html(title="Singapore Map")
```

## `save()`

Use `save()` to write the map directly to an HTML file.

```python
m.save("map.html")
```

Then open `map.html` in your browser.

Full example:

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
    )
)

m.save("map.html")
```

## Which Rendering Method Should You Use?

Use `save()` if you want the simplest way to create a standalone HTML map.

```python
m.save("map.html")
```

Use `render()` if you want one HTML string.

```python
html = m.render()
```

Use `render(split=True)` if you are integrating CartoLeaf into a server-rendered web app.

```python
parts = m.render(split=True)
```

Use `render_full_html()` if you want a complete HTML document as a string.

```python
html = m.render_full_html()
```

## Rendering Parts

CartoLeaf internally renders a map using four parts.

| Part           | Description                                                   |
| -------------- | ------------------------------------------------------------- |
| `dependencies` | Leaflet CSS/JS and optional external dependencies.            |
| `map`          | The map container element.                                    |
| `script`       | JavaScript used to create the Leaflet map and layers.         |
| `emission`     | JavaScript helpers used for CartoLeaf browser event emission. |

When using `render(split=True)`, these parts are returned separately.

## Notes

* The generated output should be rendered as HTML, not escaped text.
* In template engines such as Jinja2, use `| safe` when inserting rendered CartoLeaf HTML.
* Use `render(split=True)` when you need more control over where dependencies and scripts are placed.
* Use `save()` for the easiest standalone output.

## Next Steps

Continue with:

* [Web Frameworks](web-frameworks.md)
* [Events](events.md)
* [Map](map.md)
* [Quick Start](quickstart.md)

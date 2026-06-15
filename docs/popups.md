# Popups

CartoLeaf supports popups on supported map layers.

Popups can be used to show labels, descriptions, metadata, HTML content, or contextual information when users interact with map objects.

## Supported Layers

Popups are supported on:

* `Marker`
* `Circle`
* `Polygon`
* `Polyline`
* `GeoJson`

## Plain Text Popups

Use `popup` for simple text content.

```python
from cartoleaf import Marker

marker = Marker(
    lat=1.3521,
    lng=103.8198,
    popup="Singapore",
)
```

This creates a normal Leaflet popup with plain text content.

## HTML Popups

Use `popup_html` when you want richer popup content.

Unlike `popup`, which is intended for plain text, `popup_html` allows you to pass custom HTML into the popup. This gives you more freedom over layout, formatting, inline styles, links, buttons, and other HTML elements.

```python
from cartoleaf import Marker

marker = Marker(
    lat=1.3521,
    lng=103.8198,
    popup_html="""
        <div style="width: 180px; color: #000;">
            <h4 style="margin: 0;">Singapore</h4>
            <p style="margin: 4px 0;">Custom popup HTML works.</p>
            <button onclick="alert('Hello from CartoLeaf')">Click me</button>
        </div>
    """,
)
```

This allows the popup content to be styled and structured like normal HTML.

Common uses include:

* formatted titles and descriptions
* buttons
* links
* images
* small tables
* custom inline styles
* frontend event handlers
* richer popup cards

Use `popup_html` when you need more control over how the popup looks or behaves.

Use `popup` when you only need simple plain text.

## Use Either `popup` or `popup_html`

Use either `popup` or `popup_html`, not both.

This will raise an error:

```python
Marker(
    lat=1.3521,
    lng=103.8198,
    popup="Singapore",
    popup_html="<strong>Singapore</strong>",
)
```

Use this instead:

```python
Marker(
    lat=1.3521,
    lng=103.8198,
    popup="Singapore",
)
```

Or this:

```python
Marker(
    lat=1.3521,
    lng=103.8198,
    popup_html="<strong>Singapore</strong>",
)
```

## Marker Popups

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

## Circle Popups

```python
from cartoleaf import Circle

circle = Circle(
    lat=1.3521,
    lng=103.8198,
    radius=500,
    popup="500m radius",
)
```

## Polygon Popups

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

## Polyline Popups

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

## Generating Popup HTML from Templates

`popup_html` accepts a normal Python string containing HTML.

This means you can generate popup content using any Python-based templating approach before passing the rendered HTML into CartoLeaf. This is useful when popup layouts become larger, reusable, or data-driven.

Common examples include:

* Flask with Jinja2
* Django templates
* FastAPI with Jinja2
* Standalone Jinja2 templates
* Any other Python template renderer that returns an HTML string

The general pattern is:

```python
popup_html = render_template_or_string(...)

Marker(
    lat=1.3521,
    lng=103.8198,
    popup_html=popup_html,
)
```

CartoLeaf does not need to know how the HTML was generated. It only receives the final rendered HTML string.

## Example: Reusable Popup Template

Instead of writing popup HTML inline, you can define a reusable popup template.

Example template:

```html
<div style="width: 180px; color: #000;">
  <h4 style="margin: 0;">{{ title }}</h4>
  <p style="margin: 4px 0;">{{ description }}</p>
  <button onclick="alert('{{ button_message }}')">
    {{ button_label }}
  </button>
</div>
```

Then render the template in your Python application and pass the result to `popup_html`.

```python
popup_html = render_template_or_string(
    template_name_or_string,
    title="Singapore",
    description="Custom popup HTML works.",
    button_label="Click me",
    button_message="Hello from CartoLeaf",
)

marker = Marker(
    lat=1.3521,
    lng=103.8198,
    popup_html=popup_html,
)
```

This pattern keeps popup layout separate from map logic.

## Flask Example

In Flask, you can use `render_template()`.

```python
from flask import Flask, render_template
from cartoleaf import Map, Marker

app = Flask(__name__)

@app.route("/")
def index():
    popup_html = render_template(
        "popups/location_popup.html",
        title="Singapore",
        description="Custom popup HTML works.",
        button_label="Click me",
        button_message="Hello from CartoLeaf",
    )

    m = Map(
        center=(1.3521, 103.8198),
        zoom=12,
    )

    m.add_marker(
        Marker(
            lat=1.3521,
            lng=103.8198,
            popup_html=popup_html,
        )
    )

    return m.render()
```

Example popup template:

```text
templates/popups/location_popup.html
```

```html
<div style="width: 180px; color: #000;">
  <h4 style="margin: 0;">{{ title }}</h4>
  <p style="margin: 4px 0;">{{ description }}</p>
  <button onclick="alert('{{ button_message }}')">
    {{ button_label }}
  </button>
</div>
```

## Standalone Jinja2 Example

You can also use Jinja2 directly, even outside a web framework.

```python
from jinja2 import Template
from cartoleaf import Marker

popup_template = Template("""
<div style="width: 180px; color: #000;">
  <h4 style="margin: 0;">{{ title }}</h4>
  <p style="margin: 4px 0;">{{ description }}</p>
  <button onclick="alert('{{ button_message }}')">
    {{ button_label }}
  </button>
</div>
""")

popup_html = popup_template.render(
    title="Singapore",
    description="Custom popup HTML works.",
    button_label="Click me",
    button_message="Hello from CartoLeaf",
)

marker = Marker(
    lat=1.3521,
    lng=103.8198,
    popup_html=popup_html,
)
```

## Django Example

In Django, you can render a template to a string before passing it into `popup_html`.

```python
from django.template.loader import render_to_string
from cartoleaf import Map, Marker

def index(request):
    popup_html = render_to_string(
        "popups/location_popup.html",
        {
            "title": "Singapore",
            "description": "Custom popup HTML works.",
            "button_label": "Click me",
            "button_message": "Hello from CartoLeaf",
        },
    )

    m = Map(
        center=(1.3521, 103.8198),
        zoom=12,
    )

    m.add_marker(
        Marker(
            lat=1.3521,
            lng=103.8198,
            popup_html=popup_html,
        )
    )

    return HttpResponse(m.render())
```

## Why Use Templates for Popups?

Reusable popup templates are useful when:

* multiple markers share the same popup layout
* popup content is generated from database records
* the popup contains several fields
* the popup includes buttons, links, or custom styling
* you want to separate HTML layout from Python map construction

For simple text labels, use `popup`.

For richer or reusable popup layouts, use `popup_html` with a template renderer.

## GeoJSON Popups

GeoJSON layers use `popup_field` instead of `popup` or `popup_html`.

```python
from cartoleaf import GeoJson

geojson = GeoJson(
    data=geojson_data,
    popup_field="name",
)
```

CartoLeaf will look for the `name` field in each GeoJSON feature's `properties`.

For example:

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

## Hover Popups

Popups normally open when the user clicks a map object.

You can also configure popups to open when the cursor enters a map object.

```python
Marker(
    lat=1.3521,
    lng=103.8198,
    popup="Hover popup",
    popup_open_on_hover=True,
)
```

To close the popup when the cursor leaves the object, set `popup_close_on_hoverout=True`.

```python
Marker(
    lat=1.3521,
    lng=103.8198,
    popup="Hover popup",
    popup_open_on_hover=True,
    popup_close_on_hoverout=True,
)
```

This pattern is also supported by circles, polygons, polylines, and GeoJSON layers.

## Multiple Popups

By default, Leaflet closes the current popup when another popup opens.

Set `allow_multiple_popups=True` on the map to allow multiple popups to remain open at the same time.

```python
from cartoleaf import Map

m = Map(
    center=(1.3521, 103.8198),
    zoom=12,
    allow_multiple_popups=True,
)
```

This applies map-level popup behavior.

## Popup Options

Some CartoLeaf layer classes include a `popup_options` parameter.

```python
Marker(
    lat=1.3521,
    lng=103.8198,
    popup="Singapore",
    popup_options={},
)
```

At the moment, `popup_options` is reserved for future popup configuration support. It is included in the public API but may not yet affect rendered popup behavior depending on the layer and template implementation.

## HTML Safety

`popup_html` renders HTML into the generated map.

Only pass trusted HTML content, especially if the popup content comes from user input or external data.

For untrusted content, prefer `popup` instead of `popup_html`.

```python
Marker(
    lat=1.3521,
    lng=103.8198,
    popup="Plain text popup",
)
```

## Choosing Between Popup Types

| Option                    | Use case                                            |
| ------------------------- | --------------------------------------------------- |
| `popup`                   | Simple plain text content.                          |
| `popup_html`              | Rich HTML popup content.                            |
| `popup_field`             | GeoJSON property-based popups.                      |
| `popup_open_on_hover`     | Open popup when cursor enters the object.           |
| `popup_close_on_hoverout` | Close popup when cursor leaves the object.          |
| `allow_multiple_popups`   | Allow multiple popups to stay open on the same map. |

## Notes

* Use `popup` for plain text.
* Use `popup_html` for trusted HTML content.
* Use either `popup` or `popup_html`, not both.
* GeoJSON layers use `popup_field`.
* Hover popup behavior can be enabled with `popup_open_on_hover`.
* `allow_multiple_popups=True` is configured on the `Map`, not individual layers.
* `popup_options` is currently reserved for future popup configuration support.

## Next Steps

Continue with:

* [Markers](markers.md)
* [GeoJSON](geojson.md)
* [Events](events.md)
* [Map](map.md)

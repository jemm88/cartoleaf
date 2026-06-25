# Changelog

## 0.1.2

### Added

- New optional `Map` settings `min_zoom` (minimum zoom level the user can zoom
  out to) and `max_bounds` (geographic bounds, as `((south, west),
  (north, east))`, that the map cannot be panned outside of), plus
  `max_bounds_viscosity` to control how hard the bounds feel. These map to
  Leaflet's `minZoom`, `maxBounds`, and `maxBoundsViscosity` options.

- The Leaflet map instance is now exposed at `window.cartoleaf.maps[map_id]`
  when a map is generated. This makes cartoleaf safe to re-render into the same
  container (for example on an htmx swap): each rendered script tears down any
  existing map on the same `map_id` via `map.remove()` before creating the new
  one, so the old instance is no longer orphaned.
- Each map now carries its own per-map layer registries
  (`map.markers`, `map.circles`, `map.polygons`, `map.polylines`,
  `map.geojsonLayers`) in addition to the existing global `window.cartoleaf.*`
  registries. On teardown the dead map's entries are pruned from the global
  registries so they no longer leak.
- On every render the generated script now also prunes any previously-rendered
  map whose container has left the DOM (for example one replaced by an htmx
  swap), calling `map.remove()` on it and dropping it from
  `window.cartoleaf.maps`. This keeps the registry bounded when rendering maps
  with unique ids — the recommended pattern for swapping maps under htmx, since
  reusing a single fixed `map_id` across a swap can race the outgoing and
  incoming containers and leave the map mis-rendered.

## 0.1.1

### Added

- Significantly expanded documentation.

### Fixed

- `custom_pin_icon` no longer ignores per-call `background_color`/`text_color`
  when multiple icons share the same `name_type`. Instance-varying styles are
  now applied inline instead of in a shared class-scoped `<style>` block.
- Fixed `AttributeError` when rendering a map containing a `Polyline`
  (`points_json` is now serialized correctly).

## 0.1.0

Initial public release.

### Added

- Map generation
- Marker support
- Circle support
- Polygon support
- Polyline support
- GeoJSON support
- Text and HTML popups
- Styling support
- Browser event emission
- `window.cartoleaf` layer references
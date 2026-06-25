# Changelog

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
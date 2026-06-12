from cartoleaf import Map, Marker


m = Map(
    center=(1.3521, 103.8198),
    zoom=12,
)

marker = Marker(
    lat=1.300,
    lng=103.800,
    popup="Property A",
    data={
        "id": 1,
        "name": "Property A",
        "price": 1_500_000,
    },
    events={
        "click": "marker:clicked",
        "hoverin": "marker:hovered",
    },
)

m.add_marker(marker)
m.save("example.html")
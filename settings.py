NE_SCALE=10

OFFLINE_MAP=True

DEFAULT_JS = [
    ("leaflet", 'node_modules/leaflet/dist/leaflet.js'),
    ("jquery", "node_modules/jquery/dist/jquery.min.js"),
    (
        "bootstrap",
        "node_modules/bootstrap/dist/js/bootstrap.bundle.min.js",
    ),
    (
        "awesome_markers",
        "node_modules/leaflet.awesome-markers/dist/leaflet.awesome-markers.min.js",
    ), 
]
DEFAULT_CSS = [
    ("leaflet_css", "node_modules/leaflet/dist/leaflet.css"),
    (
        "bootstrap_css",
        "node_modules/bootstrap/dist/css/bootstrap.min.css",
    ),
    (
        "awesome_markers_font_css",
        "node_modules/fontawesome-free/css/all.min.css",
    ), 
    (
        "awesome_markers_css",
        "node_modules/leaflet.awesome-markers/dist/leaflet.awesome-markers.css",
    ),  
    (
        "awesome_rotate_css",
        "assets/js/leaflet.awesome.rotate.min.css",
    ), 
]

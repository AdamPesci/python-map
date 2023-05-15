# Interactive Map using Folium

This is an interactive map exercise that uses the Folium Python package. The goal is to be able to render an interactive map offline.

## Requirements

### Technologies

- Python
- npm (if you want to easily grab required packages)

### Data

- Natural Earth data: https://www.naturalearthdata.com/downloads/

You'll need the 1:10m scale data.  

Specifically:
            - ocean: ne_10m_ocean.shp
            - gridlines: ne_10m_geographic_lines.shp
            - coasline: ne_10m_coastline.shp
            - minor_islands: 10m/ne_10m_minor_islands.shp

However downloading all the data at once doesn't take long and isn't very big so i'd just download 10m and 50m and place them in the `assets/natural_earth/10m/`  and `assets/natural_earth/50m/` directories respectively.  


## Setup

1. Clone this repository.
2. Create a Python virtual environment using the following command: `python -m venv .venv`
3. Activate the Python virtual environment:
    - For Windows: `.venv\Scripts\activate`
    - For Linux: `source .venv/bin/activate`
4. Install Node.js modules using the following command: `npm install`
6. Run the code as required.

# Config
If you want to use the maps without an internet connection you can update the .config files settings.   
  
The deafults are:
```python
NE_SCALE=10
```
```python
OFFLINE_MAP=False
```
```python
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
```
```python
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
```

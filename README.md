# Interactive Map using Folium

This is an interactive map exercise that uses the Folium Python package. The goal is to be able to render an interactive map offline.

## Requirements

### Technologies

- Python
- npm (if you want to easily grab required packages)

### Data

- Natural Earth data: https://www.naturalearthdata.com/downloads/ The code assumes medium scale 1:50m is used. You'll need the cultural and physical data. Place them in the `assets/natural_earth/50/` directory.

## Setup

1. Clone this repository.
2. Create a Python virtual environment using the following command: `python -m venv .venv`
3. Activate the Python virtual environment:
    - For Windows: `.venv\Scripts\activate`
    - For Linux: `source .venv/bin/activate`
4. Install Node.js modules using the following command: `npm install`
5. Copy `leaflet.awesome.rotate.min.css` into `node_modules/leaflet/dist/`.
6. Run the code as required.

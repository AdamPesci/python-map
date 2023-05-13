import folium
import geopandas as gpd
from uuid import uuid4
from dotenv import dotenv_values
CONFIG = dotenv_values('.config')
SCALE = CONFIG.get('NE_SCALE', '10')


'''
Creates a folium map with geopandas data
'''
def create_map():
    # Read shapefiles for map layers from local files
    ocean = gpd.read_file(f'assets/natural_earth/{SCALE}m/ne_{SCALE}m_ocean.shp')
    gridlines = gpd.read_file(f'assets/natural_earth/{SCALE}m/ne_{SCALE}m_geographic_lines.shp')
    coastline = gpd.read_file(f'assets/natural_earth/{SCALE}m/ne_{SCALE}m_coastline.shp')
    # minor islands only come as 10m
    minor_islands = gpd.read_file(f'assets/natural_earth/10m/ne_10m_minor_islands.shp')

    # Create folium GeoJson objects for each layer with appropriate styles
    layers = [
        folium.GeoJson(
            data=ocean.to_json(),
            style_function=lambda x: {'color': '#a9eafc', 'weight': 0.5},
            name='Ocean', show=True
        ),

        folium.GeoJson(
            data=gridlines.to_json(),
            style_function=lambda x: {
                'color': '#000000', 'weight': 0.5, 'dashArray': '5, 5'},
            name='Gridlines', show=False
        ),
        folium.GeoJson(
            data=coastline.to_json(),
            style_function=lambda x: {'color': '#000000', 'weight': 0.5},
            name='Coastline', show=True
        ),

        folium.GeoJson(
            data=minor_islands.to_json(),
            style_function=lambda x: {'color': '#000000', 'weight': 0.5},
            name='Minor Islands', show=True
        ),
    ]

    # set bounds of map around ocean so user is forced to stay within the map
    sw = ocean.total_bounds[[1, 0]]
    ne = ocean.total_bounds[[3, 2]]
    m = folium.Map(location=[0, 0], tiles=None, zoom_start=1.5, maxBounds=[sw.tolist(), ne.tolist()])
    m.options.update(minZoom=2)

    # Add the layers to the map
    for layer in layers:
        layer.add_to(m)

    # Add a layer control to the map
    folium.LayerControl().add_to(m)
    
    # Override the deafult css and js to local paths if offline map set in config
    if CONFIG.get('OFFLINE_MAP') == 'True':
        override_default_js_css(m)

    return m


'''
Overrides the default js/css paths
'''
def override_default_js_css(m):
    for i, (name, _) in enumerate(m.default_js):
            if name == 'leaflet':
                link = CONFIG['LEAFLET_JS']
            elif name == 'jquery':
                link = CONFIG['JQUERY_JS']
            elif name == 'bootstrap':
                link = CONFIG['BOOTSTRAP_JS']
            elif name == 'awesome_markers':
                link = CONFIG['AWESOME_MARKERS_JS']
            m.default_js[i] = (name, link)

    # bootstrap3 glyphicons not required with bootstrap5
    gli_index = 0
    for i, (name, _) in enumerate(m.default_css):
        if name == 'leaflet_css':
            link = CONFIG['LEAFLET_CSS']
        elif name == 'bootstrap_css':
            link = CONFIG['BOOTSTRAP_CSS']
        elif name == 'glyphicons_css':
            gli_index = i
        elif name == 'awesome_markers_font_css':
            link = CONFIG['FONTAWESOME_FREE_CSS']
        elif name == 'awesome_markers_css':
            link = CONFIG['AWESOME_MARKERS_CSS']
        elif name == 'awesome_rotate_css':
            link = CONFIG['AWESOME_ROTATE_CSS']
        m.default_css[i] = (name, link)
    m.default_css.pop(gli_index)
    
def main():
    m = create_map()
    m.save(f'map_{uuid4()}.html')
        
if __name__ == '__main__':
    main()

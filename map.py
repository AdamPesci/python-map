import folium
import geopandas as gpd
from uuid import uuid4
import settings




'''
Creates a folium map with geopandas data
'''
def create_map():
    scale = settings.NE_SCALE
    # Read shapefiles for map layers from local files
    ocean = gpd.read_file(f'assets/natural_earth/{scale}m/ne_{scale}m_ocean.shp')
    gridlines = gpd.read_file(f'assets/natural_earth/{scale}m/ne_{scale}m_geographic_lines.shp')
    coastline = gpd.read_file(f'assets/natural_earth/{scale}m/ne_{scale}m_coastline.shp')
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
    if settings.OFFLINE_MAP:
        m.default_css = settings.DEFAULT_CSS
        m.default_js = settings.DEFAULT_JS

    return m
    
def main():
    m = create_map()
    m.save(f'map_{uuid4()}.html')
        
if __name__ == '__main__':
    main()

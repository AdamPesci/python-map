import folium
import geopandas as gpd
import random
import re
import glob
from uuid import uuid4

'''
Replace cdn links with using static paths
'''
def static_replace_with_local(html_string):
    # Replace external references with local ones (allows user to manually change if replace with local doesnt work)
    replacements = {
        "https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/leaflet.js": "assets/leaflet.js",
        "https://code.jquery.com/jquery-1.12.4.min.js": "assets/jquery.min.js",
        "https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/js/bootstrap.bundle.min.js": "assets/bootstrap.bundle.min.js",
        "https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.js": "assets/leaflet.awesome-markers.js",
        "https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/leaflet.css": "assets/leaflet.css",
        "https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css": "assets/bootstrap.min.css",
        "https://netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css": "assets/bootstrap-3.0.0.min.css",
        "https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.2.0/css/all.min.css": "assets/fontawesome-free-6.2.0.min.css",
        "https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.css": "assets/leaflet.awesome-markers.css",
        "https://cdn.jsdelivr.net/gh/python-visualization/folium/folium/templates/leaflet.awesome.rotate.min.css": "assets/leaflet.awesome.rotate.min.css",
    }

    for external, local in replacements.items():
        html_string = html_string.replace(external, local)

    return html_string

'''
Replace cdn links using regex and node modules
'''
def replace_with_local_wrapper(html_string, static):
    # Replace external references with local ones
    
    if static:
        return static_replace_with_local(html_string)
    
    html_string = re.sub(
        r"https://[^/]+/([^/]+/)*([^/]+?)(\.js|\.css)", replace_with_local, html_string
    )
    return html_string

def replace_with_local(match):
    patterns_to_local = {
        r"leaflet(?!\.awesome-markers)": "node_modules/leaflet",
        r"jquery": "node_modules/jquery",
        r"bootstrap": "node_modules/bootstrap",
        r"Leaflet\.awesome-markers": "node_modules/leaflet.awesome-markers",
        r"@fortawesome/fontawesome-free": "node_modules/fontawesome-free",
    }

    for pattern, local_path in patterns_to_local.items():
        if re.search(pattern, match.group(0)):
            local_path_versions = glob.glob(f"{local_path}@*/")
            if not local_path_versions:
                local_path_versions = glob.glob(f"{local_path}*/")

            local_path_version = local_path_versions[0]

            folder = "dist"
            subfolder = ""
            if pattern == r"jquery":
                folder = "dist"
                file_name = "jquery.min.js"
            elif pattern == r"bootstrap":
                folder = "dist"
                subfolder = "js" if ".js" in match.group(0) else "css"
                file_name = match.group(0).rsplit("/", 1)[-1]
                if subfolder == "js" and file_name.endswith(".css"):
                    subfolder = "css"
            elif pattern == r"Leaflet\.awesome-markers":
                folder = "dist"
                file_name = match.group(0).rsplit("/", 1)[-1]
            elif pattern == r"@fortawesome/fontawesome-free":
                folder = "css"
                file_name = "all.min.css"
            elif pattern == r"leaflet(?!\.awesome-markers)":
                folder = "dist"
                file_name = match.group(0).rsplit("/", 1)[-1]

            return f"{local_path_version}{folder}/{subfolder}/{file_name}" if subfolder else f"{local_path_version}{folder}/{file_name}"

    return match.group(0)

'''
Creates a folium map with geopandas data
'''
def create_map():
    # Read shapefiles for map layers from local files
    countries = gpd.read_file("assets/natural_earth/50m/ne_50m_admin_0_countries.shp")
    ocean = gpd.read_file("assets/natural_earth/50m/ne_50m_ocean.shp")
    gridlines = gpd.read_file("assets/natural_earth/50m/ne_50m_geographic_lines.shp")
    # rivers = gpd.read_file("assets/natural_earth/50m/ne_50m_rivers_lake_centerlines.shp")
    # lakes = gpd.read_file("assets/natural_earth/50m/ne_50m_lakes.shp")

    # Define color palette for countries
    color_palette = [
        "#e6e6e6", "#f5b897", "#c5e5a4", "#b3d0d8", "#f0e1a1", "#f3c29d", "#c5d9a5",
        "#d4c6a2", "#b3d0d8", "#d4c6a2", "#c5d9a5", "#d4c6a2", "#f0e1a1"
    ]

    # Assign random colors to each country
    countries['color'] = [random.choice(color_palette) for _ in range(len(countries))]


     # Create folium GeoJson objects for each layer with appropriate styles
    style = {"color": "#000000", "weight": 1, "fillOpacity": 0.7}
    countries_json = folium.GeoJson(
        data=countries.to_json(),
        style_function=lambda x: dict(style, fillColor=x['properties']['color']),
        name='Countries', show=True
    )

    ocean_json = folium.GeoJson(
        data=ocean.to_json(),
        style_function=lambda x: {"color": "#a9eafc", "weight": 0.5},
        name='Ocean', show=True
    )

    lines_json = folium.GeoJson(
        data=gridlines.to_json(),
        style_function=lambda x: {"color": "#000000", "weight": 0.5, "dashArray": "5, 5"},
        name='Gridlines', show=False
    )

    # rivers_json = folium.GeoJson(
    #     data=rivers.to_json(),
    #     style_function=lambda x: {"color": "#a9eafc", "weight": 0.5},
    #     name='Rivers', show=False
    # )

    # lakes_json = folium.GeoJson(
    #     data=lakes.to_json(),
    #     style_function=lambda x: {"color": "#a9eafc", "weight": 0.5},
    #     name='Lakes', show=False
    # )

    # Create a folium map and add layers to it
    sw = countries.total_bounds[[1, 0]]
    ne = countries.total_bounds[[3, 2]]
    m = folium.Map(location=[0, 0], tiles=None, zoom_start=1.5, maxBounds=[sw.tolist(), ne.tolist()])
    m.options.update(minZoom=2)
    
    
    # Add the layers to the map
    for layer in [countries_json, ocean_json, lines_json]:
        layer.add_to(m)
    
    # Add a layer control to the map
    folium.LayerControl().add_to(m)

    return m

'''
Saves the folium map as an HTML file
'''   
def save_map_as_html(m, save_as=None, static=False):
    out_path = save_as if save_as else f'map_{uuid4()}.html'
    html_string = replace_with_local_wrapper(m.get_root().render(), static)
    with open(out_path, "w") as f:
        f.write(html_string)
    
def main():
    m = create_map()
    save_map_as_html(m)
    
if __name__ == '__main__':
    main()


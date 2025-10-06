
from flask import Flask, render_template_string
import pandas as pd, os, folium

app = Flask(__name__)
TEMPLATE = '''
<!doctype html>
<title>UVI Dashboard - Los Angeles (Demo)</title>
<h1>Urban Vitality Index - Los Angeles (Demo)</h1>
<p>Layers: NDVI (Landsat), LST (MODIS/VIIRS), NO2 (Sentinel-5P), Precipitation (GPM), Soil Moisture (SMAP), DEM.</p>
{% if map_html %}
{{ map_html|safe }}
{% else %}
<p>No map generated. Run data pipeline to populate outputs/indices and outputs/map.html</p>
{% endif %}
'''

@app.route('/')
def index():
    map_fp = os.path.join('outputs','map.html')
    if os.path.exists(map_fp):
        with open(map_fp,'r',encoding='utf-8') as f:
            map_html = f.read()
        return render_template_string(TEMPLATE, map_html=map_html)
    return render_template_string(TEMPLATE, map_html=None)

if __name__=='__main__':
    app.run(debug=True)

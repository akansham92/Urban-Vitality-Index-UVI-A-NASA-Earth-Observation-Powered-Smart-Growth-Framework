
# Sentinel-5P NO2 (TROPOMI) - Access Instructions

Sentinel-5P (TROPOMI) Level 2/3 NO2 products are available via:
- Copernicus Open Access Hub (https://scihub.copernicus.eu/) - requires registration
- Google Earth Engine (dataset id: COPERNICUS_S5P_OFFL_L3_NO2) - requires Earth Engine account
- Some derived L3 NO2 products are accessible via public cloud or through the Copernicus Data Space

Recommended options:
1. Use Google Earth Engine Python API to fetch NO2 rasters for the LA bbox. (Requires GEE signup: https://earthengine.google.com/)
2. Register for Copernicus Open Access Hub and use `sentinelsat` to download Level-2 products and reproject to your grid.

This repo includes an example notebook showing how to load COPERNICUS_S5P_OFFL_L3_NO2 via Earth Engine (user must authenticate).

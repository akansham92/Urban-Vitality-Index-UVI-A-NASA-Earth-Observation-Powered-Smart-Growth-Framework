
# Urban Vitality Index (UVI) - Real Project (Los Angeles)

This repository implements the Urban Vitality Index for **Los Angeles** using publicly-available Earth observation datasets (Option B: public cloud & data portals). The code automates data discovery and download (where possible via public cloud), computes environmental indices (NDVI, LST proxy), ingests air quality and precipitation, and produces a notebook + Flask dashboard combining all layers.

Important: many satellite products are large. The scripts are designed to download **only the tiles overlapping a user-provided bounding box** (Los Angeles by default). Some data sources require an account (Copernicus / Earthdata) — instructions are provided.


## Datasets & Public Endpoints used (links)

- Landsat Collection 2 (AWS public datasets)
  - https://registry.opendata.aws/usgs-landsat/  (Landsat on AWS)
- MODIS LST (MOD11A1) via Google Cloud / public catalogs (Earth Engine catalog link)
  - https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MOD11A1
- VIIRS (VNP09 / VNP21) via NASA LP DAAC / NOAA product catalogs
  - https://www.earthdata.nasa.gov/data/instruments/viirs
- Sentinel-5P (NO2) - Copernicus Open Data / Google Earth Engine catalog
  - https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S5P_OFFL_L3_NO2
  - Copernicus Hub: https://scihub.copernicus.eu/ (registration required for direct downloads)
- SMAP (soil moisture) - NSIDC DAAC (instructions)
  - https://nsidc.org/data/smap
- GPM IMERG (precipitation) - AWS & NASA GES DISC Registry
  - https://registry.opendata.aws/nasa-gpm3imergdf/
- DEM / SRTM (elevation) - OpenTopography / USGS / AWS
  - https://portal.opentopography.org/  and https://registry.opendata.aws/

See `docs/dataset_links.md` for clickable links and notes.

## Quickstart (high-level)

1. Create environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Configure optional cloud clients:
   - AWS CLI (for S3 public reads): `aws configure` (anonymous reads generally work for public datasets)
   - Google Cloud SDK (if using GCS public datasets): `gcloud init` (anonymous reads may work for public buckets)
   - Copernicus / Earthdata: see `docs/credentials.md` if you want to download Sentinel-5P or LP DAAC products requiring authentication.

3. Run data discovery + download (small test mode downloads minimal tiles):
   ```bash
   python data/landsat_download.py --bbox -118.67 33.70 -118.15 34.34 --out_dir data/landsat --max-scenes 10
   python data/gpm_download.py --bbox -118.67 33.70 -118.15 34.34 --out_dir data/gpm --start 2023-07-01 --end 2023-07-31
   python data/modis_download.py --bbox -118.67 33.70 -118.15 34.34 --out_dir data/modis --start 2023-07-01 --end 2023-07-31
   # Sentinel-5P and SMAP scripts provide guided downloads and metadata instructions.
   ```

4. Compute indices & train model:
   ```bash
   python processing/compute_indices.py --landsat_dir data/landsat --modis_dir data/modis --gpm_dir data/gpm --out_dir outputs/indices
   python modeling/train_model.py --indices_dir outputs/indices --out_dir outputs/model
   ```

5. Generate notebook report and run dashboard:
   ```bash
   jupyter lab notebooks/UVI_LA_report.ipynb
   export FLASK_APP=app/dashboard.py
   flask run
   ```

---
This package is designed to be reproducible and uses public cloud datasets where possible. For any dataset that requires credentials (Copernicus / Earthdata), the repo includes exact steps to obtain tokens and how to plug them into the scripts.


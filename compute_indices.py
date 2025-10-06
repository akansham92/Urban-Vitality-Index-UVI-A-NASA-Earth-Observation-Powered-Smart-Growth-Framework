
#!/usr/bin/env python3
"""Compute NDVI, aggregate LST proxies, and combine layers into a per-tile index.

This script expects:

- Landsat SR bands (red=NIR band 4/5 depending on sensor) in data/landsat
- MODIS/VIIRS LST in data/modis or data/viirs
- GPM IMERG netCDF files in data/gpm
- SRTM DEM in data/dem (optional)
"""
import os, glob, rasterio, numpy as np, pandas as pd, xarray as xr
from rasterio.enums import Resampling

def compute_ndvi(red_fp, nir_fp, out_fp=None):
    with rasterio.open(red_fp) as r:
        red = r.read(1).astype('float32')
        profile = r.profile
    with rasterio.open(nir_fp) as r:
        nir = r.read(1).astype('float32')
    ndvi = (nir - red) / (nir + red + 1e-6)
    if out_fp:
        profile.update(dtype='float32', count=1)
        with rasterio.open(out_fp,'w',**profile) as dst:
            dst.write(ndvi.astype('float32'),1)
    return ndvi, profile

def aggregate_gpm_daily(gpm_dir):
    # placeholder: read netCDFs and average precipitation across period
    files = glob.glob(os.path.join(gpm_dir,'*.nc4')) + glob.glob(os.path.join(gpm_dir,'*.nc'))
    if not files:
        print('No GPM files found in', gpm_dir)
        return None
    ds = xr.open_mfdataset(files, combine='by_coords')
    # Many IMERG files contain precipitation variable 'precipitationCal' or similar
    var = None
    for name in ['precipitationCal','precipitation','precipitationCal']: 
        if name in ds.variables:
            var = ds[name]
            break
    if var is None:
        print('No precipitation variable found in GPM files.')
        return None
    mean_precip = var.mean(dim='time', skipna=True)
    return mean_precip

def main(landsat_dir='data/landsat', modis_dir='data/modis', gpm_dir='data/gpm', out_dir='outputs/indices'):
    os.makedirs(out_dir, exist_ok=True)
    # find red/nir pairs (simple heuristic)
    red_files = sorted(glob.glob(os.path.join(landsat_dir,'*B4*.TIF')) + glob.glob(os.path.join(landsat_dir,'*band4*.TIF')) + glob.glob(os.path.join(landsat_dir,'*sr_band4*.TIF')))
    nir_files = sorted(glob.glob(os.path.join(landsat_dir,'*B5*.TIF')) + glob.glob(os.path.join(landsat_dir,'*band5*.TIF')) + glob.glob(os.path.join(landsat_dir,'*sr_band5*.TIF')))
    pairs = list(zip(red_files, nir_files))
    rows = []
    for red_fp, nir_fp in pairs:
        ndvi, profile = compute_ndvi(red_fp, nir_fp)
        rows.append({'file': os.path.basename(red_fp), 'ndvi_mean': float(np.nanmean(ndvi)), 'ndvi_std': float(np.nanstd(ndvi))})
    # aggregate GPM
    gpm_mean = aggregate_gpm_daily(gpm_dir)
    if gpm_mean is not None:
        # Save placeholder
        pass
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(out_dir,'landsat_ndvi_summary.csv'), index=False)
    print('Wrote indices to', out_dir)

if __name__=='__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--landsat_dir', default='data/landsat')
    p.add_argument('--modis_dir', default='data/modis')
    p.add_argument('--gpm_dir', default='data/gpm')
    p.add_argument('--out_dir', default='outputs/indices')
    args = p.parse_args()
    main(args.landsat_dir, args.modis_dir, args.gpm_dir, args.out_dir)

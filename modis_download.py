
#!/usr/bin/env python3
"""MODIS MOD11A1 LST downloader (via Google Cloud public dataset or Earthdata).

This script demonstrates how to locate MOD11A1 files for a date range. For Google Cloud access, you can use the public bucket if available; otherwise follow Earthdata instructions.
"""
import os, argparse, datetime, requests
def main(bbox, out_dir, start, end):
    os.makedirs(out_dir, exist_ok=True)
    print('This script provides instructions and a placeholder for downloading MODIS LST (MOD11A1).')
    print('MODIS MOD11A1 is available via Google Earth Engine catalog and sometimes as public GCS datasets.')
    print('For automated download, consider using the LP DAAC API or the Google Cloud public dataset (gcp-public-data-modis).')
if __name__=='__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--bbox', nargs=4, type=float, default=[-118.67,33.70,-118.15,34.34])
    p.add_argument('--out_dir', default='data/modis')
    p.add_argument('--start', default='2023-07-01')
    p.add_argument('--end', default='2023-07-31')
    args = p.parse_args()
    main(args.bbox, args.out_dir, args.start, args.end)

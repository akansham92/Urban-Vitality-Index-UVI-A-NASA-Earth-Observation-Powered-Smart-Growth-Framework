
#!/usr/bin/env python3
"""Download GPM IMERG aggregated files from the AWS Public dataset (registry.opendata.aws/nasa-gpm3imergdf).

This script will list objects for a date range and download netCDF files intersecting the bbox. For large download use cloud processing.
"""
import os, argparse, boto3, botocore, datetime
from shapely.geometry import box
import rasterio.features, json

def list_objects_for_day(s3, bucket, prefix):
    resp = s3.list_objects_v2(Bucket=bucket, Prefix=prefix, MaxKeys=1000)
    return [o['Key'] for o in resp.get('Contents', [])]

def download_imerg(bbox, out_dir, start, end):
    s3 = boto3.client('s3', config=boto3.session.Config(signature_version='unsigned'))
    bucket = 'nasa-gpm3imergdf'
    os.makedirs(out_dir, exist_ok=True)
    cur = start
    while cur <= end:
        key = f'V07/IMERGDF/1.0/{cur.year:04d}/{cur.month:02d}/{cur.day:02d}/3B-DAY.MS.MRG.3IMERG.{cur.year:04d}{cur.month:02d}{cur.day:02d}-S000000-E235959.V07.nc4'
        try:
            outpath = os.path.join(out_dir, os.path.basename(key))
            s3.download_file(bucket, key, outpath)
            print('Downloaded', outpath)
        except botocore.exceptions.ClientError as e:
            print('Not found on S3 for', cur, e)
        cur += datetime.timedelta(days=1)

if __name__=='__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--bbox', nargs=4, type=float, default=[-118.67,33.70,-118.15,34.34])
    p.add_argument('--out_dir', default='data/gpm')
    p.add_argument('--start', type=lambda s: __import__('datetime').datetime.strptime(s,'%Y-%m-%d').date(), default='2023-07-01')
    p.add_argument('--end', type=lambda s: __import__('datetime').datetime.strptime(s,'%Y-%m-%d').date(), default='2023-07-31')
    args = p.parse_args()
    download_imerg(args.bbox, args.out_dir, args.start, args.end)

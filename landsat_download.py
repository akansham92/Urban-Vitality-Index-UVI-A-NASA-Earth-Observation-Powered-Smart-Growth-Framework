
#!/usr/bin/env python3
"""Landsat Collection 2 discovery & download using STAC (USGS/Collection2 STAC).

This script uses pystac-client to search scenes overlapping a bbox and downloads selected bands from the AWS-hosted assets.
"""
import os, argparse, requests, math
from pystac_client import Client
from rasterio.session import AWSSession
import boto3

def download_asset(url, out_path):
    # simple HTTP GET. For S3 https://... you can use requests or boto3 with unsigned config.
    if url.startswith('s3://'):
        # use boto3 to download public S3 object
        import boto3
        s3 = boto3.client('s3', config=boto3.session.Config(signature_version='unsigned'))
        parts = url.replace('s3://','').split('/',1)
        bucket, key = parts[0], parts[1]
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        s3.download_file(bucket, key, out_path)
    else:
        resp = requests.get(url, stream=True)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path,'wb') as f:
            for chunk in resp.iter_content(1024*1024):
                if chunk:
                    f.write(chunk)

def main(bbox, out_dir, max_scenes=5):
    os.makedirs(out_dir, exist_ok=True)
    # STAC endpoint (USGS landsat STAC)
    stac_url = 'https://cmr.earthdata.nasa.gov/stac/Landsat'  # fallback; some providers have different endpoints
    try:
        client = Client.open('https://earth-search.aws.element84.com/v0')  # Earth Search STAC (works for many public datasets)
    except Exception as e:
        print('Failed to open STAC client:', e)
        return
    # search for Landsat Collection 2 scenes
    search = client.search(collections=['landsat-8-c2-l2'], bbox=bbox, limit=max_scenes)
    items = list(search.get_items())
    print(f'Found {len(items)} scenes')
    for it in items:
        properties = it.to_dict().get('properties',{})
        scene_id = properties.get('landsat:scene_id', properties.get('scene_id', 'scene'))
        print('Scene:', scene_id)
        # choose common surface reflectance bands (red, nir) and 'pixel_qa' if available, and 'sr_band' assets which may live on s3
        for asset_key, asset in it.assets.items():
            href = asset.get('href')
            if href and any(k in asset_key.lower() for k in ['sr_band_4','sr_band_5','red','nir','band4','band5','sr_band']):
                out_path = os.path.join(out_dir, os.path.basename(href))
                print('Downloading', href, '->', out_path)
                try:
                    download_asset(href, out_path)
                except Exception as e:
                    print('Download failed', e)
    print('Done.')
if __name__=='__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--bbox', nargs=4, type=float, default=[-118.67,33.70,-118.15,34.34], help='minx miny maxx maxy')
    p.add_argument('--out_dir', default='data/landsat')
    p.add_argument('--max_scenes', type=int, default=5)
    args = p.parse_args()
    main(args.bbox, args.out_dir, args.max_scenes)

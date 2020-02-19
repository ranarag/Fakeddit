import argparse
import pandas as pd
import os
from tqdm import tqdm as tqdm
import urllib.request
import numpy as np
import sys

def url_downloader(image_url, image_path, retries=5):
  downloaded = False
  while retries > 0:
    try:
      urllib.request.urlretrieve(image_url, image_path)
      downloaded = True
    except:
      retries -= 1
      continue
    else:
      break
  return downloaded
      
    
parser = argparse.ArgumentParser(description='r/Fakeddit image downloader')

parser.add_argument('type', type=str, help='train, validate, or test')

args = parser.parse_args()

df = pd.read_csv(args.type, sep="\t")
df = df.replace(np.nan, '', regex=True)
df.fillna('', inplace=True)

pbar = tqdm(total=len(df))

if not os.path.exists("images"):
  os.makedirs("images")
for index, row in df.iterrows():
  if row["hasImage"] == True and row["image_url"] != "" and row["image_url"] != "nan":
    image_url = row["image_url"]
    image_path = "images/" + row["id"] + ".jpg"
    if os.path.exists(image_path):
      continue
    if not url_downloader(image_url, image_path):
      print("Download failed for url {}".format(image_url))    
  pbar.update(1)
print("done")

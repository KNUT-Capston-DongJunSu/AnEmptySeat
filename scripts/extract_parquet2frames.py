import pandas as pd
from PIL import Image
import io, os

scenes = ['train']

for scene in scenes:
    df = pd.read_parquet(f'../IndoorCrowd/mot/{scene}-00000-of-00001.parquet')
    out_dir = f'../data/images/frames_{scene}'
    os.makedirs(out_dir, exist_ok=True)

    for i, row in df.iterrows():
        img_bytes = row['image']['bytes']
        img = Image.open(io.BytesIO(img_bytes))
        img.save(f'{out_dir}/frame_{i:05d}.jpg')
    
    print(f'{scene} 완료: {len(df)}프레임')
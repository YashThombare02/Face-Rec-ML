import os
from PIL import Image
import pandas as pd

IMAGE_DIR = "data"   # change if your images are elsewhere

rows = []

for root, _, files in os.walk(IMAGE_DIR):
    for file in files:
        if file.lower().endswith((".png", ".jpg", ".jpeg")):
            path = os.path.join(root, file)
            try:
                with Image.open(path) as img:
                    width, height = img.size
                    rows.append({
                        "filename": file,
                        "path": path,
                        "width": width,
                        "height": height,
                        "size_kb": round(os.path.getsize(path) / 1024, 2),
                        "format": img.format
                    })
            except Exception as e:
                rows.append({
                    "filename": file,
                    "path": path,
                    "width": None,
                    "height": None,
                    "size_kb": 0,
                    "format": "CORRUPTED"
                })

df = pd.DataFrame(rows)
df.to_csv("image_metadata.csv", index=False)

print("✅ image_metadata.csv generated")

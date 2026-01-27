import os
import csv
from PIL import Image

IMAGE_DIR = "data"
OUTPUT_FILE = "data/image_metadata.csv"

rows = []
rows.append(["filename", "width", "height", "format", "size_kb"])

for root, _, files in os.walk(IMAGE_DIR):
    for file in files:
        if file.lower().endswith((".png", ".jpg", ".jpeg")):
            filepath = os.path.join(root, file)

            try:
                with Image.open(filepath) as img:
                    width, height = img.size
                    img_format = img.format
                    size_kb = round(os.path.getsize(filepath) / 1024, 2)

                    rows.append([
                        file,
                        width,
                        height,
                        img_format,
                        size_kb
                    ])
            except Exception as e:
                print(f"Skipping file {file}: {e}")

# Write CSV
os.makedirs("data", exist_ok=True)

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print("image_metadata.csv generated successfully")

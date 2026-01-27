import os
import cv2
import pandas as pd

IMAGE_DIR = "subjects_photos"

def generate_metadata():
    records = []

    for root, dirs, files in os.walk(IMAGE_DIR):
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                path = os.path.join(root, file)

                try:
                    img = cv2.imread(path)
                    if img is None:
                        continue

                    height, width, _ = img.shape
                    size_kb = round(os.path.getsize(path) / 1024, 2)
                    ext = os.path.splitext(file)[1].replace(".", "").upper()

                    records.append({
                        "filename": file,
                        "width": width,
                        "height": height,
                        "size_kb": size_kb,
                        "format": ext
                    })

                except Exception as e:
                    print(f"❌ Failed processing {path}: {e}")

    df = pd.DataFrame(records)

    # ✅ Force CSV to be saved in project root
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CSV_PATH = os.path.join(BASE_DIR, "image_metadata.csv")

    df.to_csv(CSV_PATH, index=False)
    print(f" image_metadata.csv saved at: {CSV_PATH}")


if __name__ == "__main__":
    generate_metadata()

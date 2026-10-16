

import numpy as np
import py5
from PIL import Image
from pathlib import Path

mask_preview = None


IMAGE_PATH = Path(__file__).parent / "images" / "Girl-with-a-Pearl.jpg"

def settings():
    py5.size(500, 620)

def setup():
   global mask_preview
   img_pixels = np.array(Image.open(IMAGE_PATH).convert("L"), dtype=np.uint8)
   grey_pixels = img_pixels.astype(np.float32) / 255.0
   threshold = 0.5  # Adjust this to control the threshold for the image layer
   masked_pixels = grey_pixels >= threshold
   print(masked_pixels.sum(), "of", grey_pixels.size, "pixels are above the threshold.")
   mask_pixels = masked_pixels.astype(np.uint8) * 255
   mask_preview = py5.create_image_from_numpy(mask_pixels, bands="L")

def draw():
    py5.background(35)
    if mask_preview is not None:
        py5.image(mask_preview, 10, 10, py5.width-20, py5.height-20)



if __name__ == "__main__":
    py5.run_sketch()
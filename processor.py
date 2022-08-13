import os
from PIL import Image
import time
images = []

import cv2
import numpy as np

mangas = os.listdir("downloads")

for manga in mangas:

    print("processing manga: " + manga)

    time.sleep(1)

    imagefiles = os.listdir(f"downloads/{manga}")

    imagelen = len(imagefiles)

    print("Cropping images...")

    import cropper

    for i in range(1, imagelen):
        try:
            
            print("Processing image " + str(i))
            image = cv2.imread(str(f"downloads/{manga}/{i}.png"))
            height, width = image.shape[0:2]
            image_preprocessed = cropper.preproces_image(image)
            edges = cropper.find_edges(image_preprocessed)
            (x_min, x_max), (y_min, y_max) = cropper.adapt_edges(
                edges, height=height, width=width
            )
            image_cropped = image[x_min:x_max, y_min:y_max]
            cv2.imwrite(str(f"downloads/{manga}/{i}.png"), image_cropped)
        except:
            print("Error processing image " + str(i))
            continue

    print("Done! Beggining to append to pdf...")

    for i in range(1, imagelen):
        print("Opening image " + str(i))
        images.append(Image.open(f"downloads/{manga}/{i}.png"))


    pdf_path = manga + ".pdf"

    print("Saving to pdf    ")
    images[0].save(
        pdf_path, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:]
    )
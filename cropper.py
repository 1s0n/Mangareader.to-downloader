# Taken from https://codereview.stackexchange.com/questions/212391/trimming-blank-space-from-images
import cv2
import numpy as np

def preproces_image(
    image,
    *,
    kernel_size=15,
    crop_side=50,
    blocksize=35,
    constant=15,
    max_value=255,
):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    bit = cv2.bitwise_not(gray)
    image_adapted = cv2.adaptiveThreshold(
        src=bit,
        maxValue=max_value,
        adaptiveMethod=cv2.ADAPTIVE_THRESH_MEAN_C,
        thresholdType=cv2.THRESH_BINARY,
        blockSize=blocksize,
        C=constant,
    )
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    erosion = cv2.erode(image_adapted, kernel, iterations=2)
    return erosion[crop_side:-crop_side, crop_side:-crop_side]

def find_edges(image_preprocessed, *, bw_threshold=150, limits=(0.2, 0.15)):
    mask = image_preprocessed < bw_threshold
    edges = []
    for axis in (1, 0):
        count = mask.sum(axis=axis)
        limit = limits[axis] * image_preprocessed.shape[axis]
        index_ = np.where(count >= limit)
        _min, _max = index_[0][0], index_[0][-1]
        edges.append((_min, _max))
    return edges


def adapt_edges(edges, *, height, width):
    (x_min, x_max), (y_min, y_max) = edges
    x_min2 = x_min
    x_max2 = x_max + min(250, (height - x_max) * 10 // 11)
    # could do with less magic numbers
    y_min2 = max(0, y_min)
    y_max2 = y_max + min(250, (width - y_max) * 10 // 11)
    return (x_min2, x_max2), (y_min2, y_max2)

if __name__ == "__main__":

    filename_in = "9.png"
    filename_out = "new9.png"

    image = cv2.imread(str(filename_in))
    height, width = image.shape[0:2]
    image_preprocessed = preproces_image(image)
    edges = find_edges(image_preprocessed)
    (x_min, x_max), (y_min, y_max) = adapt_edges(
        edges, height=height, width=width
    )
    image_cropped = image[x_min:x_max, y_min:y_max]
    cv2.imwrite(str(filename_out), image_cropped)
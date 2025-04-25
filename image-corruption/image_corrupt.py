import cv2
import os
# from imquality import brisque
from brisque import BRISQUE

import traceback
import multiprocessing

obj = BRISQUE(url=False)

def is_image_corrupted_with_brisque(image_path, threshold=50, use_bottom=False):
    """
    Returns True if the image is likely corrupted or low-quality based on BRISQUE score.
    """
    try:
        img = cv2.imread(image_path)

        if img is None:
            print(f"[ERROR] Failed to load: {image_path}")
            return True  # Treat unreadable image as corrupted

        # Convert to grayscale
        # gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Crop bottom 20% of the image
        if use_bottom:
            height = img.shape[0]
            top_crop = int(height * 0.8)
            img = img[top_crop:, :, :]  # (rows, cols, channels)

        score = obj.score(img)
        # cv2.imshow("title", img)
        # cv2.waitKey(0)
        # if score > threshold:
        #     print(f"[INFO] BRISQUE score for {image_path}: {score:.2f}")

        return score > threshold
    except Exception as e:
        # print(f"[ERROR] Exception processing {im`age_path}: {e}")
        traceback.print_exc()
        return True  # Treat error during processing as corruption


from PIL import Image
import numpy as np
from scipy.stats import entropy

# image feature based
def is_image_suspicious(image_path, color_threshold=0.15, entropy_threshold=4.0, use_bottom=False):
    img = Image.open(image_path).convert('RGB')

    # Crop the bottom half of the image
    if use_bottom:
        width, height = img.size
        top_crop = int(height * 0.8)
        img = img.crop((0, top_crop, width, height))

    arr = np.array(img)

    # Check for dominant color
    flat = arr.reshape(-1, 3)
    unique, counts = np.unique(flat, axis=0, return_counts=True)
    dominant_ratio = counts.max() / counts.sum()
    
    # Entropy check (lower entropy means less detail)
    # entropy is not really useful, as it is the same with dominant ratio
    # gray = np.mean(arr, axis=2).astype(np.uint8)
    # hist, _ = np.histogram(gray, bins=256, range=(0, 256), density=True)
    # img_entropy = entropy(hist + 1e-8)  
    
    # print("Dominant:", dominant_ratio * 100, "Entropy:", img_entropy)
    # if dominant_ratio > color_threshold:
    #     print("Dominant Ratio:", dominant_ratio)
    return dominant_ratio > color_threshold # or img_entropy < entropy_threshold

def handle_image_corruption(image_path):
    """Detect and delete image corruption."""
    file_size_mb = os.path.getsize(image_path) / (1024 * 1024)    # to MB

    if file_size_mb < 0.2:
        print("Deleted:", image_path)
        # os.remove(image_path)
    elif file_size_mb < 1:
        if is_image_corrupted_with_brisque(image_path, use_bottom=False):
            print("Deleted:", image_path)
            # os.remove(image_path)
            return
        
        if is_image_suspicious(image_path, use_bottom=True):
            print("Deleted:", image_path)
            # os.remove(image_path)
    else:
        if is_image_suspicious(image_path, use_bottom=True):
            print("Deleted:", image_path)
            # os.remove(image_path)
            return
        
        if is_image_corrupted_with_brisque(image_path, use_bottom=False):
            print("Deleted:", image_path)
            # os.remove(image_path)



if __name__ == "__main__":

    # Example usage with a folder of images
    # folder_path = "./image/corrupted_image/corrupted"
    folder_path = "./image/20250310/090000"
    tasks = [
        os.path.join(folder_path, filename)
        for filename in os.listdir(folder_path)
        if filename.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    with multiprocessing.Pool(processes=16) as pool:
        pool.map(handle_image_corruption, tasks)
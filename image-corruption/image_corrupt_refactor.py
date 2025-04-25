import os
import cv2
import traceback
import multiprocessing
import glob
from brisque import BRISQUE
from PIL import Image
import numpy as np

obj = BRISQUE(url=False)

def is_image_corrupted_with_brisque(image_path, threshold=50, use_bottom=False):
    """
    Returns True if the image is likely corrupted or low-quality based on BRISQUE score.
    
    Parameters:
        image_path (str): Path to the image file.
        threshold (float): BRISQUE score threshold. Higher means lower quality.
        use_bottom (bool): If True, analyze only the bottom 20% of the image.
    
    Returns:
        bool: True if image is considered corrupted/low-quality.
    """
    try:
        img = cv2.imread(image_path)

        if img is None:
            print(f"[ERROR] Failed to load: {image_path}")
            return True  # Treat unreadable image as corrupted

        # Crop bottom 20% of the image
        if use_bottom:
            height = img.shape[0]
            top_crop = int(height * 0.8)
            img = img[top_crop:, :, :]  # (rows, cols, channels)

        score = obj.score(img)

        return score > threshold
    except Exception as e:
        traceback.print_exc()
        return True  # Treat error during processing as corruption


def is_image_suspicious(image_path, color_threshold=0.15, use_bottom=False):
    """
    Returns True if the image appears suspicious (e.g., solid color) based on color dominance.

    Parameters:
        image_path (str): Path to the image file.
        color_threshold (float): Threshold for detecting dominant color.
        use_bottom (bool): If True, analyze only the bottom 20% of the image.

    Returns:
        bool: True if image appears suspicious.
    """
    img = Image.open(image_path).convert('RGB')

    # Crop the bottom 20% of the image
    if use_bottom:
        width, height = img.size
        top_crop = int(height * 0.8)
        img = img.crop((0, top_crop, width, height))

    arr = np.array(img)

    # Check for dominant color
    flat = arr.reshape(-1, 3)
    unique, counts = np.unique(flat, axis=0, return_counts=True)
    dominant_ratio = counts.max() / counts.sum()
    
    return dominant_ratio > color_threshold


def handle_image_corruption(image_path):
    """
    Determines whether an image is corrupted or suspicious based on file size,
    BRISQUE quality, and visual feature analysis. Optionally deletes the image.

    Parameters:
        image_path (str): Path to the image file.
    """
    file_size_mb = os.path.getsize(image_path) / (1024 * 1024)  # Convert to MB

    # Always delete very small files
    if file_size_mb < 0.2:
        print("Deleted:", image_path)
        # os.remove(image_path)     # uncomment at your own risk !!!
        return

    # Check visual suspicious features (bottom 20%) for all images >= 0.2 MB
    if is_image_suspicious(image_path, use_bottom=True):
        print("Deleted:", image_path)
        # os.remove(image_path)     # uncomment at your own risk !!!
        return

    # Check BRISQUE quality score
    if is_image_corrupted_with_brisque(image_path, use_bottom=False):
        print("Deleted:", image_path)
        # os.remove(image_path)     # uncomment at your own risk !!!


if __name__ == "__main__":
    """
    Main function to process a folder of images for corruption/suspicious content.
    Uses multiprocessing to speed up processing.
    """
    folder_path = "./image/20250310/090000" # change this line for your input folder

    tasks = glob.glob(os.path.join(folder_path, '**', '*.[jJpP][pPnN][gG]'), recursive=True)

    with multiprocessing.Pool(processes=16) as pool:
        pool.map(handle_image_corruption, tasks)

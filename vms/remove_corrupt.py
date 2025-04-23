import os
import glob
from PIL import Image
from tqdm import tqdm 
import cv2

# Set the range for grey values
lower_bound = 110
upper_bound = 210

def check_and_remove_corrupted_image(file_path):
    grey= nonblack=0
    for filename in tqdm(glob.glob(file_path)):
        print(">>" ,filename)
        img = Image.open(filename)
        h = img.height
        w = img.width
        total = w*h  
        lower_limit= 90
        higher_limit=100
        # print(img.getdata)
        for pixel in img.getdata():
            # if pixel == (110,110,110) or pixel == (210,210,210):
            if lower_bound <= pixel[0] <= upper_bound and lower_bound <= pixel[1] <= upper_bound and lower_bound <= pixel[2] <= upper_bound:
                grey +=1
            else:
                nonblack +=1
            # print(f"grey ={grey} , others ={nonblack}")
        
        percent = round((grey*100.0/total),1)
        print(f"{filename} is {percent}%")
        if lower_limit <= percent <= higher_limit:
            print("-----------")
            print(f"Remove {filename}")
            os.remove(filename)
            break


def scan_and_clean_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root,file)
            check_and_remove_corrupted_image(file_path)

if __name__ == "__main__":
    directory = "/home/itmax/hik_api_python/snapshot/20250307/100000"
    scan_and_clean_directory(directory)
    print(f"Directory scan and clean up files is completed")
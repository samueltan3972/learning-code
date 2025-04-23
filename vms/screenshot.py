import cv2
import os
import time

def capture_screenshot(rtsp_url, output_folder, interval=5):
    """
    Captures screenshots from an RTSP stream and saves them into a folder.
    
    :param rtsp_url: RTSP stream link
    :param output_folder: Folder to save the images
    :param interval: Time interval (in seconds) between screenshots
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    cap = cv2.VideoCapture(rtsp_url)
    if not cap.isOpened():
        print("Error: Could not open RTSP stream")
        return
    
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame")
            break
        
        filename = os.path.join(output_folder, f"screenshot_{frame_count}.jpg")
        cv2.imwrite(filename, frame)
        print(f"Saved: {filename}")
        
        frame_count += 1
        time.sleep(interval)
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    rtsp_link = ""  # Replace with your RTSP link
    output_dir = "screenshots"
    capture_screenshot(rtsp_link, output_dir, interval=5)

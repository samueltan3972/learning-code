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
            # break
        
        filename = os.path.join(output_folder, f"screenshot_{frame_count}.jpg")
        cv2.imwrite(filename, frame)
        print(f"Saved: {filename}")
        
        frame_count += 1
        time.sleep(interval)
    
    cap.release()
    cv2.destroyAllWindows()


def record_video_rtsp(rtsp_url, filename='output.mp4', duration=10, fps=20.0, resolution=(640, 480)):
    """
    Records video from an RTSP stream and saves it to a file.

    Parameters:
    - rtsp_url: str, the RTSP stream URL
    - filename: str, name of the output file
    - duration: int, duration of the recording in seconds
    - fps: float, frames per second
    - resolution: tuple, resolution of the video (width, height)
    """
    cap = cv2.VideoCapture(rtsp_url)

    if not cap.isOpened():
        print("Error: Could not open RTSP stream.")
        return

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use 'XVID' for .avi or 'mp4v' for .mp4
    out = cv2.VideoWriter(filename, fourcc, fps, resolution)

    print("Recording started from RTSP stream. Press 'q' to stop early.")
    frame_count = 0
    max_frames = int(fps * duration)

    while frame_count < max_frames:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame from RTSP stream.")
            break

        frame_resized = cv2.resize(frame, resolution)  # Ensure consistent output size
        out.write(frame_resized)
        # cv2.imshow('Recording RTSP Stream...', frame_resized)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Recording stopped by user.")
            break

        frame_count += 1

    cap.release()
    out.release()
    # cv2.destroyAllWindows()
    print(f"Recording saved to {filename}")



if __name__ == "__main__":
    rtsp_link = "rtsp://"  # Replace with your RTSP link
    output_dir = "screenshots"
    # capture_screenshot(rtsp_link, output_dir, interval=5)
    record_video_rtsp(rtsp_link)

    # Open the file in read mode
    # with open('rtsp.txt', 'r') as file:
    #     # Read each line in the file
    #     for line in file:
    #         # Print each line
    #         print(line.strip())

    #         capture_screenshot(line.strip(), output_dir, interval=5)

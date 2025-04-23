import cv2
import os
import traceback
import multiprocessing
import pandas as pd
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# GLOBAL df (will be set in initializer)
df = None

def init_worker(df_arg):
    global df
    df = df_arg

def log_error_to_file(message, log_file="error_log.txt"):
    """Append an error or warning message to the log file with a timestamp."""
    with open(log_file, "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {message}\n")

def capture_screenshot(rtsp_url, output_folder, filename, interval=5, retries=3, retry_delay=2):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    filepath = os.path.join(output_folder, f"{filename}.jpg")

    for attempt in range(retries):
        try:
            cap = cv2.VideoCapture(rtsp_url)

            if not cap.isOpened():
                raise Exception("RTSP stream could not be opened.")

            # Optional buffer wait
            # time.sleep(interval)

            ret, frame = cap.read()
            if not ret or frame is None:
                raise Exception("Failed to grab frame.")

            success = cv2.imwrite(filepath, frame)
            if not success:
                raise Exception("Failed to write image file.")

            print(f"[OK] Snapshot saved: {filepath}")
            return

        except Exception as e:
            msg = f"[WARN] Attempt {attempt+1}/{retries} failed for {filename}: {e}"
            print(msg)
            log_error_to_file(msg)
            # time.sleep(retry_delay)

        finally:
            if 'cap' in locals():
                cap.release()
            cv2.destroyAllWindows()

    error_msg = f"[ERROR] All retry attempts failed for {filename}"
    print(error_msg)
    log_error_to_file(error_msg)

def retrieve_rtsp(camera_code, timestamp: int):
    return "rtsp://"

def get_snapshot(timestamp):
    global df
    timestamp_ns = timestamp * 1000
    print(f"[{multiprocessing.current_process().name}] Processing timestamp: {timestamp}")

    for _, row in df.iterrows():
        camera_code = row['cameraIndexCode']
        camera_name = row['name']
        formatted_camera_name = camera_name.strip()

        pd_timestamp = pd.to_datetime(timestamp, unit='s').tz_localize('UTC').tz_convert('Asia/Kuala_Lumpur')
        date_string = pd_timestamp.strftime('%Y%m%d')
        hour_string = pd_timestamp.strftime('%H%M%S')
        folder_name = f"snapshot/{date_string}/{hour_string}"
        file_name = f"{date_string}_{hour_string}_{formatted_camera_name.replace(' ', '-')}"

        rtsp_url = retrieve_rtsp(camera_code, timestamp_ns)
        capture_screenshot(rtsp_url, folder_name, file_name)

if __name__ == "__main__":
    try:
        local_df = pd.read_csv("input.csv")
        start_timestamp = 1741312800
        end_timestamp = 1741316400
        sample = 1
        gap = int(3600 / sample)
        timestamps = list(range(start_timestamp, end_timestamp, gap))

        with multiprocessing.Pool(processes=10, initializer=init_worker, initargs=(local_df,)) as pool:
            pool.map(get_snapshot, timestamps)

    except Exception:
        print(f"Error: {traceback.print_exc()}")

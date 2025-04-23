import os

from dotenv import load_dotenv
from src.hik_api import HIK_API
from medoo import Medoo
from datetime import timezone

import cv2
import psycopg2
import traceback

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

me = Medoo(
    dbtype="pgsql",
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    database=POSTGRES_DB,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
)


def retrieve_images(id, camera_code, timestamp: int, table_name: str) -> None:
    """Retrieve images from the CCTV feed."""
    api = HIK_API()

    playback_url = api.get_playback_url(
        camera_code_index=camera_code, timestamp=timestamp
    )
    cap = cv2.VideoCapture(playback_url, cv2.CAP_FFMPEG)
    cap.set(cv2.CAP_PROP_CONVERT_RGB, 1)

    if not cap.isOpened():
        print("Error: Cannot open RTSP stream")

    _, frame = cap.read()
    _, jpg_img = cv2.imencode(".jpg", frame)
    image_bytes = jpg_img.tobytes()

    if table_name == "features_output.get_vehicles":
        table_name = "features_output.vehicle_tracking"

    # Save screenshot to database
    me.update(
        table_name, data={"image": psycopg2.Binary(image_bytes)}, where={"id": id}
    )

    cap.release()


if __name__ == "__main__":
    """
    This script is to get image for events, face and vehicle tracking where it is miss during get notification
    """
    # events
    data = me.select(
        "features_output.get_events",
        "id, cctv_name, start_time",
        where={"image": "", 'ORDER': {'start_time': 'desc'}, "LIMIT": (1000)},
    ).all()

    for record in data:
        # timestamp = record.start_time.replace(tzinfo=timezone.utc).timestamp() - (
        #     3600 * 8
        # )  # for container
        timestamp = record.start_time.replace(tzinfo=timezone.utc).timestamp()  # to run in local
        timestamp *= 1000  # ms

        try:
            retrieve_images(
                record.id, record.cctv_name, timestamp, "features_output.events"
            )
        except Exception:
            traceback.format_exc()
            pass

    # vehicle tracking
    data = me.select(
        "features_output.get_vehicles",
        "id, cctv_name, timestamp",
        where={"image[is]": None, "LIMIT": (1000)},
    ).all()

    for record in data:
        # timestamp = record.timestamp.replace(tzinfo=timezone.utc).timestamp() - (
        #     3600 * 8
        # )  # for container
        timestamp = record.timestamp.replace(tzinfo=timezone.utc).timestamp()  # to run in local
        timestamp *= 1000  # ms

        try:
            retrieve_images(
                record.id,
                record.cctv_name,
                timestamp,
                "features_output.vehicle_tracking",
            )
        except Exception:
            traceback.format_exc()
            pass

    # face embeddings
    data = me.select(
        "features_output.get_faces",
        "id, cctv_name, timestamp",
        where={"image[is]": None, "LIMIT": (1000)},
    ).all()

    for record in data:
        # timestamp = record.timestamp.replace(tzinfo=timezone.utc).timestamp() - (
        #     3600 * 8
        # )  # for container
        timestamp = record.timestamp.replace(tzinfo=timezone.utc).timestamp()  # to run in local
        timestamp *= 1000  # ms

        try:
            retrieve_images(
                record.id, record.cctv_name, timestamp, "features_output.face_embedding"
            )
        except Exception:
            traceback.format_exc()
            pass

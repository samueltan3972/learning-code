from dotenv import load_dotenv
from medoo import Medoo
from datetime import timezone

import asyncio
import asyncpg
import psycopg2
import multiprocessing
import traceback

import os
import cv2
import json
from zoneinfo import ZoneInfo
from multiprocessing.pool import ThreadPool
import queue
import threading
import time

class ImageRetriever(multiprocessing.Process):
    def __init__(self, db_config, channel, table_name, timestamp_offset: int = 0, pool_size: int = 6) -> None:
        """
        Image Retriever
        """
        super().__init__()

        self.pool_size = pool_size
        self.__close_switch = multiprocessing.Event()
        self.channel = channel
        self.timestamp_offset = timestamp_offset
        self.table_name = table_name

        self.db_config = db_config
        self.me = Medoo(
            dbtype="pgsql",
            **db_config
        )
        self.input_queue = multiprocessing.Queue() # queue for item that need to retrieve image


    def retrieve_images(self, id, camera_code, timestamp: int) -> None:
        """Retrieve images from the CCTV feed."""

        playback_url = "rtsp://"
        cap = cv2.VideoCapture(playback_url, cv2.CAP_FFMPEG)
        print(playback_url)
        cap.set(cv2.CAP_PROP_CONVERT_RGB, 1)

        if not cap.isOpened():
            print("Error: Cannot open RTSP stream")

        _, frame = cap.read()
        _, jpg_img = cv2.imencode(".jpg", frame)
        image_bytes = jpg_img.tobytes()

        # Save screenshot to database
        self.me.update(
            self.table_name, data={"image": psycopg2.Binary(image_bytes)}, where={"id": id}
        )

        cap.release()
        
    def worker_function(self, data:dict):
        try:
            _id = data.get("id")
            cctv_name = data.get("cctv_name")

            # Getting time from database
            if self.channel == "new_events":
                start_time = self.me.get(self.table_name, ["start_time"], where={"id": _id})
            else:
                start_time = self.me.get(self.table_name, ["timestamp"], where={"id": _id})

            # timestamp = start_time.replace(tzinfo=timezone.utc).timestamp()   # uncomment this if running in local
            timestamp = start_time.replace(tzinfo=timezone.utc).timestamp() + (
                3600 * 8
            )  # for container (as it is in UTC)
            timestamp += self.timestamp_offset
            timestamp *= 1000

            # Retrieve the image
            self.retrieve_images(_id, cctv_name, timestamp)

        except Exception:
            traceback.print_exc()


    # Handler for notifications
    def notification_handler(self, connection, pid, channel, payload):
        # print(f"Received notification on {channel}: {payload}")
        self.input_queue.put(json.loads(payload))

        
    async def listen_notifications(self):
        """Listen for PostgreSQL notifications on a given channel."""

        # Connect to PostgreSQL database
        conn = await asyncpg.connect(
            **self.db_config
        )

        # Listen to the channel
        await conn.add_listener(self.channel, self.notification_handler)

        print(f"Listening for notifications on '{self.channel}'...")

        # Keep the program running and listening for notifications
        try:
            while True:
                await asyncio.sleep(10)  # Sleep to keep the loop running
        finally:
            await conn.close()

    
    def _start_async_listener(self):
        # This runs the async method in a separate event loop in its own thread
        asyncio.run(self.listen_notifications())


    def run(self) -> None:
        print("Postprocessing controller started and waiting for tasks...")

        try:            
            threading.Thread(target=self._start_async_listener, daemon=True).start()

            # Process after getting notification
            # with multiprocessing.Pool(self.pool_size) as pool: # for process pool, worker function need to be static
            with ThreadPool(self.pool_size) as pool:
                while not self.__close_switch.is_set():
                    if self.input_queue.qsize() > 0:
                        data = self.input_queue.get()
                        pool.apply_async(
                            self.worker_function, args=(data,) #, callback=self.task_done
                        )

        except Exception:
            print("\033[91m" + "Controller down cause error")
            print(f"Error : {traceback.print_exc()}")

        self.close()
        print("Postprocess Controller down")
        return

    def close(self) -> None:
        if not self.__close_switch.is_set():
            self.__close_switch.set()

if __name__ == "__main__":
    load_dotenv()

    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")

    db_config = {
        "user": POSTGRES_USER,
        "password": POSTGRES_PASSWORD,
        "database": POSTGRES_DB,
        "host": POSTGRES_HOST,
        "port": POSTGRES_PORT,
    }

    image_retriever = ImageRetriever(db_config=db_config, channel="and_i_i_i_will_always_love_you", table_name="love_you_ohhhhh")
    image_retriever.start()
    image_retriever.join()
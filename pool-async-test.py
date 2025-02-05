import asyncio
import asyncpg
from multiprocessing import Process, Queue, Pool
from threading import Thread
import time


class Controller(Process):
    def __init__(self, input_queue, pool_size=4, db_config=None):
        """
        Controller initializes the input queue, process pool, and database connection pool.
        :param input_queue: multiprocessing.Queue used for receiving data from the main process.
        :param pool_size: Number of worker processes in the pool.
        :param db_config: Dictionary containing PostgreSQL connection parameters.
        """
        super().__init__()
        self.input_queue = input_queue
        self.pool_size = pool_size
        self.db_config = db_config or {
            "user": "your_user",
            "password": "your_password",
            "database": "your_database",
            "host": "localhost",
        }
        self.results_queue = Queue()
        self.db_loop = asyncio.new_event_loop()

    @staticmethod
    def worker_function(data):
        """
        Function executed by worker processes in the pool.
        """
        print(f"Worker is processing data: {data}", flush=True)
        time.sleep(1)  # Simulate work
        return f"Processed: {data}"

    async def create_db_pool(self):
        """
        Create a database connection pool using asyncpg.
        """
        self.db_pool = await asyncpg.create_pool(
            min_size=1,
            max_size=10,
            **self.db_config
        )
        print("Database connection pool created.")

    async def insert_into_db(self, result):
        """
        Insert result into the database.
        """
        try:
            async with self.db_pool.acquire() as conn:
                # await conn.execute("INSERT INTO task_results (result) VALUES ($1)", result)
                print(f"Inserted into database: {result}")
        except Exception as e:
            print(f"Error inserting into database: {e}")

    async def process_results(self):
        """
        Continuously process results from the results_queue and insert them into the database.
        """
        print("Starting process_results coroutine...")
        while True:
            result = self.results_queue.get()  # Block until a result is available
            print("Result", result)
            await self.insert_into_db(result)

    def task_done(self, result):
        """
        Callback function to handle the result of a task.
        """
        print(f"Task completed with result: {result}", flush=True)
        self.results_queue.put(result)  # Add the result to the results queue

    def start_db_task(self):
        """
        Run the asyncio event loop for the database processing in a separate thread.
        """
        self.db_loop.run_until_complete(self.process_results())
        self.db_loop.run_until_complete(self.db_pool.close())
        print("Database connection pool closed.")

    def run(self):
        """
        Main loop to process tasks and manage the database insertion thread.
        """
        asyncio.set_event_loop(self.db_loop)
        self.db_loop.run_until_complete(self.create_db_pool())
        
        # Start the database processing thread
        db_thread = Thread(target=self.start_db_task)
        db_thread.start()

        print("Controller started and waiting for tasks...", flush=True)
        with Pool(self.pool_size) as pool:
            while True:
                try:
                    # Get data from the input queue
                    data = self.input_queue.get(timeout=5)  # Timeout to prevent infinite wait
                except Exception as e:
                    print(f"Queue timeout or error: {e}", flush=True)
                    break

                # Check for the sentinel value to terminate
                if data == "STOP":
                    print("Stopping Controller...", flush=True)
                    # self.results_queue.put("STOP")  # Notify the results processor to stop
                    break

                print(f"Received data: {data}", flush=True)

                # Add task to the process pool
                pool.apply_async(self.worker_function, args=(data,), callback=self.task_done)

            pool.close()
            pool.join()

        # Wait for the database thread to finish
        db_thread.join()
        print("Controller process finished.")


if __name__ == "__main__":
    # Create the shared queue
    input_queue = Queue()

    # Database configuration (adjust with your credentials)
    db_config = {
        "user": "app",
        "password": "PrtXH3bw6Ltx",
        "database": "SMART_CITY",
        "host": "localhost",
    }

    # Start the Controller process
    controller = Controller(input_queue, pool_size=4, db_config=db_config)
    controller.start()

    # Simulate the main process adding data to the queue
    for i in range(10):
        print(f"Main process putting data: {i}", flush=True)
        input_queue.put(i)

    # Add a sentinel value to stop the controller
    input_queue.put("STOP")

    # Wait for the controller to finish
    controller.join()
    print("Main process finished.", flush=True)

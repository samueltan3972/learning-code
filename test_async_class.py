from multiprocessing import Process, Queue, Pool, Semaphore
import time, random


class Controller(Process):
    def __init__(self, input_queue, pool_size=4):
        """
        Controller initializes the input queue and process pool.
        :param input_queue: multiprocessing.Queue used for receiving data from the main process.
        :param pool_size: Number of worker processes in the pool.
        """
        super().__init__()
        self.input_queue = input_queue
        self.pool_size = pool_size
        self.semaphore = Semaphore(pool_size)

    @staticmethod
    def worker_function(data):
        """
        Function executed by worker processes in the pool.
        :param data: The data received from the queue.
        :return: The processed result.
        """
        print(f"Worker is processing data: {data}", flush=True)
        time.sleep(0.25)  # Simulate work
        return f"Processed: {data}"

    # @staticmethod
    def task_done(self, result):
        """
        Callback function to handle the result of a task.
        """
        print(f"Task completed with result: {result}", flush=True)
        self.semaphore.release()

    def run(self):
        """
        Main loop to continuously process data from the queue.
        """
        print("Controller started and waiting for tasks...", flush=True)
        with Pool(self.pool_size) as pool:  # Create the pool inside the run method
            while True:
                try:
                    self.semaphore.acquire()
                    # Get data from the input queue
                    data = self.input_queue.get(timeout=5)  # Timeout to prevent infinite wait
                except Exception as e:
                    print(f"Queue timeout or error: {e}", flush=True)
                    break

                # Check for the sentinel value to terminate
                if data == "STOP":
                    print("Stopping Controller...", flush=True)
                    break

                # print(f"Received data: {data}", flush=True)
                
                # Add task to the process pool
                pool.apply_async(self.worker_function, args=(data,), callback=self.task_done)

            pool.close()
            pool.join()


if __name__ == "__main__":
    # Create the shared queue
    input_queue = Queue()

    # Start the Controller process
    controller = Controller(input_queue, pool_size=4)
    controller.start()

    # Simulate the main process adding data to the queue
    while True:
        i = random.randint(1, 100)
        # print(f"Main process putting data: {i}", flush=True)
        input_queue.put(i)

    # Add a sentinel value to stop the controller
    # input_queue.put("STOP")

    # Wait for the controller to finish
    controller.join()
    print("Main process finished.", flush=True)

from multiprocessing import Pool, BoundedSemaphore, Semaphore
import time
import random

pool_size = 2
semaphore = Semaphore(pool_size)

def worker_function(data):
    print(f"Processing: {data}")
    time.sleep(1)  # Simulate some work
    return f"Processed: {data}"

def task_done(result):
    semaphore.release()
    print(f"Task completed: {result}")

if __name__ == "__main__":
    data_list = [1, 2, 3, 4, 5]
    pool = Pool(pool_size)

    # Create a pool of 4 workers
    # with Pool(2) as pool:
    #     # Submit tasks
    #     while True:
    #         semaphore.acquire()
    #         data = random.randint(1, 100)
    #         pool.apply_async(worker_function, args=(data,), callback=task_done)

        # Close and join the pool
        # pool.close()
        # pool.join()
    while True:
        semaphore.acquire()
        data = random.randint(1, 100)
        pool.apply_async(worker_function, args=(data,), callback=task_done)

    pool.close()
    pool.join()

    print("All tasks completed.")

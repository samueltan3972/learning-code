from cuda import cuda

def is_cuda_available():
    try:
        # Initialize CUDA driver
        cuda.cuInit(0)
        # Get the number of CUDA devices
        device_count = cuda.cuDeviceGetCount()
        device_name = cuda.cuDeviceGetName(100, 0)
        print('Device Count:', device_count[1])
        print('Device Name:', device_name[1])
        return device_count[1] > 0
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        print(f"CUDA error: {e}")
        return False

if __name__ == "__main__":
    if is_cuda_available():
        print("CUDA is available!")
    else:
        print("CUDA is not available.")

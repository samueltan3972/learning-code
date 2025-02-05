import time

for i in range(5):
    # print(i, end=" ", flush=True)  # Print numbers as soon as they are generated
    # print(i, end=" ", flush=False)  # Print everything together at the end
    print(i)
    time.sleep(0.5)

print("end")
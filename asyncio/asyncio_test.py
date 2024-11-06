import cv2
import numpy as np
import timeit
import asyncio


# decode
# a = cv2.imread("sample_video/av.jpg")
async def pwait(s, text):
    await asyncio.sleep(s)
    print(text)

async def main():
    await pwait(5, "five")
    await pwait(1, "one")

if __name__ == "__main__":
    asyncio.run(main())
    # print("test")

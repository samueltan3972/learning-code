import cv2


def view_bounding_box(image: str):
    frame = cv2.imread(image)

    box = (135, 309, 175, 325)  # raw=image
    color = (0, 0, 255)

    frame = cv2.rectangle(
        frame, (box[0], box[1]), (box[2], box[3]), color=color, thickness=2
    )  # xyxy

    frame = cv2.rectangle(frame, (box[0], box[1], box[2], box[3]), color=color, thickness=2) # xywh
    frame = frame[box[1]:box[3], box[0]:box[2], :]

    cv2.imshow("title", frame)
    cv2.waitKey(0)


if __name__ == "__main__":
    image = "/home/ubuntu/work/license-plate-recognition/data/1-raw/2024-04-24/raining_732/30360e5093494de48f8da8b3da695ba9803d0238e0aa0e79930fa953.jpg"

    view_bounding_box(image)

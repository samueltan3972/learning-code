import cv2

from websockets.sync.client import connect

cap = cv2.VideoCapture("rtsp://admin:senatraffic1234*@192.168.1.65:554")

while(cap.isOpened()):
    ret, frame = cap.read()

    with connect("ws://localhost:8765") as websocket:
        websocket.send(frame.tobytes())

    print('sending')
    # cv2.imshow('show', frame)

    if 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
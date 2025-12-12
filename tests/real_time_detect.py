#import cv2
from picamera2 import Picamera2
import time
import sys

# cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
cascade_path = "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(cascade_path)
if face_cascade.empty():
    print(f"Failed to load cascade at: {cascade_path}")
    sys.exit(1)

picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (640, 480), "format": "RGB888"})
picam2.configure(config)
picam2.start()
time.sleep(0.2) 

try:
    while True:
        # RGB frame from the Pcam
        frame = picam2.capture_array()
        if frame is None:
            print("No frame captured at this point")
            break

        # conv rgb to gray for detect
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        # recte on frame
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # conv tpo bgr for imshow
        bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        cv2.imshow("Cam Feed", bgr)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
finally:
    try:
        picam2.stop()
    except Exception:
        pass
    try:
        picam2.close()
    except Exception:
        pass
    cv2.destroyAllWindows()

import cv2
import time
import face_recognition
import pickle
import numpy as np
from picamera2 import Picamera2
from pymodbus.client import ModbusTcpClient
import json
import tempfile
from pathlib import Path
from datetime import datetime
import os

PLC_IP = "192.168.0.1"
Modbus_Port = 502
# ghex y5 = 8196
Coil_Addr = 8199
Coil_2 = 8200
client = ModbusTcpClient(host=PLC_IP, port=Modbus_Port)
try:
    client.connect()
    print("Connectted to PLC successfully")
except Exception as e:
    print("Failed to connect", e)

# Path to encodings file
# ENC_PATH = "../src/face_encodings.pkl"
ENC_PATH = "../src/face_encodings_2.pkl"

# Loadin known encodings from database
def load_encodings(path):
    with open(path, "rb") as fp:
        db = pickle.load(fp)
    enc = db["encodings"]
    names = db["names"]
    if not enc:
        raise ValueError("No encodings in DB.")
    return np.array(enc), names

known_encodings, known_names = load_encodings(ENC_PATH)
print(f"[OK] Loaded {len(known_encodings)} encodings for {len(set(known_names))} people")


# # OpenCV setup for camera
# cap = cv2.VideoCapture(0)  # Change 0 to the correct camera ID if using a different camera
# if not cap.isOpened():
#     print("Error: Cannot access the camera")
#     exit()

# Picam setip for camera
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (640, 480)})
picam2.configure(config)
picam2.start()

# Frame processing loop
print("[INFO] Press 'q' to quit.")
# path to status file (backend)
STATUS_PATH = Path(__file__).parent.parent / "backend" / "app" / "recognition_status.json"

def write_recognition_status(name: str, status: str):
    payload = {
        "name": name,
        "status": status,
        "updated_at": datetime.utcnow().isoformat()
    }
    # atomic write: write to temp file in same dir then replace
    STATUS_PATH.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(dir=str(STATUS_PATH.parent))
    try:
        with os.fdopen(fd, 'w') as f:
            json.dump(payload, f)
        Path(tmp_path).replace(STATUS_PATH)
    except Exception:
        try:
            # best-effort fallback
            with open(STATUS_PATH, 'w') as f:
                json.dump(payload, f)
        except Exception:
            pass
while True:
    # OpenCV Cam
    # Capture frame-by-frame
    # ret, frame = cap.read()
    # if not ret:
    #     print("Error: Failed to capture image")
    #     break

    # Picam
    frame = picam2.capture_array()
    # rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # COnvertion from BGR cv to RGB face recognition format
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect faces in the frame
    face_locations = face_recognition.face_locations(rgb_frame)

    if len(face_locations) == 0:
        print("NOthing detected")
        client.write_coil(address=Coil_Addr, value=False)
        client.write_coil(address=Coil_2, value=False)
        # update frontend status: no face / idle
        try:
            write_recognition_status("Unknown", "idle")
        except Exception:
            pass
#        continue
    
    # Getting face encodings for the detected faces
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # Process each detected face
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Compute distances to all known encodings
        dists = face_recognition.face_distance(known_encodings, face_encoding)

        # Find the best match
        best_idx = np.argmin(dists)
        best_dist = dists[best_idx]
 
        print("Nothing to detcect")
        client.write_coil(address=Coil_Addr, value=False)       
        # incease tha best march is below the tolerance, lable face
        if best_dist <= 0.6:  
            label = known_names[best_idx]
            client.write_coil(address=Coil_Addr, value=True)
            print("True to COil")
        else:
            label = "Unknown"
            client.write_coil(address=Coil_Addr, value=False)
            client.write_coil(address=Coil_2, value=True)
            print("False to Coil")
#        else:
#            print("Nothing to detect")
#            client.write_coil(address=Coil_Addr, value=False)

        print("Detection: ", label)

        # write status for frontend
        try:
            if label == "Unknown":
                write_recognition_status(label, "unknown")
            else:
                write_recognition_status(label, "recognized")
        except Exception:
            pass

        # Draw rectangle and label detect on the frame
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 180, 0), cv2.FILLED)
        cv2.putText(frame, label, (left + 6, bottom - 6),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)

    # Display the result frame
    cv2.imshow("Real-Time Face Recognition", frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the cv windows
cap.release()
cv2.destroyAllWindows()

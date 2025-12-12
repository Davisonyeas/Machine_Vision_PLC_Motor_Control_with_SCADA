from picamera2 import Picamera2

picam = Picamera2()

picam.start_and_record_video("ter.mp4", duration=5)


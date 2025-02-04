import cv2
import numpy as np
import threading
import time

class FaceDetector:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.cap = cv2.VideoCapture(0)
        self.frame = None
        self.processed_frame = None
        self.running = False
        self.multiple_faces_detected = False
        self.warning_start_time = None
        self.warning_duration = 20  # Warning duration in seconds
        self.test_auto_submitted = False  # Flag for test submission state

    def start(self):
        self.running = True
        threading.Thread(target=self._capture_thread).start()
        threading.Thread(target=self._detection_thread).start()

    def stop(self):
        self.running = False
        self.cap.release()

    def _capture_thread(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                self.frame = frame

    def _detection_thread(self):
        while self.running:
            if self.frame is not None:
                frame = self.frame.copy()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
                
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                
                if len(faces) > 1:
                    if not self.multiple_faces_detected:
                        self.multiple_faces_detected = True
                        self.warning_start_time = time.time()
                    
                    elapsed_time = time.time() - self.warning_start_time
                    if elapsed_time <= self.warning_duration:
                        warning_text = f"Warning: Multiple faces detected! Test will be submitted in {int(self.warning_duration - elapsed_time)} seconds"
                        cv2.putText(frame, warning_text, (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.7, (0, 0, 0), 1)
                    else:
                        self.test_auto_submitted = True
                        self.stop()  # Stop the detection and capture
                        break
                else:
                    self.multiple_faces_detected = False
                    self.warning_start_time = None
                
                self.processed_frame = frame

    def get_frame(self):
        return self.processed_frame

    def get_black_frame_with_text(self):
    # Create a black frame
        black_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # Add the "Test auto-submitted" frame
        cv2.putText(black_frame, "Test auto-submitted", (50, 220), cv2.FONT_HERSHEY_COMPLEX, 1.0, (255, 255, 255), 2)
        cv2.putText(black_frame, "due to multiple face detection", (50, 260), cv2.FONT_HERSHEY_COMPLEX, 1.0, (255, 255, 255), 2)
    
        return black_frame

def main():
    detector = FaceDetector()
    detector.start()

    # Set the OpenCV window to full screen
    cv2.namedWindow('Face Detection during Test', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('Face Detection during Test', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    try:
        while detector.running:  # Check if the detector is still running
            frame = detector.get_frame()
            if frame is not None:
                cv2.imshow('Face Detection during Test', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        if detector.test_auto_submitted:
            
            black_frame = detector.get_black_frame_with_text()
            for _ in range(200): 
                cv2.imshow('Test Status', black_frame)
                if cv2.waitKey(45) & 0xFF == ord('q'):
                    break
    finally:
        detector.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()


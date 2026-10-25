import cv2
import time
import xlwrite
from pathlib import Path
import winsound

# Initialize
attendance_dict = {}  # track already marked students

# Ensure Excel folder exists
excel_folder = Path('firebase/attendance_files')
excel_folder.mkdir(parents=True, exist_ok=True)

# Load face detector and recognizer
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)
cap = cv2.VideoCapture(0)
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('C:/Users/User/Desktop/trainer/trainer.yml')  # trained model path

font = cv2.FONT_HERSHEY_SIMPLEX
time.sleep(1)  # webcam warm-up

CONF_THRESHOLD = 80  # adjust based on your training

face_detected = False  # flag to know when a face is detected

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50,50))

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_gray = cv2.resize(roi_gray, (200,200))

        id_, conf = recognizer.predict(roi_gray)
        name = "Unknown"

        if conf < CONF_THRESHOLD:
            if id_ == 1: name = "Shoaib"
            elif id_ == 2: name = "Hossain"
            elif id_ == 3: name = "Rashed"
            elif id_ == 4: name = "Nayan Sir"

            if name not in attendance_dict:
                xlwrite.output('attendance', 'class1', id_, name, 'yes')
                attendance_dict[name] = True
                print(f"Attendance marked for {name}")

        # Draw rectangle and label
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255,0,0), 2)
        cv2.putText(frame, f"{name} {int(conf)}", (x, y-10), font, 0.55, (120,255,120), 1)

        face_detected = True  # face detected, set flag
        break  # break after detecting first face

    cv2.imshow("Face Recognition", frame)

    if face_detected:
        # Delay 3-4 seconds before closing so user can see
        cv2.waitKey(1000)  # 1000 ms = 1 second
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
import cv2
import os

def assure_path_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

face_id = input('enter your id: ')

# Start capturing video
vid_cam = cv2.VideoCapture(0)

if not vid_cam.isOpened():
    print("Camera not found")
    exit()

# Load Haarcascade correctly
face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

count = 0
dataset_path = "C:/Users/User/Desktop/dataset/"
assure_path_exists(dataset_path)

while True:
    ret, image_frame = vid_cam.read()
    if not ret:
        break

    gray = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)

    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        count += 1

        cv2.imwrite(
            dataset_path + "User." + str(face_id) + "." + str(count) + ".jpg",
            gray[y:y + h, x:x + w]
        )

        cv2.rectangle(image_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.imshow('frame', image_frame)

    if cv2.waitKey(100) & 0xFF == ord('q'):
        break
    elif count >= 50:
        print("Successfully Captured")
        break

vid_cam.release()
cv2.destroyAllWindows()

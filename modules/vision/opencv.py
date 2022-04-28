'''
Testing capabilities of opencv in OmniSynth.

sources:
1) Shantnu Tiwari's Real Python articles:
    https://realpython.com/face-detection-in-python-using-a-webcam/
    https://realpython.com/face-recognition-with-python/#opencv

2) https://github.com/shantnu/Webcam-Face-Detect
'''

import cv2

cascade = 'haarcascade_frontalface_default.xml'

face_cascade = cv2.CascadeClassifier(cascade)

vid_cap = cv2.VideoCapture(0)

while True:
    ret, frame = vid_cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),

        # https://stackoverflow.com/questions/36242860/attribute-error-while-using-opencv-for-face-recognition
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
vid_cap.release()
cv2.destroyAllWindows()
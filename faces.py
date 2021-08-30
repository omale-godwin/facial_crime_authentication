import numpy as np
import cv2
import os

file_name = '/home/omale/Music/facail_auth/facial_auth/students/cascade/data/haarcascade_frontalface_alt2.xml'

face_cascade = cv2.CascadeClassifier(file_name)

cap = cv2.VideoCapture(0)
address = 'http://10.238.75.42:8080/video'
cap.open(address)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
  
    frame = cv2.resize(frame, (0, 0), fx=0.3, fy=0.3)
  
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
    for (x, y, w, h) in faces:
        print(x,y,w,h)
        roi_gray = gray[y:y+h, x:x+w]
        img_term = 'my_image.png'
        cv2.imwrite(img_term, roi_gray)
        color = (255, 0, 0)
        stroke = 2
        end_cord_x = (x +w)
        end_cord_y = (y + h)

        cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
        

    # Display the resulting framez
    cv2.imshow('KADPOLY ELECTION ACCREDITATION FINAL PROJECT',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
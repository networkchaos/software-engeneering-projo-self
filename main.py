#webcam
import cv2 
import pickle
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime
 
 
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://bcs3106-ddc83-default-rtdb.firebaseio.com/",
    'storageBucket':"bcs3106-ddc83.appspot.com"
})
 



cap = cv2.VideoCapture(0)
#we are using graphics so we need to specify the frame dimensions.
cap.set(3, 640)
cap.set(4, 480)

#import the encoding file just loading the file 
print ("Loading Encoded File ...")

file = open("encodefile.p", 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
#print(studentIds)
print("Encode File Loaded")

counter = 0
id = 0


# ...

while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                img = cvzone.cornerRect(img, bbox, rt=0)
                id = studentIds[matchIndex]

                if counter == 0:
                    counter = 1

                # ...

    if counter != 0:
    # Downloading the data once
        if counter == 1:
        # Get the data
            studentsInfo = db.reference(f'Students/{id}').get()
            print(studentsInfo)
            
        if 'Last_attendance_time' in studentsInfo:
            datetimeObject = datetime.strptime(studentsInfo['Last_attendance_time'], "%Y-%m-%d %H:%M:%S")
            secondElapsed = (datetime.now() - datetimeObject).total_seconds()
            print(secondElapsed)

            if secondElapsed > 86400:
                ref = db.reference(f'Students/{id}')
                studentsInfo['total_attendance'] += 1
                ref.child('total_attendance').set(studentsInfo['total_attendance'])
                ref.child('Last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                print("Attendance marked successfully.")
            else:
                counter = 0
                print("Attendance already marked for today.")

            if 10 < counter < 20:
                print("Attendance marked sir")
            if counter <= 10:
                print(studentsInfo)

        counter += 1

        if counter >= 20:
            counter = 0
            studentsInfo = []

# ...

    else:
        counter = 0

    cv2.imshow("Webcam", img)
    cv2.waitKey(1)

# ...

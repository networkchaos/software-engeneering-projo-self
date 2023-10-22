import cv2
import face_recognition
import pickle # used for dumping
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
 
 
 
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://bcs3106-ddc83-default-rtdb.firebaseio.com/",
    'storageBucket':"bcs3106-ddc83.appspot.com"
})
 
 
 
 #we will start by importing the students images



folderPath = 'images'
PathList = os.listdir(folderPath)
print(PathList)
imgList = []

studentsIds = []


for path in PathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    #print(path)
   # print(os.path.splitext(path)[0])
    studentsIds.append(os.path.splitext(path)[0])

    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)



print(studentsIds)


def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        #ensure to move form bgr to rgb
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList
print("Encoding Starting ...")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, studentsIds]
print("Encoding Complete")

file = open("encodefile.p", 'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("file saved mate")
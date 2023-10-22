import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://bcs3106-ddc83-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')

data = {
    "9280" :
        {
            "name":"George Ruchathi Kinyanjui",
            "major":"Cyber Sec",
            "starting_year":2021,
            "total_attendance":5,
            "standing":"G",
            "year":3,
            "last_attendance_time":"2023-10-20 00:54:34"

            
        },
    "9281" :
        {
            "name":"Elon Musk ",
            "major":"Cyber Sec",
            "starting_year":2018,
            "total_attendance":5,
            "standing":"B",
            "year":4,
            "last_attendance_time":"2023-10-20 00:54:34"

            
        },
    "9282" :
        {
            "name":"Bill Gates ",
            "major":"Information Systems",
            "starting_year":2020,
            "total_attendance":5,
            "standing":"G",
            "year":3,
            "last_attendance_time":"2023-10-20 00:54:34"

            
        },

}

for key, value in data.items():
    ref.child(key).set(value)
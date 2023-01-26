import face_recognition
import cv2
from PIL import Image, ImageDraw, ImageFont
import sys
import pandas as pd
import datetime
import pygame
# Module 1 Reference Data Load Module
ef = pd.read_csv('./DataFiles/Employee.csv')
empno = ef["Employee No"].tolist()
firstname = ef["First Name"].tolist()
lastname = ef["Last Name"].tolist()
photolocation = ef["Photo Location"].tolist()
audiolocation = ef["Audio Location"].tolist()
n = len(empno)
emp = []
emp_encod = []
audio = []
for i in range(n):
    emp.append(face_recognition.load_image_file(photolocation[i]))
    emp_encod.append(face_recognition.face_encodings(emp[i])[0])



# Module 2 Face Image Capture
camera = cv2.VideoCapture(0)
for i in range(10):
    return_value, image = camera.read()
    cv2.imwrite('Employee'+str(i)+'.png', image)
del(camera)
uk =face_recognition.load_image_file('Employee5.png')

#Module 3 Face Recognition Module
def identify_employee(photo):
    try:
        uk_encode = face_recognition.face_encodings(photo)[0]
    except IndexError as e:
        print(e)
        sys.exit(1)
    found = face_recognition.compare_faces(
                emp_encod, uk_encode, tolerance = 0.5)    
    print(found)
    
    index = -1
    for i in range(n):
        if found[i]:
            index = i
    return(index)


emp_index = identify_employee(uk)    
print(emp_index)   

# Module 4 Attendance record in a data file attendance.txt
if (emp_index != -1):
    x = str(datetime.datetime.now())
    eno = str(empno[emp_index])
    f = firstname[emp_index]
    l = lastname[emp_index]
    ar = "\n"+eno+" "+f+" "+ l+ "  "+x
    f = open("./DataFiles/Attendance.txt", "a")
    f.write(ar)
    f.close()  
    print(ar)
    
# Module 5 Display Attendance Module
pil_uk = Image.fromarray(uk)
draw = ImageDraw.Draw(pil_uk)
fnt = ImageFont.truetype(
    "Pillow/Tests/fonts/Arial", 60)

if emp_index ==-1:
    name ="Face NOT Recognized"
else:
    name = firstname[emp_index]+" "+lastname[emp_index]
x = 100
y = uk.shape[0] - 100
draw.text((x, y), name, font=fnt, fill=(0,0,0))
pil_uk.show()

# Module 6 Announce Attendance Recorded Module
audioloc = audiolocation[emp_index]
pygame.mixer.init()
if emp_index ==-1:
    pygame.mixer.music.load(
        "./DataFiles/EmployeeAudio/failure.mp3")
    pygame.mixer.music.play()
else:
    pygame.mixer.music.load(audioloc)
    pygame.mixer.music.play()
    pygame.mixer.music.queue(
        "./DataFiles/EmployeeAudio/success.mp3")
    pygame.mixer.music.play()


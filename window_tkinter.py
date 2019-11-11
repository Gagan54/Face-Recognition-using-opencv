#import the necessary packages
from tkinter import *
import pandas as pd
import xlrd
import os
import sys
import cv2
import numpy as np
import sqlite3 as sql
import xlwt
from PIL import Image

#train the model
def train_data():
	def collect_training_data(path):
	    images=[os.path.join(path,f) for f in os.listdir(path)]    
	    faces=[]
	    Ids=[]
	    for imagePath in images:
	        print("Trainning image : ",imagePath)
	        gray=Image.open(imagePath).convert('L')
	        image=np.array(gray,'uint8')
	        Id=int(os.path.split(imagePath)[-1].split(".")[1])
	        faces.append(image)
	        Ids.append(Id)
	    return faces,Ids

	lbph = cv2.face_LBPHFaceRecognizer.create()
	faces,Id = collect_training_data("train_data")
	lbph.train(faces, np.array(Id))
	lbph.save("Trained_model.yml")
	status_txt.configure(text="Trained Model Successfully")


def collect_data():
	db = sql.connect('database.db')
	cur = db.cursor()

	name=(txt1.get())
	roll_no=(txt2.get())
	sql_query = '''INSERT INTO records(name,roll_no) VALUES('%s','%s')'''%(name,roll_no);

	try:
		cur.execute(sql_query)
		query = '''select * from records;'''
		cur.execute(query)
		n = []
		r = []
		for row in cur.fetchall():
			r.append(row[0])
			n.append(row[1]) 

		df = pd.DataFrame()
		df['Rollno'] = r
		df['Names'] = n
		df.to_excel('records\\Records.xls')
		print('Records inserted into an excel file')
		db.commit()

	except Exception as e:
		db.rollback()
	db.close()

	#df = pd.read_excel("records\\Records.xls")
	face_clf = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


	def face_extractor(img):
	    #function detect faces and return cropped faces   
	    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	    faces = face_clf.detectMultiScale(gray,1.3,5)

	    if faces is ():
	        return None	        
	    
	    #crop all faces found
	    for (x,y,w,h) in faces:
	        cropped_faces = img[y:y+h,x:x+w]        
	    return cropped_faces

	# Initialize webcam
	cap = cv2.VideoCapture(0)
	count=0
	flag=1
	while flag==1:
	    ret,frame = cap.read()
	    
	    if face_extractor(frame) is not None:
	        count +=1
	        face = cv2.resize(face_extractor(frame),(200,200))
	        face = cv2.cvtColor(face,cv2.COLOR_BGR2GRAY)
	            
	        # save file in specified directory with unique name
	        file_name_path = "train_data\\"+str(name)+"."+str(roll_no)+"."+str(count)+'.jpg'
	        cv2.imwrite(file_name_path,face)
	            
	        #put count on images and display images
	        cv2.putText(face,str(count),(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
	        cv2.imshow('face cropped',face)
	            
	    else:
	        print('face not found')
	            
	    if cv2.waitKey(1)==ord('q') or count==100:
	        break

	status_txt.configure(text='Training data collected Successfully.')
	cap.release()
	cv2.destroyAllWindows()


#function to clear the text 
def clear():
    txt1.delete(0, 'end')    
    txt2.delete(0, 'end')
    
#function to run main window
def run():
	window.destroy()
	import window_tkinter_main

#create a tkinter application
window=Tk()
window.title("Security System")
window.geometry('1000x650')
window.configure(background='cornsilk3')

canvas=Canvas(width=1500,height=900,bg='cornsilk3')

line0=canvas.create_line(0,100,1364,100,width=8,fill='gray')
line1=canvas.create_line(460,100,460,500,width=8,fill='gray')
line2=canvas.create_line(920,100,920,500,width=8,fill='gray')
line3=canvas.create_line(0,500,1364,500,width=8,fill='gray')

canvas.pack()

message=Label(window, text="Add New User",bg="RoyalBlue4",fg="white",width=57,height=2,font=('arial', 29, 'bold ')) 
message.place(x=0, y=0)

Lb1=Label(window,text="STEP 1 :",bg='RoyalBlue4',fg="white",width=10,height=2,font=('arial',20,'bold'))
Lb1.place(x=140, y=130)

Lb2=Label(window,text="STEP 2 :",bg='RoyalBlue4',fg="white",width=10,height=2,font=('arial',20,'bold'))
Lb2.place(x=600, y=130)

Lb3=Label(window,text="STEP 3 :",bg='RoyalBlue4',fg="white",width=10,height=2,font=('arial',20,'bold'))
Lb3.place(x=1050, y=130)

lbl1 =Label(window, text="Enter Name :",width=12  ,fg="black"  ,bg="cornsilk3" ,height=2 ,font=('arial', 18, ' bold ')) 
lbl1.place(x=40, y=250)

txt1 =Entry(window,width=20  ,bg="PaleGreen1"  ,fg="black",font=('arial', 15, ' bold ')  )
txt1.place(x=225, y=260)

lb2 =Label(window, text="Enter Roll No :",width=12 ,height=2  ,fg="black"  ,bg="cornsilk3" ,font=('arial', 18, ' bold ') ) 
lb2.place(x=40, y=325)

txt2 =Entry(window,width=20 ,bg="PaleGreen1" ,fg="black",font=('arial', 15, ' bold '))
txt2.place(x=225, y=340)

clear_btn =Button(window, text="Clear ->",width=12  ,height=1,command=clear,activebackground = "tan1",font=('arial', 15, ' bold '))#, command=TakeImages ,fg="tan1"  ,bg="PaleGreen1"  ,width=20  ,height=3, activebackground = "tan1" ,font=('arial', 15, ' bold '))
clear_btn.place(x=175, y=425)

takepic=Label(window, text="Take Pictures of the user",bg="cornsilk3",font=('arial', 18, ' bold '))#width=12  ,fg="black"  ,bg="cornsilk3"    ,height=2 ,font=('arial', 18, ' bold ')) 
takepic.place(x=560, y=250)

data=Button(window, text="Collect data ->",width=12 ,height=1,command=collect_data,activebackground = "tan1",fg="black",font=('arial', 15, ' bold '))#, command=TakeImages ,fg="tan1"  ,bg="PaleGreen1"  ,width=20  ,height=3, activebackground = "tan1" ,font=('arial', 15, ' bold '))
data.place(x=600, y=350)

train_model=Label(window, text="Train the model with current user",bg="cornsilk3",font=('arial', 18, ' bold '))#width=12  ,fg="black"  ,bg="cornsilk3"    ,height=2 ,font=('arial', 18, ' bold ')) 
train_model.place(x=960, y=250)

train=Button(window, text="Train->",width=12 ,height=1,command=train_data,activebackground = "tan1",fg="black",font=('arial', 15, ' bold '))#, command=TakeImages ,fg="tan1"  ,bg="PaleGreen1"  ,width=20  ,height=3, activebackground = "tan1" ,font=('arial', 15, ' bold '))
train.place(x=1075, y=350)

status=Label(window, text="Status :",width=6  ,fg="black"  ,bg="cornsilk3"    ,height=2 ,font=('arial', 18, ' bold ')) 
status.place(x=50, y=570)

status_txt=Label(window,width=40 ,bg="white" ,fg="firebrick1",font=('arial', 20, ' bold '))
status_txt.place(x=160, y=585)

Back_btn=Button(window, text="Back to Main Page->",width=18 ,height=2,command=run,activebackground = "tan1",font=('arial', 15, ' bold '))#, command=TakeImages ,fg="tan1"  ,bg="PaleGreen1"  ,width=20  ,height=3, activebackground = "tan1" ,font=('arial', 15, ' bold '))
Back_btn.place(x=1100, y=535)

window.mainloop()
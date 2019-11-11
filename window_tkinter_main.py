#import the necessary packages
from tkinter import *
import pandas as pd
import numpy as np
import cv2
import xlrd
	
#Read the names from the record file to display available users
df=pd.read_excel("records\\Records.xls")
names=[]
names=df['Names']

#function to run the new window
def run():
	window.destroy()
	import window_tkinter
		
#tester function to scan face and predict their names
def tester():
	lbph = cv2.face.LBPHFaceRecognizer_create()
	lbph.read("Trained_model.yml")
	faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")   
	df=pd.read_excel("records\\Records.xls")
	font = cv2.FONT_HERSHEY_SIMPLEX        
	cam = cv2.VideoCapture(0)

	while True:
	    ret, img =cam.read()
	    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	    faces=faceCascade.detectMultiScale(gray, 1.2,5)    
	    for(x,y,w,h) in faces:
	        cv2.rectangle(img,(x,y),(x+w,y+h),(225,0,0),2)
	        Id, conf = lbph.predict(gray[y:y+h,x:x+w])                              

	        if(conf < 50):
	            n=df.loc[df['Rollno'] == Id]['Names'].values           
	        else:
	            Id='Unknown'                
	            n='Unknown'  

	        print("Label",Id)
	        print("Confidence",conf)        
	        cv2.putText(img,str(n),(x,y+h), font, 1,(255,255,255),2)        
	    cv2.imshow('Image',img) 
	    if (cv2.waitKey(1)==ord('q')):
	        break


	cam.release()
	cv2.destroyAllWindows()

#function to quit
def quit():
	exit()

#create a tkinter application
window=Tk()
window.configure(background='cornsilk3')
window.geometry("1500x900")

#create a canvas to draw line
canvas=Canvas(width=1500,height=900,bg='cornsilk3')
line1=canvas.create_line(450,100,450,800,width=8,fill='gray')
canvas.pack()

message=Label(window, text="Security System",bg="RoyalBlue4",fg="white",width=57,height=2,font=('arial', 30, 'bold underline')) 
message.place(x=0, y=0)

Lb1=Label(window,text="Availale Users ",bg='Palegreen4',fg="white",width=16,height=2,font=('arial',18,'bold'))
Lb1.place(x=150, y=130)

add_user_btn  =Button(window, text="Add New User",bg="Palegreen4",fg="white",width=15  ,height=2,command=run,activebackground = "tan1",font=('arial', 25, ' bold '))#, command=TakeImages ,fg="tan1"  ,bg="PaleGreen1"  ,width=20  ,height=3, activebackground = "tan1" ,font=('arial', 15, ' bold '))
add_user_btn.place(x=700, y=350)

tester_btn =Button(window, text="Tester",bg="Palegreen4",fg="white",width=15  ,height=2,command=tester,activebackground = "tan1",font=('arial', 25, ' bold '))#, command=TakeImages ,fg="tan1"  ,bg="PaleGreen1"  ,width=20  ,height=3, activebackground = "tan1" ,font=('arial', 15, ' bold '))
tester_btn.place(x=700, y=200)

quit_btn =Button(window, text="Quit->",width=6 ,bg='lightgray' ,height=1,command=quit,activebackground = "tomato",font=('arial', 22))#, command=TakeImages ,fg="tan1"  ,bg="PaleGreen1"  ,width=20  ,height=3, activebackground = "tan1" ,font=('arial', 15, ' bold '))
quit_btn.place(x=1200, y=550)

#creating a scrollbar and aligning it
frame=Frame(window)
scroll=Scrollbar(frame)
scroll.pack(side=RIGHT,fill=Y)
listbox=Listbox(frame,yscrollcommand=scroll.set,font=('arial',20),width=15,height=10)
listbox.configure(justify=CENTER)
scroll.config(command=listbox.yview)
frame.place(x=150,y=250)

#insert names in scrollbar
for i in range(len(names)):
	listbox.insert(END,names[i])
listbox.pack(side=LEFT)

window.mainloop()
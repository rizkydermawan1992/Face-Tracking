#import all the required modules

import numpy as np
import serial
import time
import sys
import cv2

#Setup Communication path for arduino (In place of 'COM3' put the port to which your arduino is connected)
ard = serial.Serial('COM4', 9600) 
time.sleep(2)
print("Connected to arduino...")

#importing the Haarcascade for face detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#To capture the video stream from webcam.
vid = cv2.VideoCapture(0)

while True:
    _, frame = vid.read()#reads the current frame to the variable frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)#converts frame -> grayscaled image
        
        #the following line detects faces.
        #First parameter is the image on which you want to detect on
        #minSize=() specifies the minimum size of the face in terms of pixels
        #Click the above link to know more about the Cascade Classification
    faces = face_cascade.detectMultiScale(gray, minSize=(80, 80), minNeighbors=3)
        
        #A for loop to detect the faces.
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)#draws a rectangle around the face
        Xpos = x+(w/2)#calculates the X co-ordinate of the center of the face.
        Ypos = y+(h/2)#calcualtes the Y co-ordinate of the center of the face
        if Xpos > 280:                  #The following code blocks check if the face is    
            ard.write('R'.encode()) #on the left, right, top or bottom with respect to the 
            time.sleep(0.01)        #center of the frame. 
        elif Xpos < 360:                #If any of the conditions are true, it send a command to
            ard.write('L'.encode()) #the arduino through the serial bus.
            time.sleep(0.01)
        else:
            ard.write('S'.encode())
            time.sleep(0.01)
        if Ypos > 280:
            ard.write('U'.encode())
            time.sleep(0.01)
        elif Ypos < 200:
            ard.write('D'.encode())
            time.sleep(0.01)
        else:
            ard.write('S'.encode())
            time.sleep(0.01)
        break

    text = "Ypos = " + str(Ypos) + " Xpos = " + str(Xpos)
    cv2.putText(frame, 
                    text, 
                    (10, 20),                     # text position (x0,y0) 
                    cv2.FONT_HERSHEY_SIMPLEX,     # font
                    0.9,                          # font scale 
                    (0, 255, 255),                # color (B, G, R) 
                    1)                            # thickness

    cv2.imshow('frame', frame)#displays the frame in a seperate window.
    k = cv2.waitKey(1)&0xFF
    if(k == ord('q')): #if 'q' is pressed on the keyboard, it exits the while loop.
        break   

cv2.destroyAllWindows() #closes all windows
ard.close() #closes the serial communication
vid.release() #stops receiving video from the web cam.
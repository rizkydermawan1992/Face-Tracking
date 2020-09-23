import numpy as np
import serial
import time
import sys
import cv2

#Silakan sesuaikan dengan port COM yang digunakan
ard = serial.Serial('COM4', 9600) 
time.sleep(2)
print("Connected to arduino...")

#import file xml
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#capture video melalui webcam.
vid = cv2.VideoCapture(0)

while True:
    _, frame = vid.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
    faces = face_cascade.detectMultiScale(gray, minSize=(80, 80), minNeighbors=3)
        
    
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)#menampilkan kerangka persegi di sekitaran wajah
        Xpos = x+(w/2)#calculates the X co-ordinate of the center of the face.
        Ypos = y+(h/2)#calcualtes the Y co-ordinate of the center of the face
        if Xpos > 280:                  
            ard.write('R'.encode())  
            time.sleep(0.01)        
        elif Xpos < 360:                
            ard.write('L'.encode()) 
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
                    (10, 20),                     # posisi teks (x0,y0) 
                    cv2.FONT_HERSHEY_SIMPLEX,     # jenis font
                    0.9,                          # ukuran font 
                    (0, 255, 255),                # warna (B, G, R) 
                    1)                            # ketebalan

    cv2.imshow('frame', frame)#membuka jendela.
    k = cv2.waitKey(1)&0xFF
    if(k == ord('q')): #tekan tombol q pada keyboard untuk mengakhiri looping.
        break   

cv2.destroyAllWindows() #menutup semua jendela
ard.close() #mengakhiri komunikasi serial
vid.release() #mengakhiri capture webcam.

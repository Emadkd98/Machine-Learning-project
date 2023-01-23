






import cv2
import HandTrackingModule as htm
import math
import serial
serialcomm = serial.Serial('COM4', 9600)
cap = cv2.VideoCapture(0)

detector = htm.handDetector(detectionCon=0.75)
tipIds =[4, 8 ,12, 16, 20]
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) !=0:
        #print(lmList[4],lmList[8])
        
        x1, y1 = lmList[4][1], lmList[4][2]
        
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = int((x1+x2)/2), int((y1+y2)/2)
        
        #d=int(math.sqrt(math.pow(x2 - x1, 2)+math.pow(y2 - y1, 2) * 1.0))
        #d=int((d/110)*255)
        d = int(math.hypot(x2-x1, y2-y1))
        

        fingers = []
            #شرط الابهام
        if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
                    #شرط باقي الاصابع
        for id in range (1,5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
                #print(fingers)       
            totalFingers =  fingers.count(1)
            #print(totalFingers)
        if totalFingers == 0:
            cv2.rectangle(img,(10,30),(150,100) ,(0,0,255),cv2.FILLED)
            cv2.putText(img,str('off'),(30,85),cv2.FONT_HERSHEY_COMPLEX,2,(255,0,0),3)
            serialcomm.write(str(totalFingers).encode())
            serialcomm.write(b'L')
        else:
                cv2.circle(img,(x1,y1) , 10, (255,0,255),cv2.FILLED)
                cv2.circle(img,(x2,y2) , 10, (255,0,255),cv2.FILLED)
                cv2.line(img, (x1,y1), (x2,y2),(255,0,255),2)
                cv2.circle(img,(cx,cy) , 10, (255,0,255),cv2.FILLED)
                cv2.rectangle(img,(10,30),(150,100) ,(0,255,0),cv2.FILLED)
                cv2.putText(img,str(d),(20,85),cv2.FONT_HERSHEY_COMPLEX,2,(255,0,0),3)    
                e='H'
        if 5<d<256:
                    
            serialcomm.write(str(d).encode())
            serialcomm.write(b'H')      
            
    cv2.imshow('Image',img)  
    if cv2.waitKey(20) & 0xFF == 27:
        break        
cv2.destroyAllWindows()
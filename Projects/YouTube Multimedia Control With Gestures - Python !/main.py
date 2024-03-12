# Supported For YouTube

import cv2
import mediapipe
import time
import pyautogui
from os import system

capture = cv2.VideoCapture(0)

mpHands =  mediapipe.solutions.hands
Hands = mpHands.Hands()
mpDraw = mediapipe.solutions.drawing_utils


def hit(key):
    pyautogui.keyDown(key)
    return


count = 0
system("cls")
while True:
    captureSuccess,frame = capture.read()
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = Hands.process(frame)
    global id_x_y
    id_x_y = []
    Fingers = []
    id_x_y_HasLandmarks = False
    
    
    if results.multi_hand_landmarks:
        for landmark in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(frame, landmark, mpHands.HAND_CONNECTIONS)          
            for id , lms in enumerate(landmark.landmark):
                h,w,c = frame.shape
                Sx,Sy = int(lms.x*w), int(lms.y*h)
                
                id_x_y.append([id,Sx,Sy])                
                id_x_y_HasLandmarks = True
                if id == 4 or id == 8:
                    cv2.circle(frame,(Sx,Sy),8,(255,0,0),cv2.FILLED)
     
    count+=1    
    
    if id_x_y_HasLandmarks:
        thumbLength_x = abs(id_x_y[0][1] - id_x_y[4][1])
        indexLength_y = abs(id_x_y[0][2] - id_x_y[8][2])
        middleLength_y = abs(id_x_y[0][2] - id_x_y[12][2])
        ringLength_y = abs(id_x_y[0][2] - id_x_y[16][2])
        pinkyLength_y = abs(id_x_y[0][2] - id_x_y[20][2])
        
        conditionLength_y = (abs(id_x_y[0][2] - id_x_y[9][2]))
        
        index = True if indexLength_y > conditionLength_y else False
        middle = True if middleLength_y > conditionLength_y else False
        ring = True if ringLength_y > conditionLength_y else False
        pinky = True if pinkyLength_y > conditionLength_y else False
        
        Fingers.append(index)
        Fingers.append(middle)
        Fingers.append(ring)
        Fingers.append(pinky)
        
        countOfFingers = Fingers.count(True)
        
        
        match(countOfFingers):
            case 0:
                if count%15 == 0:
                    hit('k')
            case 1:
                if count%15 == 0:
                    hit('left')
            case 2:
                if count%15 == 0:
                    hit('right')
            case 3:
                pyautogui.press('volumeup')
            case 4:
                pyautogui.press('volumedown')

import cv2 as cv
import mediapipe as mp
import autopy
import time
import numpy as np
import pyautogui
from pynput.mouse import Button, Controller

import HandDetectionAndRecognition as hdr


mouse = Controller()

cameraWidth = 640
cameraHeight = 480
frameReduction = 100
smootheningValue = 6

previousTime = 0
currentTime = 0
y2Temp = 0
flagDrag = 0
flagRightClick = 0

previousLocationOfX = 0
previousLocationOfY = 0

currentLocationOfX = 0
currentLocationOfY = 0

cap = cv.VideoCapture(0)

cap.set(3, cameraWidth)
cap.set(4, cameraHeight)

detectorAndRecognizer = hdr.handDetector(maxNumHands = 1)

screenWidth, screenHeight = autopy.screen.size()
#print(screenWidth, screenHeight)

while True:

    # Hand Landmarks
    ret, img = cap.read()

    img = detectorAndRecognizer.findHands(img)
    landMarkList, boundingBox = detectorAndRecognizer.findHandlandMarks(img)

    # print(landMarkList)

    # Index and middle fingers tip finding
    lengthOfLandMarkList = len(landMarkList)

    if lengthOfLandMarkList != 0:
        x1, y1 = landMarkList[8][1:]
        x2, y2 = landMarkList[12][1:]

        # print(x1, y1, x2, y2)
        
        # fingers are up or down
        upFingers = detectorAndRecognizer.findingUpFingers()
        #print(upFingers)

        cv.rectangle(img, (frameReduction, frameReduction),
                         (cameraWidth - frameReduction, cameraHeight - frameReduction),
                         (255, 0, 255), 2)

        # Mouse moving if and only if index finger is up
        if upFingers[1] == 1 and upFingers[2] == 0:

            # Convert Coordinates
            x3 = np.interp(x1, (frameReduction, cameraWidth - frameReduction), (0, screenWidth))
            y3 = np.interp(y1, (frameReduction, cameraHeight - frameReduction), (0, screenHeight))

            # Smoothing the values 
            currentLocationOfX = previousLocationOfX + (x3 - previousLocationOfX) / smootheningValue
            currentLocationOfY = previousLocationOfY + (y3 - previousLocationOfY) / smootheningValue

            # Mouse Movement
            autopy.mouse.move(currentLocationOfX, currentLocationOfY)

            length, img, redLineInformation = detectorAndRecognizer.findDistance(4, 8, img)

            # Mouse Drag
            if length < 30 and flagDrag == 0:
                mouse.press(Button.left)
                flagDrag = 1

            if length > 30:
                flagDrag = 0
                mouse.release(Button.left)

            cv.circle(img, (x1, y1), 10, (128, 0, 128), cv.FILLED)
            
            previousLocationOfX = currentLocationOfX
            previousLocationOfY = currentLocationOfY

        # Left Click
        if upFingers[1] == 1 and upFingers[2] == 1 and upFingers[3] == 0 and upFingers[0] == 0:
            # Find distance between fingers
            length, img, redLineInformation = detectorAndRecognizer.findDistance(8, 12, img)
            #print(length)

            if length < 30:
                cv.circle(img, (redLineInformation[4], redLineInformation[5]), 
                          10, (0, 255, 0), cv.FILLED)

                mouse.click(Button.left, 1)
        
        # Right Click
        if upFingers[0] == 0 and upFingers[1] == 1 and upFingers[2] == 0 and upFingers[3] == 0 and upFingers[4] == 1 and flagRightClick == 0: 
            mouse.click(Button.right, 1)
            flagRightClick = 1

        if upFingers[4] == 0:
            flagRightClick = 0

        # Scroll Up and down
        if upFingers[1] == 1 and upFingers[2] == 1 and upFingers[3] == 1 and upFingers[4] == 0:
             if lengthOfLandMarkList != 0:

                x1, y1 = landMarkList[8][1:]
                x2, y2 = landMarkList[12][1:]  

                scrollUpAndDown = y2 - y2Temp

                if scrollUpAndDown > 2:
                    mouse.scroll(0, 1)

                if scrollUpAndDown < -2:
                    mouse.scroll(0,-1)

                y2Temp = y2

    # Frame rate 
    currentTime = time.time()
    fps = 1/(currentTime - previousTime)
    previousTime = currentTime

    cv.putText(img, str(int(fps)), (20, 50), cv.FONT_HERSHEY_COMPLEX_SMALL, 3, 
               (255, 0, 0), 3)

    # Display
    
    cv.imshow("Image", img)
    cv.waitKey(1)

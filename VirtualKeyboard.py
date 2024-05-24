import cv2 as cv
import numpy as np
import time
import pyautogui
import numpy as np
import cvzone
import imutils
import HandDetectionAndRecognition as hdr

cameraWidth = 1280
cameraHeight = 720
a = 80
b = 80
spaceFromStart = 50

flag = 0

cap = cv.VideoCapture(0)

cap.set(cv.CAP_PROP_FRAME_WIDTH, cameraWidth)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, cameraHeight)

detectorAndRecognizer = hdr.handDetector(maxNumHands = 1)

firstLine = ["Tab", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "/"]
secondLine = ["CapsLk", "A", "S", "D", "F", "G", "H", "J", "K", "L", "Enter"]
thirdLine = ["Shift", "Z", "X", "C", "V", "B", "N", "M", ".", "Shift'"]
fourthLine = ["Ctrl", "Win", "Alt", "Space", "Alt'", "Ctrl'", ",", "up"]
fifthLine = ["volup", "voldown", "mute", "lt", "dn", "rt"]


def displayAllKeys(img, numberList):

    imgNew = np.zeros_like(img, np.uint8)

    for key in numberList:

        x, y = key.position
        width, height = key.size

        cvzone.cornerRect(imgNew, (key.position[0], key.position[1], key.size[0], key.size[1]), 15, rt=0)

        cv.rectangle(imgNew, key.position, (x + width, y + height), (1, 1, 1), cv.FILLED)
        cv.putText(imgNew, key.alphabetText, (x + 5, y + 30),
                    cv.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

    out = img.copy()
    alpha = 0.2
    mask = imgNew.astype(bool)
    out[mask] = cv.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]

    return out

class Button():
    def __init__(self, position, alphabetText, size):

        self.position = position
        self.size = size
        self.alphabetText = alphabetText

firstLineList = []
for x, key in enumerate(firstLine):

    if key == "Tab":
        a = 100
        b = 80
        spaceFromStart = 50

    else:
        a = 80
        b = 80
        spaceFromStart = 75

    firstLineList.append(Button([100 * x + spaceFromStart, 100], key, [a, b]))

secondLineList = []
for x, key in enumerate(secondLine):

    if key == "CapsLk":
        a = 135
        b = 80
        spaceFromStart = 50

    elif key == "Enter":
        a = 140
        b = 80
        spaceFromStart = 115

    else:
        a, b = 80, 80
        spaceFromStart = 115

    secondLineList.append(Button([100 * x + spaceFromStart, 200], key, [a, b]))

thirdLineList = []
for x, key in enumerate(thirdLine):

    if key == "Shift":
        a = 188
        b = 80
        spaceFromStart = 50

    elif key == "Shift'":
        a = 188
        b = 80
        spaceFromStart = 163

    else:
        a = 80
        b = 80
        spaceFromStart = 163

    thirdLineList.append(Button([100 * x + spaceFromStart, 300], key, [a, b]))

fourthLineList = []
for x, key in enumerate(fourthLine):

    if key == "Ctrl":
        a = 80
        b = 80
        spaceFromStart = 50

    elif key == "Space":
        a = 300
        b = 80
        spaceFromStart = 50

    elif key == "Alt'" or key == "Ctrl'" or key == ",":
        a = 80
        b = 80
        spaceFromStart = 270

    elif key == "up":
        a = 80
        b = 80
        spaceFromStart = 350

    else:
        a = 80
        b = 80
        spaceFromStart = 50

    fourthLineList.append(Button([100 * x + spaceFromStart, 400], key, [a, b]))

fifthLineList = []
for x, key in enumerate(fifthLine):

    if key == "volup":
        a = 150
        b = 80
        spaceFromStart = 50

    elif key == "voldown":
        a = 170
        b = 80
        spaceFromStart = 130

    elif key == "mute":
        a = 170
        b = 80
        spaceFromStart = 230

    else:
        a = 80
        b = 80
        spaceFromStart = 650

    fifthLineList.append(Button([100 * x + spaceFromStart, 500], key, [a, b]))


while True:

    ret ,img = cap.read()
    img = imutils.resize(img,width=1280,height=640)

    img = detectorAndRecognizer.findHands(img)
    landMarkList, boundingBox = detectorAndRecognizer.findHandlandMarks(img)

    img = displayAllKeys(img, firstLineList)
    img = displayAllKeys(img, secondLineList)
    img = displayAllKeys(img, thirdLineList)
    img = displayAllKeys(img, fourthLineList)
    img = displayAllKeys(img, fifthLineList)

    if landMarkList:

        for key in firstLineList:
            x, y = key.position
            width, height = key.size

            indexFingerTipXPointPosition, indexFingerTipYPointPosition = landMarkList[8][1:]

            if x < indexFingerTipXPointPosition < (x + width) and y < indexFingerTipYPointPosition < (y + height):
                cv.rectangle(img, key.position, (x + width, y + height), (175, 0, 175), cv.FILLED)

                cv.putText(img, key.alphabetText, (x + 5, y + 30),
                    cv.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

                length, image, redLineInformation = detectorAndRecognizer.findDistance(8, 12, img)

                if length < 40 and flag == 0:
                    cv.rectangle(img, key.position, (x + width, y + height), (0, 255, 0), cv.FILLED)

                    cv.putText(img, key.alphabetText, (x + 5, y + 30),
                        cv.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

                    if key.alphabetText.lower() == "tab":
                        pyautogui.press('tab')
                        flag = 1

                    else:
                        pyautogui.press(key.alphabetText.lower())  
                        flag = 1

                if length > 30:
                    flag = 0

        for key in secondLineList:
            x, y = key.position
            width, height = key.size

            indexFingerTipXPointPosition, indexFingerTipYPointPosition = landMarkList[8][1:]

            if x < indexFingerTipXPointPosition < (x + width) and y < indexFingerTipYPointPosition < (y + height):
                cv.rectangle(img, key.position, (x + width, y + height), (175, 0, 175), cv.FILLED)

                cv.putText(img, key.alphabetText, (x + 5, y + 30),
                    cv.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

                length, image, redLineInformation = detectorAndRecognizer.findDistance(8, 12, img)

                if length < 40 and flag == 0:
                    cv.rectangle(img, key.position, (x + width, y + height), (0, 255, 0), cv.FILLED)

                    cv.putText(img, key.alphabetText, (x + 5, y + 30),
                        cv.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

                    if key.alphabetText.lower() == "capslk":
                        pyautogui.press('capslok')
                        flag = 1

                    elif key.alphabetText.lower() == "enter":
                        pyautogui.press('enter')

                    else:
                        pyautogui.press(key.alphabetText.lower())  
                        flag = 1

                if length > 30:
                    flag = 0

        for key in thirdLineList:
            x, y = key.position
            width, height = key.size

            indexFingerTipXPointPosition, indexFingerTipYPointPosition = landMarkList[8][1:]

            if x < indexFingerTipXPointPosition < (x + width) and y < indexFingerTipYPointPosition < (y + height):
                cv.rectangle(img, key.position, (x + width, y + height), (175, 0, 175), cv.FILLED)

                cv.putText(img, key.alphabetText, (x + 5, y + 30),
                    cv.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

                length, image, redLineInformation = detectorAndRecognizer.findDistance(8, 12, img)

                if length < 40 and flag == 0:
                    cv.rectangle(img, key.position, (x + width, y + height), (0, 255, 0), cv.FILLED)

                    cv.putText(img, key.alphabetText, (x + 5, y + 30),
                        cv.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

                    if key.alphabetText.lower() == "shift" or key.alphabetText.lower() == "shift'":
                        pyautogui.press('shift')
                        flag = 1

                    else:
                        pyautogui.press(key.alphabetText.lower())  
                        flag = 1

                if length > 30:
                    flag = 0

        for key in fourthLineList:
            x, y = key.position
            width, height = key.size

            indexFingerTipXPointPosition, indexFingerTipYPointPosition = landMarkList[8][1:]

            if x < indexFingerTipXPointPosition < (x + width) and y < indexFingerTipYPointPosition < (y + height):
                cv.rectangle(img, key.position, (x + width, y + height), (175, 0, 175), cv.FILLED)

                cv.putText(img, key.alphabetText, (x + 5, y + 30),
                    cv.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

                length, image, redLineInformation = detectorAndRecognizer.findDistance(8, 12, img)

                if length < 40 and flag == 0:
                    cv.rectangle(img, key.position, (x + width, y + height), (0, 255, 0), cv.FILLED)

                    cv.putText(img, key.alphabetText, (x + 5, y + 30),
                        cv.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

                    if key.alphabetText.lower() == "ctrl" or key.alphabetText.lower() == "ctrl'":
                        pyautogui.press('ctrl')
                        flag = 1

                    elif key.alphabetText.lower() == "alt" or key.alphabetText.lower() == "alt'":
                        pyautogui.press('alt')
                        flag = 1

                    else:
                        pyautogui.press(key.alphabetText)  
                        flag = 1

                if length > 30:
                    flag = 0

        for key in fifthLineList:
            x, y = key.position
            width, height = key.size

            indexFingerTipXPointPosition, indexFingerTipYPointPosition = landMarkList[8][1:]

            if x < indexFingerTipXPointPosition < (x + width) and y < indexFingerTipYPointPosition < (y + height):
                cv.rectangle(img, key.position, (x + width, y + height), (175, 0, 175), cv.FILLED)

                cv.putText(img, key.alphabetText, (x + 5, y + 30),
                    cv.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

                length, image, redLineInformation = detectorAndRecognizer.findDistance(8, 12, img)

                if length < 40 and flag == 0:
                    cv.rectangle(img, key.position, (x + width, y + height), (0, 255, 0), cv.FILLED)

                    cv.putText(img, key.alphabetText, (x + 5, y + 30),
                        cv.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

                    if key.alphabetText.lower() == "dn":
                        pyautogui.press('down')
                        flag = 1

                    elif key.alphabetText.lower() == "lt":
                        pyautogui.press('left')
                        flag = 1

                    elif key.alphabetText.lower() == "rt":
                        pyautogui.press('right')
                        flag = 1

                    elif key.alphabetText.lower() == "volup":
                        pyautogui.press('volumeup')
                        flag = 1

                    elif key.alphabetText.lower() == "voldown":
                        pyautogui.press('volumedown')
                        flag = 1

                    elif key.alphabetText.lower() == "mute":
                        pyautogui.press('volumemute')
                        flag = 1

                if length > 30:
                    flag = 0

    cv.imshow("Virtual Keyboard", img)
    cv.waitKey(1)
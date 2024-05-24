import cv2 as cv
import mediapipe as mp
import time
import math

class handDetector():

    def __init__(self, staticImageMode = False, maxNumHands = 1, 
                 minDetectionConfidence = 0.5, minTrackingConfidence = 0.5):

        self.staticImageMode = staticImageMode
        self.maxNumHands = maxNumHands

        self.minDetectionConfidence = minDetectionConfidence
        self.minTrackingConfidence = minTrackingConfidence

        self.mpHands = mp.solutions.hands

        self.hands = self.mpHands.Hands(self.staticImageMode, self.maxNumHands, 
                                        self.minDetectionConfidence, self.minTrackingConfidence)

        self.mpDraw = mp.solutions.drawing_utils
        self.drawingStyles = mp.solutions.drawing_styles

        self.fingerTipsIds = [4, 8, 12, 16, 20]

    def findHands(self, image, draw = True):

        image1 = cv.flip(image, 1)
        imgRGB = cv.cvtColor(image1, cv.COLOR_BGR2RGB)

        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:

            for handLandmarks in self.results.multi_hand_landmarks:

                if draw:
                    self.mpDraw.draw_landmarks(image1, handLandmarks, 
                                               self.mpHands.HAND_CONNECTIONS,
                                               self.drawingStyles.get_default_hand_landmark_style(),
                                               self.drawingStyles.get_default_hand_connection_style())

        return image1

    def findHandlandMarks(self, img, handNumber = 0, draw = True):

        xList = []
        yList = []
        boundingBox = []

        self.landMarkList = []

        if self.results.multi_hand_landmarks:

            oneParticularHand = self.results.multi_hand_landmarks[handNumber]

            for id, lm in enumerate(oneParticularHand.landmark):

                imageHeight, imageWidth, c = img.shape

                cx = int(lm.x * imageWidth)
                cy = int(lm.y * imageHeight)

                xList.append(cx)
                yList.append(cy)

                self.landMarkList.append([id, cx, cy])

                if draw:
                    if id == 0:
                        cv.circle(img, (cx, cy), 10, (255, 0, 255), cv.FILLED)

            xMinimum = min(xList)
            xMaximum = max(xList)
            yMinimum = min(yList)
            yMaximum = max(yList)

            boundingBox = xMinimum, yMinimum, xMaximum, yMaximum

            if draw:
                cv.rectangle(img, (xMinimum - 20, yMinimum - 20), (xMaximum + 20, yMaximum + 20), 
                             (0, 255, 0), 2)

        return self.landMarkList, boundingBox

    def findingUpFingers(self):

        upFingersList = []

        #thumb
        if self.landMarkList[self.fingerTipsIds[0]][2] > self.landMarkList[self.fingerTipsIds[0] - 1][2]:
            upFingersList.append(1)

        else:
            upFingersList.append(0)

        #Fingers
        for id in range(1, 5):
            if self.landMarkList[self.fingerTipsIds[id]][2] < self.landMarkList[self.fingerTipsIds[id] - 2][2]:
                upFingersList.append(1)

            else:
                upFingersList.append(0)

        return upFingersList

    def findDistance(self, p1, p2, img, draw = True, r = 10, t = 3):

        x1, y1 = self.landMarkList[p1][1:]
        x2, y2 = self.landMarkList[p2][1:]

        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        if draw:
            cv.line(img, (x1, y1), (x2,y2), (255, 0, 255), t)
            cv.circle(img, (x1, y1), r, (255, 0, 255), cv.FILLED)
            cv.circle(img, (x2, y2), r, (255, 0, 255), cv.FILLED)
            cv.circle(img, (cx, cy), r, (0, 0, 255), cv.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)

        return length, img, [x1, y1, x2, y2, cx, cy]

def main():

    previousTime = 0
    currentTime = 0

    cap = cv.VideoCapture(0)

    detector = handDetector()

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    while True:

        ret ,image = cap.read()

        image = detector.findHands(image)

        landmarkList = detector.findHandlandMarks(image)

        lengthOfLandMarkList = len(landmarkList)

        #if lengthOfLandMarkList != 0:
            #print(landmarkList[4])

        if not ret:
            print("Can't receive frame. Exiting ...")
            break 

        currentTime = time.time()
        fps = 1/(currentTime - previousTime)
        previousTime = currentTime

        cv.putText(image, str(int(fps)), (20, 50), cv.FONT_HERSHEY_COMPLEX_SMALL, 3, 
               (255, 0, 0), 3)

        cv.imshow("Mouse", image)
        cv.waitKey(1)

if __name__ == "__main__":
    main()
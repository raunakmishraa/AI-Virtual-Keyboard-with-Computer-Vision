import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
from pynput.keyboard import Controller

cap = cv2.VideoCapture(0)
cap.set(3, 1000)
cap.set(4, 640)

detector = HandDetector(detectionCon=0.8)

def drawALL(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 5, y + 50), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img

class Button():
    def __init__(self, pos, text, size=[55,55]):
        self.pos = pos
        self.size = size
        self.text = text


keys = [["Q","W","E","R","T","Y","U","I","O","P"],
        ["A","S","D","F","G","H","J","K","L",";"],
        ["Z","X","C","V","B","N","M",",",".","/"]]

buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([60 * j + 50, 60 * i + 50], key))

keyboard = Controller()

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)

    img = drawALL(img, buttonList)

    if lmList:
        for button in buttonList:
            x,y = button.pos
            w,h = button.size
            text = button.text
            if x < lmList[8][0] < x+w and y < lmList[8][1] < y+h:
                fingers = detector.fingersUp()
                thumbFinger = fingers[0]
                indexFinger = fingers[1]
                if str(thumbFinger)=="0" and str(indexFinger)=="1":
                    #print("Hovering")
                    cv2.rectangle(img, button.pos, (x + w, y + h), (175, 0, 175), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 5, y + 50), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                if str(thumbFinger)=="1" and str(indexFinger)=="1":
                    #print("Pressed")
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 5, y + 50), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    keyboard.press(text)
                    keyboard.release(text)
                # if totalFingers == 1:
                #     cv2.rectangle(img, button.pos, (x + w, y + h), (175, 0, 175), cv2.FILLED)
                #     cv2.putText(img, button.text, (x + 5, y + 50), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                #     # l1,_,_ = detector.findDistance(5,9,img, draw=False)
                #     # l2, _, _ = detector.findDistance(6, 10, img, draw=False)
                #     # l = l1 - l2
                # elif totalFingers == 2:
                #     cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                #     cv2.putText(img, button.text, (x + 5, y + 50), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                #     keyboard.press(text)
                    #print("Hello")

                #print(l)
                    #sleep(0.2)

    #img = mybutton.draw(img)

    cv2.imshow("Image", img)
    cv2.waitKey(1)

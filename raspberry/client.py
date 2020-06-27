import cv2 as cv
import os
import numpy as np
import time

#加载训练数据集文件
recogizer=cv.face.LBPHFaceRecognizer_create()
recogizer.read('trainer.yml')
face_detector = cv.CascadeClassifier(
    'haarcascade_frontalface_default.xml')


cap = cv.VideoCapture(0)
# while 1:
#准备识别的图片
# ret, img = cap.read()
img=cv.imread('target.jpg')
gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
faces = face_detector.detectMultiScale(gray)
for x,y,w,h in faces:
    cv.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
    #人脸识别
    id,confidence=recogizer.predict(gray[y:y+h,x:x+w])
    print('标签id:',id,'置信评分：',confidence)
cv.imshow('result',img)
    # if cv.waitKey(1) & 0xFF == ord('q'):
    #     break
    # time.sleep(1)


cv.waitKey(0)
cv.destroyAllWindows()
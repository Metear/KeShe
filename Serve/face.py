import cv2 as cv
import os
import numpy as np


def predict(path):
    # 加载训练数据集文件
    recogizer = cv.face.LBPHFaceRecognizer_create()
    recogizer.read('../confing/trainer.yml')
    # 准备识别的图片
    # img=cv.imread('Target/6.jpg')
    img = cv.imread(path)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    face_detector = cv.CascadeClassifier(
        '../confing/haarcascade_frontalface_default.xml')
    faces = face_detector.detectMultiScale(gray)
    for x, y, w, h in faces:
        cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # 人脸识别
        id, confidence = recogizer.predict(gray[y:y + h, x:x + w])
        print('标签id:', id, '置信评分：', confidence)
    return id, confidence


'''
cv.imshow('result', img)
cv.waitKey(0)
cv.destroyAllWindows()
'''

#camshift.py
#Author: Sean Devonport
#Script that implements camshift.
from face.detector import FaceDetector
import sys
import cv2 as cv
import numpy as np

RATIO = 2

TRACK = 30

SKIP = 2

vidcap = cv.VideoCapture(0)

termination = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT,10,1)

def VJFindFace(frame):
	global RATIO, orig

	allPoiPts = []

	orig = frame.copy()

	dim = (frame.shape[1]/RATIO, frame.shape[0]/RATIO)

	resized = cv.resize(frame, dim, interpolation=cv.INTER_AREA)

	gray = cv2.cvtColor(resized,cv2.COLOR_BGR2GRAY)

	fd = FaceDetector('cascades/haarcascade_frontalface_default.xml')
	faceRects = fd.detect(gray,scaleFactor=1.1,minNeighbours=5,minSize=(10,10))
	# loop over the faces and draw a rectangle around each
	for (x,y,w,h) in faceRects:
		x=RATIO*(x+10)
		y=RATIO*(y+10)
		w=RATIO*(w-15)
		x=RATIO*(h-15)

		allRoiPts.append((x,y,x+w,y+h))

	cv.imshow("Faces",frame)
	cv.waitkey(1)
	return allRoiPts

def calHist(allRoiPts):
	global orig
	allRoiHist=[]

	for roiPts in allRoiPts:

		roi = orig[roiPts[1]:roiPts[-1],roiPts[0]:roiPts[2]]
		roi = cv.cvtColor(roi,cv.COLOR_BGR2HSV)

		roiHist = cv.calcHist([roi],[0],None,[16],[0,180])
		roiHist = cv.normalize(roiHist,roiHist,0,255,cv.NORM_MINMAX)
		allRoiHist.append(roiHist)

	return allRoiHist
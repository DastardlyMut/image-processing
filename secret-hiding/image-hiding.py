'''
image-hiding.py

Author: Sean Devonport

Script that hides message a message in two images

'''

import cv2 as cv
import numpy as np


def steg(filename):
	# read in image, convert to black and white
	img = cv.imread(filename,0)
	rval ,img = cv.threshold(img,135,255,cv.THRESH_BINARY)
	cv.imshow('frame', img)


	cv.waitKey(0)
	cv.destroyAllWindows


steg('kickflip.jpg')
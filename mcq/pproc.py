'''

pproc.py

Author: Sean Devonport

Script that extracts images from pdf and aligns them correctly for processing

'''

import cv2
import os
import numpy as np
import argparse as ap
import cvutils
import math
from matplotlib import pyplot as plt

# def erode_img(img,times):
# 	kernel = np.ones((3,3),np.uint8)
# 	e_img = cv2.erode(img,kernel,iterations=times)
# 	cv2.imshow('e_img',cv2.resize(e_img,(0,0),fx=0.15,fy=0.15))
# 	cv2.waitKey(0)
# 	return e_img

# def dilate_img(img, times):
# 	kernel = np.ones((3,3),np.uint8)
# 	d_img = cv2.dilate(img,kernel,iterations=times)
# 	return d_img


def findCorners(img):
# Finds all corners of MCQ using a template match.
# Returns 4 centre positions of corners. If no_cnrs < 4 then return flag value 1.
	cnr_template = cv2.imread('data/template/corner.ppm',0)
	img2 = img.copy()
	w,h = np.shape(cnr_template)
	corners = []
	accuracy = 0.9
	flg=0
	for i in range(4):
		# Find corner
		res = cv2.matchTemplate(img2, cnr_template,cv2.TM_CCOEFF_NORMED)
		
		#loc =np.where(res >= 0.8)
		# if(res.all() == 0):
		# 	flg=1
		# 	break
		_, max_val, _, max_loc = cv2.minMaxLoc(res)

		if max_val > accuracy:
			# get centre
			top_left = max_loc
			bottom_right = (top_left[0] + w, top_left[1] + h)
			centre = (top_left[0]+30, top_left[1]+30)

			# Draw circle over corner
			cv2.circle(img2,centre,50,(0,255,0),-1)

			# cv2.rectangle(img2,top_left, bottom_right, (0,0,255), 3)
			# cv2.imshow('img',cv2.resize(img2,(0,0),fx=0.2,fy=0.2))
			# cv2.waitKey(0)

			# append corner to list
			corners.append(centre)

	corners = sorted(corners, key=lambda x: x[1])
	if len(corners) != 4:
		flg = 1
	print 'corners: ' + str(corners)
	return corners,flg



# def threshold(img):
# 	thresh = 205
# 	maxValue = 255
# 	th, dst = cv2.threshold(img, thresh, maxValue, cv2.THRESH_BINARY)
# 	return dst

def flipPage(img, cnrs):
# Determines if page is upside down or not. Returns correctly orientated page as image and corners.
	in_img = img
	out_img = img
	corners = cnrs
	w,h = np.shape(img)
	
	# if the top left corner y value < 500, then flip
	if cnrs[0][1] < 500:
		# Flip image
		out_img = cv2.flip(img,-1)
		corners, flg = findCorners(out_img)

	# cv2.imshow('out',cv2.resize(out_img,(0,0),fx=0.2,fy=0.2))
	# cv2.waitKey(0)

	return out_img,corners

def get_angle(pt1,pt2):
# Get angle between two points
	xdiff = pt1[0]-pt2[0]
	ydiff = pt1[1]-pt2[1]
	print xdiff
	print ydiff
	gr = ydiff/xdiff

	deg = np.arctan(gr)

	return deg

	

def fixOrient(img, cnrs):
	out_img=[]
	rows,cols = np.shape(img)
	# print cnrs[0][1]
	# print cnrs[1][1]
	if cnrs[0][1] != cnrs[1][1]:
		# Find angle (in radians) between them
		angle = get_angle(cnrs[0],cnrs[1])
		# rotate image by inverse angle
		print angle
		M = cv2.getRotationMatrix2D((cols/2,rows/2),angle,1)
		out_img = cv2.warpAffine(img,M,(cols,rows))
		corners = findCorners(out_img)
		# out_img = cv2.rotateImage(img,-angle)
		cv2.imshow('rot',cv2.resize(out_img,(0,0),fx=0.2,fy=0.2))
		cv2.waitKey(0)




def procMCQ(mcq):
	# read image in Grayscale
	img = cv2.imread(mcq,0)
	# threshold image
	# img = threshold(img)

	# find corners with template match
	corners,flg = findCorners(img)

	if len(corners) != 0:
		#print corners
		# fix minor orientation


		# turn page upright
		img, corners = flipPage(img, corners)
		#flip_page(img,[(3359, 4314), (129, 100), (178, 4338), (2606, 532)])
		#print corners
		# fix orientation (minor miss alignment)
		fixOrient(img, corners)	

		# get name section





def main():
	# read in ppm images
	ppm_images = cvutils.imlist('data/ppm/600dpi')
	for ppm in ppm_images:
		img = procMCQ(ppm)




procMCQ('data/ppm/600dpi/pg_7.ppm')

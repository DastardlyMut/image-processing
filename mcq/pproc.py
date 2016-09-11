'''

pproc.py

Author: Sean Devonport

Script that extracts images from pdf and aligns them correctly for processing

'''

import cv2
import os
import csv
import numpy as np
import argparse as ap
import cvutils
import math
from matplotlib import pyplot as plt

def erode_img(img,times):
	kernel = np.ones((2,2),np.uint8)
	e_img = cv2.erode(img,kernel,iterations=times)
	return e_img

def dilate_img(img, times):
	kernel = np.ones((2,2),np.uint8)
	d_img = cv2.dilate(img,kernel,iterations=times)
	return d_img

def findCorners(img):
# Finds all corners of MCQ using a template match.
# Returns 4 centre positions of corners. If no_cnrs < 4 then return flag value 1.
	cnr_template = cv2.imread('data/template/corner.ppm',0)
	img2 = img.copy()
	w,h = np.shape(cnr_template)
	corners = []
	accuracy = 0.75
	flg=0
	for i in range(4):
		# Find corner
		res = cv2.matchTemplate(img2, cnr_template,cv2.TM_CCOEFF_NORMED)
	
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

	corners = sorted(corners, key=lambda x: (x[1],x[0]))
	if len(corners) != 4:
		flg = 1
	print 'corners: ' + str(corners)
	return corners,flg

def threshold(img):
	thresh = 240
	maxVal = 1
	th, out = cv2.threshold(img, thresh,maxVal, cv2.THRESH_BINARY)
	return out

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
	xdiff = pt2[0]-pt1[0]
	ydiff = pt2[1]-pt1[1]
	gr = ydiff/xdiff
	rad = np.arctan(gr)

	return rad

def fixOrient(img, cnrs):
	out_img=img
	rows,cols = np.shape(img)
	corners = cnrs
	dist = cnrs[1][1] - cnrs[0][1]

	if dist >= 20:  
		# Find angle (in radians) between them
		angle = get_angle(cnrs[0],cnrs[1])
		# rotate image by inverse angle
		print angle
		M = cv2.getRotationMatrix2D((cols/2,rows/2),angle,1)
		out_img = cv2.warpAffine(img,M,(cols,rows))
		corners,flg = findCorners(out_img)
		# out_img = cv2.rotateImage(img,-angle)
		cv2.imshow('rot',cv2.resize(out_img,(0,0),fx=0.2,fy=0.2))
		cv2.waitKey(0)

	return out_img,corners

def findCircles(seg):
	# Remove noise and blur image
	segb = cv2.medianBlur(seg, 7)
	segb = dilate_img(segb,1)
	segb = erode_img(segb,2)
	# Find circles
 	circles = cv2.HoughCircles(segb,cv2.HOUGH_GRADIENT,1,60,param1=100,param2=40,minRadius=15,maxRadius=200)
 	no_circ = np.shape(circles)

 	for i in circles[0,:]:
 		cv2.circle(segb,(i[0],i[1]),i[2],(0,255,0),0)
 		cv2.circle(segb,(i[0],i[1]),2,(0,0,255),3)

 	cv2.imshow('circles',cv2.resize(segb,(0,0),fx=0.25,fy=0.25) )
 	cv2.waitKey(0)
 	return circles

def detScores(seg,circles):
# Function that gets the circle positions that are filled. If less than 3 circles located 
# then return invalid answer
	out=-1
	# If circles aren't 5 then invalid
	if len(circles) != 5:
		print 'Invalid answer'
		return out
	# Extract retangles from around circle centre
	q = [0]*5
	for i in range(5):
		centre = [circles[i][0],circles[i][1]]
		pos1 = [centre[0]-45,centre[1]-45]
		pos2 = [pos1[0] + 84,pos1[1] + 84]
		rect = seg[pos1[1]:pos2[1],pos1[0]:pos2[0]]

		# cv2.imshow('rec',rect)
		# cv2.waitKey(0)

		# threshold 
		rect = threshold(rect)
		# sum all pixels in array (if less, then more black pixels. i.e filled in)
		px_sum = np.sum(rect)
		# print px_sum
		if (px_sum < 4000):
			q[i]=1

	# If more than 1 answer, invalid answer
	if np.sum(q) != 1:
		print 'Invalid answer'
		return out

	# Find index of answer
	i = q.index(1)

	if i == 0:
		out = 'a'
	elif i == 1:
		out = 'b'
	elif i == 2:
		out = 'c'
	elif i == 3:
		out = 'd'
	elif i == 4:
		out = 'e'

	print 'marked: ' + out
	return out

def getQs(seg):
# segment each q and return scores
	pos1 = [130,70]
	h_inc = 112
	w_inc = 504
	ans = [0]*5

	for i in range(5):
		q = seg[pos1[1]:pos1[1]+h_inc,pos1[0]:pos1[0]+w_inc]

		# cv2.imshow('seg',q)
		# cv2.waitKey(0)

		circles = findCircles(q)[0]
		circles = sorted(circles,key=lambda x : x[0])

		# determine scores
		q_scr = detScores(q,circles)
		ans[i] = q_scr

		# update position
		pos1 = [pos1[0],pos1[1]+100]

	# print "answer for section: " + str(ans)
	return ans

def getScores(img,corners):
# Get scores for blocks
	in_img = img
	seg = []
	scores = []

	# segment MCQ
 	pos1 = (corners[0][0]+1220,corners[0][1]+127)
 	pos2 = (pos1[0]+630,pos1[1]+630)
 	
 	# print 'seg corners ' + str(corners)

 	for i in range(12):
 		seg = in_img[pos1[1]:pos2[1],pos1[0]:pos2[0]]
		cv2.imshow('seg',seg)
 		cv2.waitKey(0)

 		# Get answers for block
 		q = getQs(seg)
 		print 'Answer for section ' + str(i) + ':' + str(q)
 		# Append to answer list
 		scores.append(q)

 		# Update positions
 		pos1 = (pos1[0],pos1[1]+660)
 		pos2 = (pos2[0],pos2[1]+660)

 		if i == 5:
 			pos1 = (corners[0][0]+2180,corners[0][1]+127)
 			pos2 = (pos1[0]+630,pos1[1]+630)
 	
 	# Flatten array
	scores = np.hstack(scores)
	return scores

def encodeChar(sec):
	i = sec.index(1)
	if i == 0:
		return 'a'
	elif i == 1:
		return 'b'
	elif i == 2:
		return 'c'
	elif i == 3:
		return 'd'
	elif i == 4:
		return 'e'
	elif i == 5:
		return 'f'
	elif i == 6:
		return 'g'
	elif i == 7:
		return 'h'
	elif i == 8:
		return 'i'
	elif i == 9:
		return 'j'
	elif i == 10:
		return 'k'
	elif i == 11:
		return 'l'
	elif i == 12:
		return 'm'
	elif i == 13:
		return 'n'
	elif i == 14:
		return 'o'
	elif i == 15:
		return 'p'
	elif i == 16:
		return 'q'
	elif i == 17:
		return 'r'
	elif i == 18:
		return 's'
	elif i == 19:
		return 't'
	elif i == 20:
		return 'u'
	elif i == 21:
		return 'v'
	elif i == 22:
		return 'w'
	elif i == 23:
		return 'x'
	elif i == 24:
		return 'y'
	elif i == 25:
		return 'z'
	else:
		return -1
# Encode char

def detCharMarked(seg,circles,no_circ):
# Determine marked char circle
	rects = []
	a = [0]*25

	for i in range(no_circ):
		centre = [circles[i][0],circles[i][1]]
		pos1 = [centre[0]-45,centre[1]-45]
		pos2 = [pos1[0] + 84,pos1[1] + 84]
		rect = seg[pos1[1]:pos2[1],pos1[0]:pos2[0]]

		# threshold 
		rect = threshold(rect)
		# sum all pixels in array (if less, then more black pixels. i.e filled in)
		px_sum = np.sum(rect)
		# print px_sum
		if (px_sum < 4000):
			a[i]=1

		# If more than 1 answer, invalid answer
	if np.sum(a) != 1:
		print 'Invalid answer'
		return -1

	# Encode char
	out = encodeChar(a)

	print 'marked: ' + out
	return out

def encodeNo(sec):
	i = sec.index(1)
	if i == 0:
		return '0'
	elif i == 1:
		return '1'
	elif i == 2:
		return '2'
	elif i == 3:
		return '3'
	elif i == 4:
		return '4'
	elif i == 5:
		return '5'
	elif i == 6:
		return '6'
	elif i == 7:
		return '7'
	elif i == 8:
		return '8'
	elif i == 9:
		return '9'
	else:
		return -1
# encode num

def detNoMarked(seg,circles,no_circ):
# Determine marked char circle
	rects = []
	a = [0]*25
	for i in range(no_circ):
		centre = [circles[i][0],circles[i][1]]
		pos1 = [centre[0]-45,centre[1]-45]
		pos2 = [pos1[0] + 84,pos1[1] + 84]
		rect = seg[pos1[1]:pos2[1],pos1[0]:pos2[0]]

		# threshold 
		rect = threshold(rect)
		# sum all pixels in array (if less, then more black pixels. i.e filled in)
		px_sum = np.sum(rect)
		# print px_sum
		if (px_sum < 4000):
			a[i]=1

		# If more than 1 answer, invalid answer
	if np.sum(a) != 1:
		print 'Invalid answer'
		return -1

	# Encode char
	out = encodeNo(a)

	print 'marked: ' + out
	return out

def detStudNo(seg,circles):
# Determine which circle filled in
	out = []
	no_circ = len(circles)

	if no_circ == 26:
	# If alphabet column
		out = detCharMarked(seg,circles,no_circ)
		return out
	if no_circ != 10:
		print 'Invalid Student No'
		return -1
	else:
	# Number column
		out = detNoMarked(seg,circles,no_circ)
		return out

def getStudNo(img,corners):
# Take in section and get student number
	in_img = img.copy()
	cnrs = corners
	stu_no = []
	circles = []

	#### Crop verticle rectangle

	# Start point
	pos1 = (cnrs[0][0]+165,cnrs[0][1] +605)
	pos2 = (pos1[0]+120,pos1[1]+1160)
	x_off = 113
	y_off = 1810

	for i in range(7):
		seg = in_img[pos1[1]:pos2[1],pos1[0]:pos2[0]]
		cv2.imshow('seg',cv2.resize(seg,(0,0),fx=0.2,fy=0.2))
		cv2.waitKey(0)

		circles=findCircles(seg)[0]
		circles=sorted(circles,key=lambda x : x[1])

		# Determine which circle filled in and append
		mark = detStudNo(seg,circles)

		stu_no.append(mark)

		if i == 1:
		# If i third column extend window segment
			pos1 = [pos1[0]+x_off, pos1[1]]
			pos2 = [pos2[0]+x_off, pos2[1]+y_off]

		elif i == 2:
		# Return back to original
			pos1 = [pos1[0]+x_off, pos1[1]]
			pos2 = [pos2[0]+x_off, pos2[1]-y_off]
		else:
			pos1 = [pos1[0]+x_off, pos1[1]]
			pos2 = [pos2[0]+x_off, pos2[1]]


	if -1 in stu_no:
		stu_no = 'Invalid Student No'
	else:
		stu_no = ''.join(stu_no)

	print 'Student No: ' +  str(stu_no)
	return stu_no

def detTaskNo(seg,circles):
# Take in image and get task number
	no_circ = len(circles)
	rects = []
	out = [0]*10
	print len(circles)
	for i in range(no_circ):
		centre = [circles[i][0],circles[i][1]]
		pos1 = [centre[0]-45,centre[1]-45]
		pos2 = [pos1[0] + 84,pos1[1] + 84]
		rect = seg[pos1[1]:pos2[1],pos1[0]:pos2[0]]

		# threshold 
		rect = threshold(rect)
		# sum all pixels in array (if less, then more black pixels. i.e filled in)
		px_sum = np.sum(rect)
		# print px_sum
		if (px_sum < 4000):
			out[i]=1

	print 'Tasks Filled: ' + str(out)
	return out

def getTaskNo(img,corners):
# Take in image and get task number
	in_img = img.copy()
	cnrs = corners
	task_no = []
	circles = []

	#### Crop verticle rectangle

	# Start point
	pos1 = (cnrs[0][0]+712,cnrs[0][1] + 2008)
	pos2 = (pos1[0]+117,pos1[1]+1160)
	x_off = 100
	y_off = 1810

	for i in range(2):
		seg = in_img[pos1[1]:pos2[1],pos1[0]:pos2[0]]
		cv2.imshow('seg',cv2.resize(seg,(0,0),fx=0.2,fy=0.2))
		cv2.waitKey(0)

		circles=findCircles(seg)[0]
		circles=sorted(circles,key=lambda x : x[1])

		# Determine which circle filled in and append
		mark = detTaskNo(seg,circles)

		task_no.append(mark)

		if i == 1:
		# If i third column extend window segment
			pos1 = [pos1[0]+x_off, pos1[1]]
			pos2 = [pos2[0]+x_off, pos2[1]+y_off]

		elif i == 2:
		# Return back to original
			pos1 = [pos1[0]+x_off, pos1[1]]
			pos2 = [pos2[0]+x_off, pos2[1]-y_off]
		else:
			pos1 = [pos1[0]+x_off, pos1[1]]
			pos2 = [pos2[0]+x_off, pos2[1]]


	task_no = np.hstack(task_no)

	print 'Task No: ' +  str(task_no)
	return task_no

def writeCSV(data,filename):
# Write CSV file
	# Unpack data
	name = data[0]
	stud_no = data[1]
	tasks = data[2]
	questions = data[3]
	print name
	print stud_no
	print tasks
	print questions
	with open(filename,'w') as csvfile:
		a = csv.writer(csvfile, delimiter=',')
		a.writerow(('Filename:',name))
		a.writerow(('Student No: ',stud_no))
		a.writerow(('Tasks Completed: ','', tasks))
		a.writerow(('Questions: ','',range(0,60)))
		a.writerow(('','',questions))
		csvfile.close()

def procMCQ(mcq):
	# read image in grayscale
	img = cv2.imread(mcq,0)
	# get image name for printing
	name = mcq.split('/')[3]
	# find corners with template match
	corners,flg = findCorners(img)

	if len(corners) >= 2:
		# turn page upright
		img, corners = flipPage(img, corners)
		# fix orientation (minor miss alignment)
		img, corners = fixOrient(img, corners)
		# get student number of mcq
		stud_no = getStudNo(img,corners)
		# get tasks completed from mcq
		task_no = getTaskNo(img,corners)
		# get scores from mcq
		scores = getScores(img,corners)
		# pack data
		all_data = [name, stud_no,task_no,scores]
		# print to csv
		writeCSV(all_data,'output.csv')
		# return [name, stud_no,task_no,scores]

	else:
		print 'No corners not found on this MCQ - Invalid MCQ'
		return -1


def main():
	# read in ppm images
	ppm_images = cvutils.imlist('data/ppm/600dpi')
	comp_mcqs = []
	for ppm in ppm_images:
		comp_mcq = procMCQ(ppm)
		comp_mcqs.append(comp_mcq)


# main()
# Problem case pg_16 (sort corners)
# Need slightly different formulation for larger image ( check if image resize works?)
procMCQ('data/ppm/600dpi/pg_1.ppm')

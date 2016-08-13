#vid_bsub.py
#Author: Sean Devonport
#Script that takes in video and applies basic frame differencing to frames.
import sys
import numpy as np
import cv2
import py_compile

def main(filename):
	# Name address of IP camera
	IP = "http://10.0.0.4:8080/video"

	# Open video capture
	vidcap = cv2.VideoCapture(IP)
	frames = [0]*3
	pF = [0]*2
	thr = 100;

	#capture first frame (background)
	success, pB = vidcap.read()
	size = np.shape(pB)
	cv2.imshow('Frame',pB)
	pB = cv2.cvtColor(pB,cv2.COLOR_BGR2GRAY)

	while (True):
		success,pCur = vidcap.read()
		pCur = cv2.cvtColor(pCur,cv2.COLOR_BGR2GRAY)
		if success:		
			# Do processing
			# calculate foreground mask
			for i in range(size[0]):
				for j in range(size[1]):
					cond=abs(int(pCur[i][j])-int(pB[i][j]))
					if cond >thr:
						pCur[i][j]=255
					else:
						pCur[i][j]=0

			cv2.imshow('fdif',pCur)

			# Save video frames
			if cv2.waitKey(2) & 0xFF == 27:
				break
		else:
			break

	vidcap.release()
	cv2.destroyAllWindows()

main(sys.argv[0])

#vid_framedif.py
#Author: Sean Devonport
#Script that takes in video and applies basic frame differencing to frames.
import sys
import numpy as np
import cv2

def main(filename):
	# Name address of IP camera
	IP = "http://10.0.0.4:8080/video"

	# Open video capture
	vidcap = cv2.VideoCapture(IP)
	frames = [0]*3
	pF = [0]*2
	thr = 12000;

	success, pB = vidcap.read()
	cv2.imshow('Frame',pB)
	pB = cv2.cvtColor(pB,cv2.COLOR_BGR2GRAY)

	while (True):
		success,pFr = vidcap.read()
		pFr = cv2.cvtColor(pFr,cv2.COLOR_BGR2GRAY)
		if success:		
			# Do processing

			# calculate foreground mask
			# update background
			fgmsk = pB - pFr
			if np.sqrt(np.sum(np.power(fgmsk,2))) > thr:
				pB = pFr
				cv2.imshow('FG Mask',fgmsk)

			# Save video frames
			#cv2.imwrite("stvidcap_out/frame%d.ppm" % count, img) #save frame as PPM file.
			if cv2.waitKey(20) & 0xFF == 27:
				break
		else:
			break

	vidcap.release()
	cv2.destroyAllWindows()

main(sys.argv[0])

'''
vid_ravg.py

Author: Sean Devonport

Script that takes in video and applies basic frame differencing to frames.

'''
import sys
import numpy as np
import cv2

def main(filename):
	# Name address of IP camera
	IP = "http://10.0.0.4:8080/video"

	# Open video capture
	vidcap = cv2.VideoCapture(0)
	thr = 20
	lr=0.05

	# capture frame at T(i-1)
	success, pB = vidcap.read()
	size = np.shape(pB)
	sclsize = [int(round(size[0]/2)),int(round(size[1]/2))]	

	pB = cv2.cvtColor(pB,cv2.COLOR_BGR2GRAY)
	pB=cv2.resize(pB,(sclsize[1],sclsize[0]),cv2.INTER_AREA)


	while (True):
		#capture frame at T(i)
		success,pCur = vidcap.read()
		pCur = cv2.cvtColor(pCur,cv2.COLOR_BGR2GRAY)
		pCur=cv2.resize(pCur,(sclsize[1],sclsize[0]),cv2.INTER_AREA)

		if success:		
			out = pB

			# calculate B(t)=alpha*F(t) + (1-alpha)*B(t-1)
			pB=lr*pCur+(1-lr)*pB

			for i in range(sclsize[0]):
				for j in range(sclsize[1]):
					cond=abs(int(pCur[i][j])-int(pB[i][j]))
					if cond > thr:
						out[i][j]=255
					else:
						out[i][j]=0
			
			out = cv2.resize(out,(size[1],size[0]),cv2.INTER_LINEAR)
			cv2.imshow('fdif',out)
			cv2.imshow('background',pB)
			# Save video frames
			if cv2.waitKey(2) & 0xFF == 27:
				break
		else:
			break

	vidcap.release()
	cv2.destroyAllWindows()

main(sys.argv[0])
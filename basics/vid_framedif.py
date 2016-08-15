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
	vidcap = cv2.VideoCapture(0)
	thr = 20;

	# capture frame at T(i-1)
	success, pB = vidcap.read()
	size = np.shape(pB)
	# sclsize = [30,30]
	pB = cv2.cvtColor(pB,cv2.COLOR_BGR2GRAY)
	# sclpB=cv2.resize(pB,(0,0),0.5,0.5,cv2.INTER_AREA)
	out=pB
	while (True):
		#capture frame at T(i)
		success,pCur = vidcap.read()
		pCur = cv2.cvtColor(pCur,cv2.COLOR_BGR2GRAY)
		# sclpCur = cv2.resize(pCur,(0,0),0.5,0.5,cv2.INTER_AREA)
		if success:		
			for i in range(size[0]):
				for j in range(size[1]):
					cond=abs(int(pCur[i][j])-int(pB[i][j]))
					if cond >thr:
						out[i][j]=255
					else:
						out[i][j]=0

			# for i in range(sclsize[0]):
			# 	for j in range(sclsize[1]):
			# 		cond=abs(int(sclpCur[i][j])-int(sclpB[i][j]))
			# 		if cond >thr:
			# 			out[i][j]=255
			# 		else:
			# 			out[i][j]=0
			#print(pCur[(i*size[0])][j])
			# out=cv2.resize(out,(0,0),1.5,1.5,cv2.INTER_LINEAR);
			
			cv2.imshow('fdif',out)
			# update background frame
			pB=pCur
			# Save video frames
			#cv2.imwrite("stvidcap_out/frame%d.ppm" % count, img) #save frame as PPM file.
			if cv2.waitKey(2) & 0xFF == 27:
				break
		else:
			break

	vidcap.release()
	cv2.destroyAllWindows()

main(sys.argv[0])

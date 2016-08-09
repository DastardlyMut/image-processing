#videocapture_std.py
#Author: Sean Devonport
#Script that takes in video and converts to frames.
import sys
import numpy as py
import cv2

def main(filename):
	# Name address of IP camera
	IP = "http://10.0.0.4:8080/video"

	# Open video capture
	vidcap = cv2.VideoCapture(IP)

	while (True):
		success,frame = vidcap.read()
		if success:

			# Save video frames
			#cv2.imwrite("stvidcap_out/frame%d.ppm" % count, img) #save frame as PPM file.
			cv2.imshow('frame',frame)
			if cv2.waitKey(1) & 0xFF == 27:
				break
		else:
			break

	vidcap.release()
	cv2.destroyAllWindows()

main(sys.argv[0])

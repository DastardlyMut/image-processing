'''

secret-hiding_decode.py

Author: Sean Devonport

Script that decodes hidden message

'''

import cv2 as cv
import numpy as np

def bin_to_str(binary,length=8):	
	input_l = [binary[i:i+length] for i in range(0,len(binary),length)]
	return ''.join([chr(int(c,base=2)) for c in input_l])

def decode(filename):
	img=cv.imread(filename)
	sz_img=np.shape(img)

	# convert image to binary
	b_img = [[[(bin(img[i][j][k]))[2:].zfill(8) for k in range(0,3)] for j in range(0,sz_img[1])] for i in range(0,sz_img[0])]
	
	# retrieve msg from image
	#decode header from first px
	msg_len = int(str(b_img[0][0][0][4:]) + str(b_img[0][0][1][4:]),2)
	print msg_len
	msg=''
	b_msg=''
	for i in range(1,msg_len):
		if(len(msg)==20):
			b_msg+=str(b_img[0][i][0][4:]) + str(b_img[0][i][1][4:]) 
			break
		else:
			b_msg+=str(b_img[0][i][0][4:]) + str(b_img[0][i][1][4:]) + str(b_img[0][i][2][4:])
		
	print b_msg

	msg = bin_to_str(b_msg)

	#clean up
	end = msg.find('*')
	msg = msg[:end]

	print msg

decode('encoded.ppm')
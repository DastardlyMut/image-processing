'''

secret-hiding.py

Author: Sean Devonport

Script that hides message a message in an image

'''

import cv2 as cv
import numpy as np
import binascii as b

def encode(word):

	encoded=list(bin(reduce(lambda x, y: 256*x+y, (ord(c) for c in word), 0)))
	
	# Get into pure binary format
	fb = encoded.pop(0)
	encoded.pop(0)

	encoded = [fb] + encoded
	encoded = "".join(encoded)

	return encoded

def decode(binary,length=8):
	
	input_l = [binary[i:i+length] for i in range(0,len(binary),length)]

	return ''.join([chr(int(c,base=2)) for c in input_l])


def main(filename):
	# read in image, convert to grayscale
	img = cv.imread(filename,0)
	
	msg = 'I like to hide things'
	bin_msg = encode(msg)
	print(bin_msg)
	cv.imshow('frame', img)

	asc_msg = decode(bin_msg)

	print(asc_msg)

	cv.imwrite('grayscaled.ppm',img,[cv.IMWRITE_PXM_BINARY,0])
	cv.waitKey(0)
	cv.destroyAllWindows


main('kickflip.jpg')
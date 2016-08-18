'''

secret-hiding_encode.py

Author: Sean Devonport

Script that hides message in an image

'''

import cv2 as cv
import numpy as np

def str_to_bin(word):
	encoded=list(bin(reduce(lambda x, y: 256*x+y, (ord(c) for c in word), 0)))
	encoded.remove('b')
	return ''.join(encoded)

def bin_to_str(binary,length=8):	
	input_l = [binary[i:i+length] for i in range(0,len(binary),length)]
	return ''.join([chr(int(c,base=2)) for c in input_l])

def writeFile(name,pixels,mxcolour=255):
	ppm_out = open(name+'.ppm','w')
	n_px=np.shape(pixels)
	header = "P3\n# This is a plain old image made by Sean Devonport\n{0} {1}\n{2}\n".format(n_px[0],n_px[1],mxcolour)
	ppm_out.write(header)
	for i in range(0,n_px[0]):
		for j in range(0,n_px[1]):
			ppm_out.write("{0} {1} {2}\n".format(pixels[i][j][2],pixels[i][j][1],pixels[i][j][0]))
	ppm_out.close() 


def encode_img(b_msg,b_img):
	# Function which encodes a message into an image. Writes the image to new file and returns the encoded binary array
	n_msg = len(b_msg)
	len_msg = n_msg/8
	blen_msg = bin(len_msg)[2:].zfill(8)
	n_px = np.shape(b_img)

	#encode header (amount of characters)
	for k in range(0,2):
		#encode header into first first item px
	 		piece = blen_msg[:4]
			blen_msg = blen_msg[4:]
			b_img[0][0][k]=b_img[0][0][k][:4] + str(piece)

	# encode into image
	i=1;
	while len(b_msg) > 0:
		# pop off piece from msg
		#encode into px 4 'unimportant' bits
		for j in range(0,3):
	 		piece = b_msg[:4]
			b_msg = b_msg[4:]
			if len(b_msg) == 0:
				break	
			b_img[0][i][j]=b_img[0][i][j][:4] + str(piece)
		i+=1

	# encode back into BGR
	enc_img = [[[int(str(b_img[i][j][k]),2) for k in range(0,3)] for j in range(0,n_px[1])] for i in range(0,n_px[0])]
	print b_img[0][1]
	print enc_img[0][1]
	# write to file
	writeFile('encoded',enc_img)

	return cv.imread('encoded.ppm')


def encode(filename,msg='I like to hide things'):
	# read in image, convert to binary
	img = cv.imread(filename)
	sz_img=np.shape(img)

	# convert image to binary
	bin_img = [[[(bin(img[i][j][k]))[2:].zfill(8) for k in range(0,3)] for j in range(0,sz_img[1])] for i in range(0,sz_img[0])]

	# Convert secret message to binary
	bin_msg = str_to_bin(msg)
	# encode the image
	enc_img=encode_img(bin_msg,bin_img)

	#print asc_msg
	cv.imshow('original', img)
	cv.imshow('encode',img)
	cv.waitKey(0)
	cv.destroyAllWindows


encode('kickflip.ppm')
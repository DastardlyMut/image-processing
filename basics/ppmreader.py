#ppmreader.py
#Author: Sean Devonport
#This script reads in a .ppm format created by GIMP. 
#It returns the size, max colour and pixels.
#Thanks to caramel-koala for help with structure.

import sys

def ppmreader(ppmfile):

	file = open(ppmfile)

	data = file.readlines()

	# Extract data

	ppm_size = data[2]
	ppm_size = ppm_size.split(' ')
	ppm_mxcolour = data[3]
	ppm_pixels = data[4:len(data)]

	size = map(int,ppm_size)
	mxcolour = int(ppm_mxcolour)
	img = map(int,ppm_pixels)

	pixels = [img[3*i:3*(i+1)] for i in range(len(img)/3)]
    	
	file.close()

	return [size,mxcolour,pixels]


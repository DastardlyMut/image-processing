#grayscale.py
#Author: Sean Devonport
#This script takes a .ppm image, does a grayscale transformation
#and returns the grayscaled image. Test images taken from GIMP.
import sys
import numpy

def main(filename):
	#open file.
	ppm_in = open('testcard32.ppm','r')
	ppm_out = open('output.ppm','w')
	#extract headers from .ppm file.
	ppmformat = ppm_in.readline()
	comment = ppm_in.readline().splitlines()
	size_width,size_height = ppm_in.readline().split()
	size_width = int(size_width)
	size_height = int(size_height)
	maxcolour = int(ppm_in.readline())
	#read body of file.
	# pixels = ppm_in.read().split()
	outRGB = [];
	#read in bits and apply transformation
	for i in range(size_width):
		for j in range(size_height):
			tR = ppm_in.readline()
			tG = ppm_in.readline()
			tB = ppm_in.readline()

			tGray = 0.299*float(tR) + 0.587*float(tG) + 0.114*float(tB)

			outRGB.append([int(tGray),int(tGray),int(tGray)])
	
	print(outRGB)
	#print to output file
	ppm_out.write("{0} \n".format(ppmformat))
	ppm_out.write("# This image has been grayscaled by Sean Devonport \n")
	ppm_out.write("{0:3d} {0:3d} \n".format(size_width,size_height))
	ppm_out.write("{0:3d} \n".format(maxcolour))

	for i in range(size_width):
		for j in range(size_height): 
			tRGB = outRGB.pop(0)
			ppm_out.write("{0:3d} {0:3d} {0:3d} \n".format(tRGB[0],tRGB[1],tRGB[2]))


	ppm_in.close()
	ppm_out.close()

main(sys.argv[1])
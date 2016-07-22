#grayscale_correct.py
#Author: Sean Devonport
#This script takes a .ppm image, does a grayscale transformation using average
#and returns the grayscaled image. Test images taken from GIMP.
import sys
import ppmreader as reader

def main(filename):
	#open and extract headers from .ppm file.
	[size,mxcolour,pixels] = reader.ppmreader(filename)

	header = "P2\n# This is image has been grayscaled by Sean Devonport\n{0} {1}\n{2}\n".format(size[0],size[1],mxcolour)

	#create output file to print to.
	ppm_out = open('output.pgm','w')

	ppm_out.write(header)

	#Apply transformation to pixels and print
	for i in pixels:
		tGray = i[0] * 0.299 + i[1] * 0.587 + i[2] * 0.114
		ppm_out.write("%d\n"%(tGray))

	ppm_out.close()

main(sys.argv[1])
#grayscale_avg.py
#Author: Sean Devonport
#This script takes a .ppm image, does a grayscale transformation using average
#and returns the grayscaled image. Test images taken from GIMP.
import sys
import ppmreader as reader

def main(filename):
	#open and extract from .ppm file.
	[size,mxcolour,pixels] = reader.ppmreader(filename)

	#create output file to print to.
	ppm_out = open('output_gray_avg.pgm','w')

	header = "P2\n# This is image has been grayscaled by Sean Devonport\n{0} {1}\n{2}\n".format(size[0],size[1],mxcolour)

	# print header to output
	ppm_out.write(header)

	#Apply transformation to pixels and print
	for i in pixels:
		tGray = (i[0]+i[1]+i[2])/3
		ppm_out.write("%d\n"%tGray)

	ppm_out.close()

main(sys.argv[1])

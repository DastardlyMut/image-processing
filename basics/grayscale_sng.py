#grayscale_sng.py
#Author: Sean Devonport
#This script takes a .ppm image, does a grayscale transformation using single RGB
#and returns the grayscaled image for each channel.
#Test images taken from GIMP.

import sys
import ppmreader as reader

def main(filename):
	#open and extract headers from .ppm file.
	[size,mxcolour,pixels] = reader.ppmreader(filename)

	header = "P2\n# This is image has been grayscaled by Sean Devonport\n{0} {1}\n{2}\n".format(size[0],size[1],mxcolour)

	#create output file for each channel.
	ppm_r = open('output_sc_r.pgm','w')
	ppm_g = open('output_sc_g.pgm','w')
	ppm_b = open('output_sc_b.pgm','w')

	# print header to output files
	ppm_r.write(header)
	ppm_g.write(header)
	ppm_b.write(header)

	#Apply transformation to pixels and print
	for i in pixels:
		ppm_r.write("%d\n"%(i[0]))
		ppm_g.write("%d\n"%(i[1]))
		ppm_b.write("%d\n"%(i[2]))

	ppm_r.close()
	ppm_g.close()
	ppm_b.close()

main(sys.argv[1])
#resize.py
#Author: Sean Devonport
#Script that implements nearest neighbour or linear interpolation rescaling.
#Uses a GIMP extracted .ppm format. 
#Takes 'nn' parameter to decide on nearest neighbour algorithm or linear interpolation.

import sys
import math
import ppmreader as reader

def main(filename, xr, yr, nn):
	#open and extract from .ppm file.
	[size, mxcolour, pixels] = reader.ppmreader(filename)

	# out_size = [xr, yr]

	# x_ratio = float(size[0]/int(out_size[0]))
	# y_ratio = float(size[1]/int(out_size[1]))

	x_ratio = float(xr)
	y_ratio = float(yr)

	out_size = [int(size[0]*x_ratio), int(size[1]*y_ratio)]
	
	header = "P3\n# This is image has been resized by Sean Devonport\n{0} {1}\n{2}\n".format(out_size[0],out_size[1],mxcolour)

	ppm_out = open('output_scaled.ppm','w')

	ppm_out.write(header)

	#create output array
	output = [0]*out_size[0]*out_size[1]

	if nn:
		for i in range(out_size[1]):
			for j in range(out_size[0]):
				x = int(j/x_ratio)
				y = int(i/y_ratio)

				output[(i*out_size[0])+j] = pixels[(y*size[0])+x]
	else:
		for i in range(out_size[1]):
			for j in range(out_size[0]):
				x = int(j/x_ratio)
				y = int(i/y_ratio)

				xd = (j/x_ratio) - x
				yd = (i/y_ratio) - y

				ind = y*size[0]+x
				a = pixels[ind]
				b = pixels[(ind+1)]
				c = pixels[(ind+size[0])]
				d = pixels[(ind+size[0]+1)]

				r = int(a[0]*(1-xd)*(1-yd) + b[0]*xd*(1-yd) + c[0]*(yd)*(1-xd) + d[0]*(xd*yd))
				g = int(a[1]*(1-xd)*(1-yd) + b[1]*xd*(1-yd) + c[1]*(yd)*(1-xd) + d[1]*(xd*yd))
				b = int(a[2]*(1-xd)*(1-yd) + b[2]*xd*(1-yd) + c[2]*(yd)*(1-xd) + d[2]*(xd*yd))

				output[(i*out_size[0])+j] = [r,g,b]

	for p in output:
		ppm_out.write("{0} {1} {2}\n".format(p[0],p[1],p[2]))


	ppm_out.close()


main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
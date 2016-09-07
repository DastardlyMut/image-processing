'''

pdf2ppm.py

Author: Sean Devonport

Script that extracts images from pdf and extract ppm images

'''

from wand.image import Image
import cv2
import cvutils

def pdf2jpg(filename):
	with Image(filename=filename,resolution=(600,600)) as img:
		img_width = img.width
		img.format = 'jpeg'
		img.save(filename="data/jpeg/pg.jpeg")

def pdf2ppm(filename):
	# Convert pdf to jpeg and save in data/jpeg
	pdf2jpg(filename)

	# Get image path
	jpg_images = cvutils.imlist('data/jpeg')

	# Read in jpeg and convert to ppm and save in data/ppm
	i = 0;
	for jpg in jpg_images:
		# Read jpg
		img = cv2.imread(jpg)
		# print i
		cv2.imwrite('data/ppm/pg_'+ str(i) + '.ppm',img)
		i+=1

pdf2ppm('data/600dpi.pdf')
# jpg2ppm('data/jpg/pg-0.ppm')
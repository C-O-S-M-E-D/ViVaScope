import sys
import os
import math
import matplotlib.pyplot as plt
import numpy as np
import cv2
import time
import threading
from collections import Counter


def clean( chip, passes, kernel_size):
	if passes == 0:
		return chip
	
	temp = np.zeros(chip.shape)	
	for y in xrange( 0, chip.shape[0] ):
		for x in xrange( 0, chip.shape[1] ):

			xs = [x]
			ys = [y]
			for h in xrange( 1, kernel_size+1 ):
				xs = xs + [x+h] + [x-h]
				ys = ys + [y+h] + [y-h]
			
			neighbors = []
			for i in xs:
				for j in ys:
					if not ( i == x and j == y ):
						neighbors = neighbors + [[j,i]]		

			neighbors = [ i for i in neighbors if i[0] > -1 and i[1] > -1 and i[0] < chip.shape[0] and i[1] < chip.shape[1] ]

			values = []
			for k in neighbors:
				y0, x0 = k
				values = values + [chip[y0,x0]]
			data = Counter( values )
			mode = data.most_common(1)[0]
			if mode[0] == 255:
				temp[y,x] = 255

	
	return clean( temp, passes - 1, kernel_size )

def regions( chip ):

	# Binarize
	#blur = cv2.GaussianBlur(chip,(11,11),0)
	chip = cv2.cvtColor( chip, cv2.COLOR_BGR2GRAY )
 	ret3,chip = cv2.threshold(chip,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	#cv2.imwrite( "otsu.png", chip )

	chip = clean( chip, 2, int(chip.shape[0]/160) )
	#cv2.imwrite( "cleaned.png", chip )
	

	# Count Regions
	regions = np.zeros( chip.shape )	
	height, width = chip.shape

	region_counter = 0
	for y in xrange( 0, chip.shape[0] ):
		for x in xrange( 0, chip.shape[1] ):
			if regions[y,x] == 0:	

				region_counter = region_counter + 1	

				toExplore = [[y,x]]
				regions[y, x] = region_counter
				while len(toExplore) > 0:
					cur = toExplore[0]	
					val = chip[cur[0], cur[1]]
					del toExplore[0]
						
					ys = [ cur[0], cur[0]-1, cur[0]+1 ] 
					xs = [ cur[1], cur[1]-1, cur[1]+1 ] 
					neighbors = []
					for j in ys:
						for i in xs:
							if not ( i == cur[1] and j == cur[0] ):
								neighbors = neighbors + [[j,i]] 

					neighbors = [ i for i in neighbors if (i[0] > -1 and i[1] > -1 and i[0] < height and i[1] < width and regions[i[0],i[1]] == 0) ]

					for n in neighbors:
						regions[n[0],n[1]] = region_counter
					
					toExplore = toExplore + neighbors	
						
	return chip, region_counter

def build_standard_chip( wellcount, channels ):
	# Determine standard chip size from number of wells
	width = 0
	height = math.sqrt( float(wellcount) )
	if ( int(height) == height ):
		height = int(height)
		width = height
	else:	
		factors = [ (i, wellcount//i) for i in xrange(1,int(height)) if wellcount%i == 0 ]

		# Find factors with smallest difference to create more square-like chip
		smallest = [-100000,100000]
		for (a, b) in factors:
			if ( b - a ) < (smallest[1] - smallest[0]):
				smallest[0] = a
				smallest[1] = b
		width = smallest[0]
		height = smallest[1]

	size = width, height, channels
	std_array = np.zeros( size )

	print "Standard Chip Layout"
	print "Height: " + str(height) + "\nWidth: " + str(width) + "\nChannels: " + str(channels) + "\n"

	return std_array

def produce_report( filename, chip, region_count):
	a = filename.split( "/" )
	chipname = a[len(a)-1]
	
	if not os.path.exists( "results" ):
		os.makedirs( "results" )
	cv2.imwrite( "results/" + chipname, chip )

def launch( filename, wellcount ):

	chip = cv2.imread( filename, 1 )
	h, w, channels = chip.shape

	# Resize Chip to manageable size
	pixel_n = h*w	
	if pixel_n > 250000:
		chip = cv2.resize( chip, (500, 500) )

	#cv2.imwrite( "resized.png", chip )

	#std_array = build_standard_chip( wellcount, channels ) 
	#cv2.imwrite( "std_array.png", std_array );
	
	chip, region_count = regions( chip )	
	produce_report( filename, chip, region_count ) 
	print "Regions: " + str( region_count )


if __name__ == '__main__':
	start = time.time();
	if len( sys.argv ) < 3:
		print "Usage: $ python Prep.py [microwell image] [number of wells]"
		sys.exit(1)
	filename = sys.argv[1]
	wellcount = int(sys.argv[2])
	launch( filename, wellcount )
	end = time.time()

	print "Total time: " + str( end - start ) + " s"

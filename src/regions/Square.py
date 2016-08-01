import sys
import os
import math
import matplotlib.pyplot as plt
import numpy as np
import cv2
import time
import threading
from collections import Counter

def regions( chip ):


	print "Binarizing with OTSU method..." 
	# Binarize
	#blur = cv2.GaussianBlur(chip,(11,11),0)
	chip = cv2.cvtColor( chip, cv2.COLOR_BGR2GRAY )
 	ret3,chip = cv2.threshold(chip,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	#cv2.imwrite( "otsu.png", chip )

	chip_temp = chip
	print "Cleaning chip of particulates..."
	chip = cv2.medianBlur(chip_temp,11)
	#cv2.imwrite( "cleaned.png", chip )
	

	print "Getting regions..."
	# Count Regions
	regions = np.zeros( chip.shape )	
	height, width = chip.shape

	region_counter = 0
	for y in xrange( 0, chip.shape[0] ):
		for x in xrange( 0, chip.shape[1] ):
			if regions[y,x] == 0 and chip[y,x] == 255:	

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

					neighbors = [ i for i in neighbors if val == 255 ]

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

def produce_report( filename, chip_origin, chip, region_count):
	a = filename.split( "/" )
	chipname = a[len(a)-1]
	a = chipname.split( "." )
	chipname = a[0]
	
	if not os.path.exists( "results" ):
		os.makedirs( "results" )
	
	location = "results/" + chipname + ".png"

	vis = np.concatenate((chip_origin, chip), axis=1)
	cv2.imwrite( location, vis )
	
	return location

def launch( filename, wellcount ):
	start = time.time();

	print "Launching for " + filename

	chip = cv2.imread( filename, 1 )
	h, w, channels = chip.shape

	# Resize Chip to manageable size
	print "Resizing to 500x500"
	pixel_n = h*w	
	if pixel_n > 250000:
		chip = cv2.resize( chip, (500, 500) )

	#cv2.imwrite( "resized.png", chip )

	#std_array = build_standard_chip( wellcount, channels ) 
	#cv2.imwrite( "std_array.png", std_array );
	
	chip_origin = chip[:,:,1]
	chip, region_count = regions( chip )	

	build_standard_chip( 1000, 1 )

	print "Producing Report in results/ folder"
	location = produce_report( filename, chip_origin, chip, region_count ) 
	print "Regions: " + str( region_count )
	
	end = time.time()
	print "Total time: " + str( end - start ) + " s"

	print "\v"

	return wellcount, region_count, 0, location


if __name__ == '__main__':
	if len( sys.argv ) < 3:
		print "Usage: $ python Prep.py [microwell image] [number of wells]"
		sys.exit(1)

	filename = sys.argv[1]
	wellcount = int(sys.argv[2])
	launch( filename, wellcount )

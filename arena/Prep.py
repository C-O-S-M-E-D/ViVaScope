import sys
import math
import matplotlib.pyplot as plt
import numpy
import cv2
import time
import glob
from collections import deque

def launch( arg ):
	chip = cv2.imread( arg, 1 )
	height, width, channels = chip.shape()

	print "Height: " + str(height) + "\nWidth: " + str(width) + "\nChannels: " + str(channels) + "\n"
	
	pixel_n = height*width
	
	if pixel_n > 250000:
		chip = cv2.resize( chip, (500, 500) )
	
	cv2.imwrite( str( "blue_" + arg ), chip[:,:,0] )
	cv2.imwrite( str( "green_" + arg ), chip[:,:,1] )
	cv2.imwrite( str( "red_" + arg ), chip[:,:,2] )
	
	chip = cv2.cvtColor( chip, cv2.COLOR_BGR2GRAY )
	cv2.imwrite( str( "gray_" + arg ), chip )
	

if __name__ == '__main__':
	start = time.time();
	file = argv(1)
	total_counted = launch( file ); 
	end = time.time();

	print "Total time: " + str( end - start )

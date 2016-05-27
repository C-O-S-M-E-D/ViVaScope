import sys
import math
import matplotlib.pyplot as plt
import numpy
import cv2
import time
import glob
from collections import deque

class Process:

	def __init__(self):
		self.optimum=-1

	def dfs( self, m, b, r, c, region_num ):
		stack = [ [r,c] ]
		count = 0
		while len(stack) > 0:
			curr = stack.pop(-1)
			r = curr[0]
			c = curr[1]
			m[r,c] = region_num
			count += 1
			down = (r + 1) % m.shape[0]
			right = (c + 1) % m.shape[1]
			m_stack = []
			m_stack.append( [down, c] );
			m_stack.append( [down, right] );
			m_stack.append( [r, right] );
			for t in m_stack:
				if b[t[0],t[1]] == 0:
					if m[t[0],t[1]] == -1:
						stack.append( t )
		return m, count

	def fill( self, rm, fm, region_numbers ):
		for i in range(rm.shape[0]):
			for j in range( rm.shape[1] ):
				for k in region_numbers:
					if rm[i,j] == k:
						fm[i,j] = 255
		return fm

	def count( self, arg, ceil, floor, printOut, binary ):

		SIZE_CEIL=ceil
		SIZE_FLOOR=floor
		regionmap=numpy.zeros(binary.shape)
		rowMax=binary.shape[0];
		colMax=binary.shape[1];
		
		row = 0
		while (row < rowMax):
			col=0
			while (col < colMax):
				regionmap[row, col]=-1
				col+=1
			row+=1

		region_sizes=[]
		region=0
		row=0
		while(row < rowMax) :
			col=0
			while ( col < colMax ):
			
				if ( regionmap[ row, col ] != -1 ):
					col += 1
					continue

				value = binary[ row, col ]
				if ( value == 0 ):
					regionmap, size = self.dfs( regionmap, binary, row, col, region );
					region += 1
					region_sizes.append(size)
				col += 1
			row += 1

		final=0

		fill_list = []
		#print( "Determining Final Region Count -> With Bubbles" )
		row = 0
		for i in range(len(region_sizes)):
			if region_sizes[i] > SIZE_FLOOR:
				if region_sizes[i] < SIZE_CEIL:
					fill_list.append( i );
					final += 1		
		#print( final )
		final_map=None
		if( printOut ):
			final_map = numpy.zeros(regionmap.shape)
			final_map = self.fill( regionmap, final_map, fill_list )
		
		return final, regionmap, fill_list, final_map

	def remove_gaps( self, regionmap, fill_list, final ):
		print( "Eliminating wells with bubbles..." )
		
		current_region=0
		status=-1 # -1: unentered, 0: entered, 1: exited

		toeliminate=[]
		current_region = regionmap[1,1]
		for y in range(2,regionmap.shape[0]):
			for x in range(2,regionmap.shape[1]):
			
				temp = regionmap[x,y]
				if temp == -1:
					if status == 0:
						status = 1
				else:
					if temp != current_region:
						if status == -1:
							status = 0
							current_region = temp
						if status == 0:
							status = 1
						elif status == 1:
							current_region = temp
							status = 0
					else:
						if status == 1:
							toeliminate.append( temp )
							if temp in fill_list:
								fill_list.remove( temp )

		print str(len(toeliminate)) + " bubbles found."
		final_nobubbles = final - len(toeliminate)
		#print( final_nobubbles )
		final_map = numpy.zeros( regionmap.shape )
		final_map = self.fill( regionmap, final_map, fill_list )	
		return final_nobubbles, final_map


	def optimum_pixel_floor( self, arg, binary ):

		if self.optimum != -1:
			return self.optimum

		results=[]
		xlabels=[]
		summ = 0;
		print( "\nDetermining optimum floor value..." );
		for i in range(0,20):
			res, rm, fl, fi = self.count( arg, 100, i, False, binary ); 
			if (res >= 0):
				xlabels.append(i)
				summ += res
				results.append( res );
		ave = summ/len(results)
		
		squared=0.0
		for k in results:
			squared += math.pow((k-ave),2)
		
		var = squared/len(results)
		stddev = math.pow(var, 0.5)
		
		print "Max: " + str(max(results))
		print "Min: " + str(min(results))
		print "Average: " + str(ave)
		print "Variance: " + str(var)
		print "Std Dev: " + str(stddev)
		
		slope_diffs=[]
		current_slope=-1.0
		prev_slope=-1.0	
		length = len(results)
		for j in range(length-1):
			i1 = float(xlabels[j])
			i2 = float(xlabels[j+1])
			j1 = float(results[j])
			j2 = float(results[j+1])
			j_d = j2-j1	
			i_d = i2-i1
			prev_slope = current_slope
			current_slope = j_d/i_d
			if prev_slope == -1.0:
				slope_diffs.append(100000.0)
				continue	
			total_d = current_slope-prev_slope	
			slope_diffs.append(total_d)

		print( "Min Slope: " + str(min(slope_diffs)) )
		thresh = slope_diffs.index(min(slope_diffs))	
		print( "Optimal Size Threshold: " + str(thresh) )

		#plt.plot( xlabels, results )
		#plt.ylabel( 'Count' )
		#plt.xlabel( 'floor' )
		#name = "plot_" + arg
		#plt.savefig(name)
		self.optimum=thresh
		return thresh


	def otsu( self, gray ):
		colMax=gray.shape[1]
		rowMax=gray.shape[0]
		pixels=colMax*rowMax
		histogram=[0]*256
		sum_total=0

		print "Creating histogram..."
		col=0
		row=0
		while (row < rowMax):
			col=0
			while (col < colMax):
				value=gray[row, col]
				sum_total+=value
				histogram[value]+=1
				col+=1
			row+=1

		sumB=sumF=wB=wF=threshold=varMax=0

		print "Finding threshold..."
		ptr=0
		while (ptr < 256):
			
			sumB+=histogram[ptr]*ptr
			wB+=histogram[ptr]
			sumF=sum_total-sumB
			wF=pixels-wB

			if (wB == 0 or wF == 0):
				ptr+=1
				continue
			mB=sumB/wB
			mF=sumF/wF

			var=wB*wF*(( mF-mB )**2 )

			if (var > varMax):
				threshold=ptr
				varMax=var

			ptr+=1

		print "Creating binary image..."
		binary=gray
		row=0

		while (row < rowMax) :
			col=0
			while (col < colMax):
				value = gray[row, col]
				if (value < threshold):
					binary[row, col]=255
				else:
					binary[row, col]=0
				col+=1
			row+=1

		#returnIm = "bin_" + arg
		#cv2.imwrite( returnIm, binary )
		#ret, bin2 = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
		#returnIm = "bin_lib_" + arg
		#cv2.imwrite( returnIm, bin2 )

		return binary;


	def process_file( self, arg, chipsize ):
		
		start=time.time();
		print arg;

		chip=cv2.imread( arg, 1 )
		chip=cv2.resize( chip, (chipsize, chipsize) )
		gray=cv2.cvtColor( chip, cv2.COLOR_BGR2GRAY )
		binary=self.otsu(gray)

		# Run through different floors to find optimum value
		thresh_floor=self.optimum_pixel_floor( arg, binary )

		# Run final with optimum threshold
		res, rm, fl, fi = self.count( arg, 100, thresh_floor, True, binary )

		#title = str(res) +"count_bubbles_" + arg
		#cv2.imwrite( title, fi )
		res,rm=self.remove_gaps( rm, fl, res )
		title=arg+"_"+str(chipsize)+"size_"+str(res)+"count_"
		print "Seconds elapsed: "+str(time.time()-start)
		print "\n---> FINAL COUNT: "+str(res)+"\n"
		cv2.imwrite(title, rm)
		return res

		
if __name__ == '__main__':
	proc = Process()

	chipsize=50
	xlabels=[]
	results=[]
	while (chipsize <= 200):
		total_counted=0
		for file in glob.glob("*.png"):
			total_counted+=proc.process_file(file, chipsize);
		results.append(total_counted)
		xlabels.append(chipsize)
		chipsize += 25


	ave = sum(results)/len(results)
	
	squared=0.0
	for k in results:
		squared += math.pow((k-ave),2)
	
	var = squared/len(results)
	stddev = math.pow(var, 0.5)
	
	print "Max: " + str(max(results))
	print "Min: " + str(min(results))
	print "Average: " + str(ave)
	print "Variance: " + str(var)
	print "Std Dev: " + str(stddev)

	plt.plot( xlabels, results )
	plt.ylabel( 'Count' )
	plt.xlabel( 'Chip resize' )
	name = "chip_resizes"
	plt.savefig(name)

	print( "\nFINAL COUNT FOR ALL FILES: " + str( total_counted ) )
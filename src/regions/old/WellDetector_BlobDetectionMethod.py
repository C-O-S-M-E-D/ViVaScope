import cv2
import numpy as np


#Load the image
img = cv2.imread('Chip 115.tif')
img = cv2.resize( img, (200,200) )
#Resized image for sanity of the eyes
original = img
cv2.imwrite("Step_1_Original.tif", original)




#We make a mask to remove dust and noise from the image
#makeMask = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#ret, mask = cv2.threshold(makeMask,55,255,cv2.THRESH_BINARY)
#img = cv2.inpaint(img,mask,10,cv2.INPAINT_NS)
#cv2.imwrite("Step_2_Remove_Dust_Via_Impaint.tif", img)


#Run Lapacian and Blur to make sure that components close to eachother are connected
cv2.Laplacian(img, cv2.CV_64F).var()
img = cv2.morphologyEx(img,cv2.MORPH_CLOSE,(19,19))
img = cv2.medianBlur(img,7)
cv2.imwrite("Step_3_Lapacian_Trans_And_Blur.tif", img)

#Run it on the jet color map for clearer segmentation
jet_color_mapped = cv2.applyColorMap(img,cv2.COLORMAP_JET)
jet_color_mapped[:,:,0] = 0
jet_color_mapped = jet_color_mapped[:,:,1]
jet_color_mapped = cv2.GaussianBlur(jet_color_mapped,(17,17),2)
ret,thresh = cv2.threshold(jet_color_mapped, 0,255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

ret,thresh_inv = cv2.threshold(jet_color_mapped, 0,255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)



#print str(contours.size())
cv2.imwrite("Step_4_Jet_Color_Mapped_Green_Channel.tif", jet_color_mapped)

cv2.imwrite("Step_5_Threshold.tif", thresh)
cv2.waitKey(0)

#Image Processing Phase Done



###This section is for our blob detector
####################################################################
# Setting the parameters for our detector.
# Need to modify to get accuracy!!!!
params = cv2.SimpleBlobDetector_Params()
# Filter by Area. Minimum pixel size for us to count as a well.
#params.filterByArea = True
#params.minArea = 300

# Filter by Circularity. Increase in the value means increase in circularity
#params.filterByCircularity = True
#params.minCircularity = 0.0
#params.maxCircularity = 0.95

# Construct the detector
detector = cv2.SimpleBlobDetector_create(params)

# Detect blobs from the binary image
keypoints = detector.detect(thresh)

thresh_copy = thresh

#Mark on the image the wells we are sure are positive
im_with_keypoints = cv2.drawKeypoints(original, keypoints, np.array([]), (0,0, 255), \
                                      cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
# Show keypoints

#Track the number of wells we are sure of
num_of_wells_sure = len(keypoints)
print 'Number of wells we are 100% sure on: ' + (str)(len(keypoints))

#Total Area of image
totalImageArea = thresh_copy.shape[0] * thresh_copy.shape[1]

#Total black pixels before we delete
blackPixelAreaBefore = totalImageArea - cv2.countNonZero(thresh_copy)

#Draw a white circle over the wells we are sure about
for roi in keypoints:
#Note: the +1 is to make sure everything is covered since float means numbers can be off for radius
    cv2.circle(thresh_copy, (int(roi.pt[0]), int(roi.pt[1])), int((roi.size+5)/2), (255,255,255), thickness=-1, lineType=8, shift=0)

#Total black pixels after deletion
blackPixelAreaAfter = totalImageArea - cv2.countNonZero(thresh_copy)

#Calculate the potential number of wells by getting the number of black pixels removed over wells we are sure
wells_potentially_left = blackPixelAreaAfter/((blackPixelAreaBefore-blackPixelAreaAfter)/num_of_wells_sure)
print 'Number of wells we are not 100% sure on: ' + str(wells_potentially_left)
print 'Total Wells Projected: ' + str(wells_potentially_left+num_of_wells_sure)


# Show the keypoints in the image(the red circles)
cv2.imwrite("Step_6_Blobs_Detected.tif", im_with_keypoints)
cv2.imwrite("Step_7_Delete_Detected_And_Average_Rest.tif",thresh_copy)
cv2.waitKey(0)



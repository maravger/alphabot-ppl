from imutils import paths
import numpy as np
import imutils
import cv2
import math
from not_found_error import *

# initialize the known object width (cm), which in this case is the beacon
KNOWN_WIDTH = 8.5

# initialize camera-lenses real world distance (cm) from robot centre
DIST_FROM_CENTRE = 7

PIC_CENTRE_WIDTH = 1296 # x-centre-coordinate of the 2596x1944 resolution picture
FOCAL_LENGTH = 4305

# define the list of boundaries (red, blue, purple, yellow, orange)
# IMPORTANT: colour boundaries should be BGR
COLOR_BOUNDARIES = [
    [([70, 60, 200], [150, 110, 250])], 
    [([160, 130, 0], [210, 180, 60])], 
    [([95, 80, 95], [130, 110 , 120])], 
    [([100, 220, 230], [170, 250, 250])], 
    [([70, 100, 190], [145, 140, 240])], 
]

class Dna(object):
    def detect_color(self, image):
	color = 0
	curr_width = 0	
	# loop over the boundaries, find the most fitting color 
	for boundaries in COLOR_BOUNDARIES:
		print("")
    		if (color == 0):
        		print("Looking for the Red Beacon...")
    		elif (color == 1):
        		print("Looking for the Blue Beacon...")
    		elif (color == 2):
        		print("Looking for the Purple Beacon...")
    		elif (color == 3):
        		print("Looking for the Yellow Beacon...")
    		else:
        		print("Looking for the Orange Beacon...")		
    		for (lower, upper) in boundaries:
			# create NumPy arrays from the boundaries
        		lower = np.array(lower, dtype = "uint8")
        		upper = np.array(upper, dtype = "uint8") 
        		# find the colors within the specified boundaries and apply
        		# the mask
        		mask = cv2.inRange(image, lower, upper)
        		mask_lists = mask.tolist()                       
 
                        try:
				# find contour based on colour
        		    	cnts = cv2.findContours(mask.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        		    	cnts = imutils.grab_contours(cnts)
        		    	c = max(cnts, key = cv2.contourArea)
			    	marker = cv2.minAreaRect(c)

			    	# Always looking for cylinders sitting on their bottom
            		    	if (marker[1][0] < marker[1][1]): 
                	    		width = marker[1][0]
                			height = marker[1][1]
                			angle = marker[2]
            			else:
                			# Cannot be sitting on their side
                			raise ValueError
            			print("Candidate contour width, height and angle:")
            			print width,height,angle
            
            			# Check if feasible beacon marker
            			# 1: width to height ratio must be within the range of [0.37, 0.43]
            			if not((width/height >= 0.37) and (width/height <= 0.43)):
                			raise ValueError
            			# 2: angle must be within the range of [-5, 5]
            			elif not(angle >= -5 and angle <= 5):
                			raise ValueError 
			
                        except ValueError:
				print('Not found!')
            			continue	
			if (width > curr_width):
            			curr_color = color
            			curr_width = width
				curr_cnt = c			

    		color += 1

	if not(curr_width == 0):
    		cms = self.find_distance(KNOWN_WIDTH, FOCAL_LENGTH, curr_width, DIST_FROM_CENTRE)
	else:
    		print "\nNo Beacon detected!"
                raise NotFoundError
    		exit()

	print("Calculated Distance: %.2f cm" % cms)

	if (curr_color == 0):
    		print("Red Beacon identified!")
	elif (curr_color == 1):
    		print("Blue Beacon identified!")
	elif (curr_color == 2):
    		print("Purple Beacon identified!")
	elif (curr_color == 3):
    		print("Yellow Beacon identified!")
	else:
    		print("Orange Beacon identified!")	
        
        return curr_cnt

    def find_marker(self, image):
        # detect the beacon color and the respective contour based on it
        c = self.detect_color(image)   
        
        # compute the bounding box of the of the color region and return it 
        return (cv2.minAreaRect(c), c)

    def find_angle(self, cnt, distance):
        # Find left extreme point
        leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])
        # Find right extreme point
        rightmost = tuple(cnt[cnt[:,:,0].argmax()][0])
        # Calculate centre of contour
        beac_centre = (rightmost[0] + leftmost[0])/2
        beac_pixel_width = rightmost[0] - leftmost[0]
        beac_real_width = KNOWN_WIDTH # cm

        cm_per_pixel = float(beac_real_width) / beac_pixel_width
        beac_pixel_dst_centre = beac_centre - PIC_CENTRE_WIDTH
        beac_real_dst_centre = cm_per_pixel * beac_pixel_dst_centre

        a = float(beac_real_dst_centre)
        b = float(distance)
        c = a / b
        angle = math.asin(c)
        return angle

    def find_distance(self, knownWidth, focalLength, perWidth, distFromCentre):
        # compute and return the distance from the maker to the camera
        return ((knownWidth * focalLength) / perWidth) + distFromCentre

    def find_distance_and_angle(self, imagePath):
        print("Checking image: " + imagePath)
        # load the image, find the marker in the image, then compute the
        # distance to the marker from the camera
        image = cv2.imread(imagePath)
        marker, contour = self.find_marker(image)
        cms = self.find_distance(KNOWN_WIDTH, FOCAL_LENGTH, marker[1][0], DIST_FROM_CENTRE)
        angle = self.find_angle(contour, cms)
        print("Calculated Distance: %.2f cm" % cms)
        print("Calculated Angle: %.2f Deg" % math.degrees(angle))

        return cms, math.degrees(angle)

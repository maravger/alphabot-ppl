from imutils import paths
import numpy as np
import imutils
import cv2
import math

# initialize the known object width (cm), which in this case is the beacon
KNOWN_WIDTH = 9.5

# initialize camera-lenses real world distance (cm) from robot centre
DIST_FROM_CENTRE = 7

PIC_CENTRE_WIDTH = 1296 # x-centre-coordinate of the 2596x1944 resolution picture
FOCAL_LENGTH = 4305

# define the list of boundaries (red, blue)
# IMPORTANT: colour boundaries should be BGR
COLOR_BOUNDARIES = [
    [([60, 30, 150], [100, 80, 210])], [([150, 130, 20], [255, 230, 150])]
]

class Dna(object):
    def detect_color(self, image):
        # 0 = pink, 1 = green 
        color = 0
        prev_pixels = 0

	# loop over the boundaries, find the most fitting color 
	for boundaries in COLOR_BOUNDARIES:
    		for (lower, upper) in boundaries:
        		# create NumPy arrays from the boundaries
        		lower = np.array(lower, dtype = "uint8")
        		upper = np.array(upper, dtype = "uint8") 
        		# find the colors within the specified boundaries and apply
        		# the mask
        		mask = cv2.inRange(image, lower, upper)
        		mask_lists = mask.tolist()
        		pixels = sum(x > 0 for lis in mask_lists for x in lis)
                        
                        try:
        		    # find contour based on colour
        		    cnts = cv2.findContours(mask.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        		    cnts = imutils.grab_contours(cnts)
        		    c = max(cnts, key = cv2.contourArea) 
			
        		    if (pixels >= prev_pixels):
            			curr_color = color
                                curr_cnt = c
                        except ValueError:
                            print('0 pixels of this colour found!')

    		color += 1
    		prev_pixels = pixels

	if (curr_color == 0):
    		print("Red Beacon identified!")
	else:
    		print("Blue Beacon identified!")
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

from imutils import paths
import numpy as np
import imutils
import cv2
import math

# initialize the known object width, which in this case is the beacon
KNOWN_WIDTH = 12

PIC_CENTRE_WIDTH = 1296 # x-centre-coordinate of the 2596x1944 resolution picture
FOCALLENGTH = 4700

class Dna(object):
    def find_marker(self, image):
        # convert the image to grayscale, blur it, and detect edges
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret,gray = cv2.threshold(gray,190,255,0)

        # find the contours in the edged image and keep the largest one;
        # we'll assume that this is our piece of paper in the image
        cnts = cv2.findContours(gray.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        c = max(cnts, key = cv2.contourArea)

        # compute the bounding box of the of the paper region and return it
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

    def find_distance(self, knownWidth, focalLength, perWidth):
        # compute and return the distance from the maker to the camera
        return (knownWidth * focalLength) / perWidth

    def find_distance_and_angle(self, imagePath):
        print("Checking image: " + imagePath)
        # load the image, find the marker in the image, then compute the
        # distance to the marker from the camera
        image = cv2.imread(imagePath)
        marker, contour = self.find_marker(image)
        cms = self.find_distance(KNOWN_WIDTH, FOCALLENGTH, marker[1][0])
        angle = self.find_angle(contour, cms)
        print("Calculated Distance: %.2f cm" % cms)
        print("Calculated Angle: %.2f Deg" % math.degrees(angle))

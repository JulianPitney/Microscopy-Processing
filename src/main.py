import cv2
import numpy as np
import tifffile
import math
import matplotlib
from matplotlib import pyplot as plt


original = tifffile.imread("../data/d1.tif")
stack = tifffile.imread("../data/d1.tif")



def display_stack(stack, auto):

    cv2.namedWindow('stack', cv2.WINDOW_NORMAL)

    for slice in stack:

        cv2.imshow('stack', slice)

        if auto:
            cv2.waitKey(1)
        else:
            cv2.waitKey(0)

def compare_stacks(original, processed, auto):

    cv2.namedWindow('original', cv2.WINDOW_NORMAL)
    cv2.namedWindow('processed', cv2.WINDOW_NORMAL)

    for slice1, slice2 in zip(original, processed):
        cv2.imshow('original', slice1)
        cv2.imshow('processed', slice2)

        if auto:
            cv2.waitKey(1)
        else:
            cv2.waitKey(0)


def max_project(stack):

    stackMax = np.max(stack, axis=0)
    return stackMax

def min_project(stack):

    stackMin = np.min(stack, axis=0)
    return stackMin




def save_stack(stack):

    for z in range(0, len(stack)):
        cv2.imwrite(str(z) + ".png", stack[z])


# In-place binary thresholding of a stack.
# Note: Threshold should be obtained from histogram info
# (either manual inspection or automatic)
def remove_all_pixels_below_threshold(stack, threshold):

    print("remove_all_pixels_below_threshold(): Starting...")

    for z in range(0, len(stack)):
        ret, thresholded_slice = cv2.threshold(stack[z], threshold, 255, cv2.THRESH_TOZERO)
        stack[z] = thresholded_slice

    print("remove_all_pixels_below_threshold(): Completed!")

def remove_all_pixels_above_threshold(stack, threshold):

    print("remove_all_pixels_above_threshold(): Starting...")

    for z in range(0, len(stack)):
        ret, thresholded_slice = cv2.threshold((stack[z]), threshold, 255, cv2.THRESH_TOZERO_INV)
        stack[z] = thresholded_slice

    print("remove_all_pixels_above_threshold(): Completed!")

def kernel_filter_2d(stack, kernelDims):

    print("kernel_filter_2d(): Starting...")

    kernel = np.ones(kernelDims, np.float32) / (kernelDims[0] * kernelDims[1])

    for z in range(0, len(stack)):

        stack[z] = cv2.filter2D(stack[z], -1, kernel)

    print("kernel_filter_2d(): Completed!")

def map_actual_range_to_max_range(val):

    leftMin = 0
    leftMax = 40
    leftRange = leftMax - leftMin
    rightMin = 0
    rightMax = 255
    rightRange = rightMax - rightMin

    if val > leftMax:
        val = leftMax

    scaled = float(val - leftMin) / float(leftRange)
    return math.floor(rightMin + (scaled * rightRange))



def gen_signal_density_map_3d(stack, kernelSize_zyx):

    print("gen_signal_density_map_3d(): Starting...")

    zLen = stack.shape[0]
    yLen = stack.shape[1]
    xLen = stack.shape[2]

    zBlocks = math.ceil(zLen / kernelSize_zyx[0])
    zPixelsRemainder = zLen % kernelSize_zyx[0]
    zPadding = kernelSize_zyx[0] - zPixelsRemainder

    yBlocks = math.ceil(yLen / kernelSize_zyx[1])
    yPixelsRemainder = yLen % kernelSize_zyx[1]
    yPadding = kernelSize_zyx[1] - yPixelsRemainder

    xBlocks = math.ceil(xLen / kernelSize_zyx[2])
    xPixelsRemainder = xLen % kernelSize_zyx[2]
    xPadding = kernelSize_zyx[2] - xPixelsRemainder

    zBounds = [0, kernelSize_zyx[0]]
    yBounds = [0, kernelSize_zyx[1]]
    xBounds = [0, kernelSize_zyx[2]]


    for z in range(0, zBlocks):


        for y in range(0, yBlocks):

            for x in range(0, xBlocks):

                totalSignal = 0
                totalVolume = 0
                for slice in stack[zBounds[0]:zBounds[1], yBounds[0]:yBounds[1], xBounds[0]:xBounds[1]]:

                    totalSignal += (slice > 0).sum()
                    totalVolume += slice.size

                density = totalSignal / totalVolume
                stack[zBounds[0]:zBounds[1], yBounds[0]:yBounds[1], xBounds[0]:xBounds[1]] = map_actual_range_to_max_range(int(density*255))

                xBounds[0] += kernelSize_zyx[2]
                xBounds[1] += kernelSize_zyx[2]
                if xPixelsRemainder != 0 and x == xBlocks - 1:
                    # TODO: Implement boundary detection case
                    break

            xBounds = [0, kernelSize_zyx[2]]
            yBounds[0] += kernelSize_zyx[1]
            yBounds[1] += kernelSize_zyx[1]
            if yPixelsRemainder != 0 and y == yBlocks - 1:
                # TODO: Implement boundary detection case
                break

        yBounds = [0, kernelSize_zyx[1]]
        zBounds[0] += kernelSize_zyx[0]
        zBounds[1] += kernelSize_zyx[0]
        if zPixelsRemainder != 0 and z == zBlocks - 1:
            #TODO: Implement boundary detection case
            break

    print("gen_signal_density_map_3d(): Completed!")

def convert_grayscale_stack_to_color(stack):

    color_stack = np.stack((stack,)*3, axis=-1)
    return color_stack


def color_map(stackGray, stackColor):


    for z in range(0, len(stackGray)):

        stackColor[z] = cv2.applyColorMap(stackGray[z], 2)




# Method 1:
# This method still needs out of bounds detection implemented
# for spaceball placement within the scan.
def draw_spaceball(stack, centerXYZ, radius):

    centerZ = centerXYZ[2]
    centerY = centerXYZ[1]
    centerX = centerXYZ[0]

    currentRadius = radius

    for z in range(centerZ, centerZ + radius):
        cv2.circle(stack[z], (centerX, centerY), currentRadius, (255, 0, 0), 2)
        currentRadius -= 1

    currentRadius = radius

    for z in range(centerZ, centerZ - radius, -1):
        cv2.circle(stack[z], (centerX, centerY), currentRadius, (255, 0, 0), 2)
        currentRadius -= 1

# Method 2:
# This should cut out a square for each circle/slice from method above.
# Each square should be packaged into an object that contains the coordinates
# of each pixel in this square from the perspective of the original slice.
def cut_out_square_sections_around_each_circle():
    pass

# Method 3:
# This method should take one of the square slice objects
# generated by the method above and detect all the individual islands
# on that slice. The islands should be packaged into island objects
# that contain the coordinates of every pixel in that island relative
# to the original slice. These island objects should have a state variable
# that can take on 1 of 4 values:
#
# 1. Unchecked/Just created (default)
# 2. In-Progress (Start slice found and currently being checked for termination)
# 3. Thrown Out (Determined not to intersect with sphere surface)
# 4. Counted (Overlap confirmed and termination confirmed)
def detect_islands_on_slice(squareSlice):
    pass

# Method 4:
# This method should check all the in-progress blobs and all the blobs
# on the current slice and take appropriate action based on the state of the blob
# object (Unchecked, In-Progress, Thrown Out, Counted). When scanning a new square slice,
# All the in progress blobs should be checked first. Once they're all taken care of, all the remaining
# blobs on the square slice should be checked. (See algorithm pdf for handle_islands() pseudocode).
def handle_islands(squareSlice):
    pass

# Method 5:
# This method should take the total number of "Counted" blobs and feed that into the spaceballs algorithm.
def calculate_length_density():
    pass

# Method 6:
# This method should implement systematic random sampling of the
# scan and perform methods 1-5 for each sample.
# The results of each sample should be stored.
def systematic_random_spaceball_sample():
    pass


remove_all_pixels_below_threshold(stack, 24)
kernel_filter_2d(stack, (3, 3))
colorStack = convert_grayscale_stack_to_color(stack)
draw_spaceball(colorStack, (1300, 500, 200), 100)
display_stack(colorStack, 0)
exit()



#plt.hist(stack.ravel(), 256, [0, 256])
remove_all_pixels_below_threshold(stack, 24)
kernel_filter_2d(stack, (3, 3))
gen_signal_density_map_3d(stack, (5, 10, 10))
maxProjection = max_project(stack)
maxProjection = cv2.GaussianBlur(maxProjection, (101, 101), 0)
maxProjectionColor = convert_grayscale_stack_to_color(maxProjection)
maxProjectionColorMapped = cv2.applyColorMap(maxProjectionColor, 2)
cv2.imwrite('density_map.png', maxProjectionColorMapped)



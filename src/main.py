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

def convert_density_map_to_color(stack):

    color_stack = np.stack((stack,)*3, axis=-1)
    return color_stack


def color_map(stackGray, stackColor):


    for z in range(0, len(stackGray)):

        stackColor[z] = cv2.applyColorMap(stackGray[z], 2)















#plt.hist(stack.ravel(), 256, [0, 256])
remove_all_pixels_below_threshold(stack, 24)
kernel_filter_2d(stack, (3, 3))
gen_signal_density_map_3d(stack, (5, 10, 10))
maxProjection = max_project(stack)

maxProjection = cv2.GaussianBlur(maxProjection, (101, 101), 0)
maxProjectionColor = convert_density_map_to_color(maxProjection)
maxProjectionColorMapped = cv2.applyColorMap(maxProjectionColor, 2)
cv2.namedWindow('test', cv2.WINDOW_NORMAL)
cv2.imshow('test', maxProjectionColorMapped)
cv2.waitKey(0)
cv2.imwrite('density_map.png', maxProjectionColorMapped)



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

    cv2.namedWindow('Max Projection', cv2.WINDOW_NORMAL)
    stackMax = np.max(stack, axis=0)
    cv2.imshow('Max Projection', stackMax)
    cv2.waitKey(0)


def save_stack(stack):

    for z in range(0, len(stack)):
        cv2.imwrite(str(z) + ".png", stack[z])


# In-place binary thresholding of a stack.
# Note: Threshold should be obtained from histogram info
# (either manual inspection or automatic)
def remove_all_pixels_below_threshold(stack, threshold):

    for z in range(0, len(stack)):
        ret, thresholded_slice = cv2.threshold(stack[z], threshold, 255, cv2.THRESH_TOZERO)
        stack[z] = thresholded_slice

def remove_all_pixels_above_threshold(stack, threshold):

    for z in range(0, len(stack)):
        ret, thresholded_slice = cv2.threshold((stack[z]), threshold, 255, cv2.THRESH_TOZERO_INV)
        stack[z] = thresholded_slice



def kernel_filter_2d(stack, kernelDims):

    kernel = np.ones(kernelDims, np.float32) / (kernelDims[0] * kernelDims[1])

    for z in range(0, len(stack)):

        stack[z] = cv2.filter2D(stack[z], -1, kernel)




def gen_signal_density_map_3d(stack, kernelSize_zyx):

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
                stack[zBounds[0]:zBounds[1], yBounds[0]:yBounds[1], xBounds[0]:xBounds[1]] = int(density*255)



                xBounds[0] += kernelSize_zyx[2]
                xBounds[1] += kernelSize_zyx[2]
                if xPixelsRemainder != 0 and x == xBlocks - 1:
                    print("X BOUNDARY DETECTED")
                    break

            xBounds = [0, kernelSize_zyx[2]]
            yBounds[0] += kernelSize_zyx[1]
            yBounds[1] += kernelSize_zyx[1]
            if yPixelsRemainder != 0 and y == yBlocks - 1:
                print("Y BOUNDARY DETECTED")
                break

        yBounds = [0, kernelSize_zyx[1]]
        zBounds[0] += kernelSize_zyx[0]
        zBounds[1] += kernelSize_zyx[0]
        if zPixelsRemainder != 0 and z == zBlocks - 1:
            print("Z BOUNDARY DETECTED")
            break


def convert_density_map_to_color(stack):

    color_stack = np.stack((stack,)*3, axis=-1)
    color_stack[:, :, :, 0:2] = 0

    return color_stack

plt.hist(stack.ravel(), 256, [0, 256])
remove_all_pixels_below_threshold(stack, 24)
kernel_filter_2d(stack, (2, 2))
gen_signal_density_map_3d(stack, (10, 30, 30))
color_stack = convert_density_map_to_color(stack)
#max_project(color_stack)
save_stack(color_stack)





import cv2
import numpy as np
import tifffile
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

# In-place binary thresholding of a stack.
# Note: Threshold should be obtained from histogram info
# (either manual inspection or automatic)
def threshold(stack, threshold):

    for z in range(0, len(stack)):
        ret, thresholded_slice = cv2.threshold(stack[z], threshold, 255, cv2.THRESH_TOZERO)
        stack[z] = thresholded_slice




def kernel_filter_2d(stack, kernelDims):

    kernel = np.ones(kernelDims, np.float32) / (kernelDims[0] * kernelDims[1])

    for z in range(0, len(stack)):

        stack[z] = cv2.filter2D(stack[z], -1, kernel)







# Process
#plt.hist(stack.ravel(), 256, [0, 256])
threshold(stack, 24)
kernel_filter_2d(stack, (2, 2))




# Compare before and after
cv2.namedWindow('Max Projection Orig', cv2.WINDOW_NORMAL)
cv2.namedWindow('Max Projection Proc', cv2.WINDOW_NORMAL)
origMax = np.max(original, axis=0)
procMax = np.max(stack, axis=0)
cv2.imshow('Max Projection Orig', origMax)
cv2.imshow('Max Projection Proc', procMax)
cv2.imwrite('orig.png', origMax)
cv2.imwrite('proc.png', procMax)
cv2.waitKey(0)





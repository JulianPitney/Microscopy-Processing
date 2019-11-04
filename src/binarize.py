import sys
import numpy as np
import tifffile
import cv2



if len(sys.argv) != 4:
    print("Invalid number of arguments, try again.")
    print("USAGE: binarize.py <stack_path> <threshold> <save_flag>")
    exit(0)


stackPath = sys.argv[1]
thresholdMin = int(sys.argv[2])
saveFlag = int(sys.argv[3])

if not isinstance(stackPath, str):
    print("stackPath argument is not a valid string, try again.")
    print("USAGE: binarize.py <stack_path> <threshold> <save_flag>")
    exit(0)
if not isinstance(thresholdMin, int):
    print("thresholdMin argument is not a valid integer, try again.")
    print("USAGE: binarize.py <stack_path> <threshold> <save_flag>")
    exit(0)
if not isinstance(saveFlag, int) or (saveFlag != 0 and saveFlag != 1):
    print("save_flag argument is not a valid value, try again.")
    print("USAGE: binarize.py <stack_path> <threshold> <save_flag>")
    exit(0)


stack = tifffile.imread(stackPath)


def max_project(stack):
    stackMax = np.max(stack, axis=0)
    return stackMax

def display_stack(stack, auto):
    cv2.namedWindow('stack', cv2.WINDOW_NORMAL)
    for slice in stack:
        cv2.imshow('stack', slice)
        if auto:
            cv2.waitKey(1)
        else:
            cv2.waitKey(0)

def displaySlice(slice):
    cv2.namedWindow('slice', cv2.WINDOW_NORMAL)
    cv2.imshow('slice', slice)
    cv2.waitKey(0)

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

def kernel_filter_2d(stack, kernelDims):
    print("kernel_filter_2d(): Starting...")
    kernel = np.ones(kernelDims, np.float32) / (kernelDims[0] * kernelDims[1])
    for z in range(0, len(stack)):
        stack[z] = cv2.filter2D(stack[z], -1, kernel)
    print("kernel_filter_2d(): Completed!")

def binarize(stack):
    stack[stack > 0] = 255


remove_all_pixels_below_threshold(stack, thresholdMin)
kernel_filter_2d(stack, (3, 3))
binarize(stack)
maxProjection = max_project(stack)
displaySlice(maxProjection)
if saveFlag:
    save_stack(stack)


import cv2
import numpy as np


def display_stack(stack, auto):

    cv2.namedWindow('stack', cv2.WINDOW_NORMAL)

    for slice in stack:

        cv2.imshow('stack', slice)

        if auto:
            cv2.waitKey(1)
        else:
            cv2.waitKey(0)



def max_project(stack):

    stackMax = np.max(stack, axis=0)
    return stackMax


def save_stack(stack):

    for z in range(0, len(stack)):
        cv2.imwrite(str(z) + ".png", stack[z])




def convert_grayscale_stack_to_color(stack):

    color_stack = np.stack((stack,)*3, axis=-1)
    return color_stack

def color_map(stackGray, stackColor):

    for z in range(0, len(stackGray)):
        stackColor[z] = cv2.applyColorMap(stackGray[z], 2)



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
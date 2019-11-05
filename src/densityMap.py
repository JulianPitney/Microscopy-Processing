import cv2
import tifffile
import math
import matplotlib
from matplotlib import pyplot as plt
import zstackUtils as zsu


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
                    print("Warning: gen_signal_density_map_3d() has detected overflow in the X direction! The last column in X will be skipped.")
                    break

            xBounds = [0, kernelSize_zyx[2]]
            yBounds[0] += kernelSize_zyx[1]
            yBounds[1] += kernelSize_zyx[1]
            if yPixelsRemainder != 0 and y == yBlocks - 1:
                print("Warning: gen_signal_density_map_3d() has detected overflow in the Y direction! The last row in Y will be skipped.")
                break

        yBounds = [0, kernelSize_zyx[1]]
        zBounds[0] += kernelSize_zyx[0]
        zBounds[1] += kernelSize_zyx[0]
        if zPixelsRemainder != 0 and z == zBlocks - 1:
            print("Warning: gen_signal_density_map_3d() has detected overflow in the Z direction! The last block in Z will be skipped.")
            break

    print("gen_signal_density_map_3d(): Completed!")



original = tifffile.imread("../data/d1.tif")
stack = tifffile.imread("../data/d1.tif")
plt.hist(stack.ravel(), 256, [0, 256])
zsu.remove_all_pixels_below_threshold(stack, 24)
zsu.kernel_filter_2d(stack, (3, 3))
gen_signal_density_map_3d(stack, (5, 10, 10))
maxProjection = zsu.max_project(stack)
maxProjection = cv2.GaussianBlur(maxProjection, (101, 101), 0)
maxProjectionColor = zsu.convert_grayscale_stack_to_color(maxProjection)
maxProjectionColorMapped = cv2.applyColorMap(maxProjectionColor, 2)
cv2.imwrite('density_map.png', maxProjectionColorMapped)
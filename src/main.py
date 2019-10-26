import cv2
import numpy as np
import tifffile
import math
import matplotlib
from matplotlib import pyplot as plt



original = tifffile.imread("../data/d1.tif")
stack = tifffile.imread("../data/d1.tif")


class Island(object):

    def __init__(self, coords):

        self.coords = coords
        self.state = "New"


class SpaceballSlice(object):

    def __init__(self, originalSlice, boundingCoords, circleCenter, circleRadius):
        self.originalSlice = originalSlice
        self.boundingCoords = boundingCoords
        self.circleCenter = circleCenter
        self.circleRadius = circleRadius
        self.islands = []











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
# This method generates a stack of images with accompanying bounding
# boxes for the circle that represents the 2D portion of the spaceball
# for that slice. All coordinates are from the perspective of the original
# stack.
# TODO: This method still needs out of bounds detection to handle spaceballs
# TODO: being requested outside the bounds of a scan.
def gen_spaceball(stack, centerXYZ, radius):

    print("gen_spaceball(): Starting...")


    centerZ = centerXYZ[2]
    centerY = centerXYZ[1]
    centerX = centerXYZ[0]
    currentRadius = radius
    spaceballSlices = [None] * (radius * 2)
    ind1 = radius
    ind2 = radius - 1

    for z in range(centerZ, centerZ + radius):

        currentRadius -= 1
        x0 = centerX - currentRadius
        y0 = centerY - currentRadius
        x1 = centerX + currentRadius
        y1 = centerY + currentRadius

        spaceBallSlice1 = SpaceballSlice(stack[z], (x0, y0, x1, y1), (centerX, centerY), currentRadius)
        spaceBallSlice2 = SpaceballSlice(stack[centerZ - (z - centerZ)], (x0, y0, x1, y1), (centerX, centerY), currentRadius)
        spaceballSlices[ind1] = spaceBallSlice1
        spaceballSlices[ind2] = spaceBallSlice2
        ind1 += 1
        ind2 -= 1

    print("gen_spaceball(): Completed!")
    return spaceballSlices

# Method 2:
# This method should take one of the square slice objects
# generated by the method above and detect all the individual islands
# inside the spaceball circle for that slice. The islands should be packaged into island objects
# that contain the coordinates of every pixel in that island relative
# to the original slice. These island objects should have a state variable
# that can take on 1 of 4 values:
#
# 1. Unchecked/Just created (default)
# 2. In-Progress (Start slice found and currently being checked for termination)
# 3. Thrown Out (Determined not to intersect with sphere surface)
# 4. Counted (Overlap confirmed and termination confirmed)
def detect_islands_on_spaceball_slices(spaceball):

    print("detect_islands_on_spaceball_slices(): Starting...")


    for z in range(0, len(spaceball)):

        print("Detecting Islands on Slice# " + str(z))
        slice = spaceball[z].originalSlice.copy()
        circleCenter = spaceball[z].circleCenter
        circleRadius = spaceball[z].circleRadius
        tempColor = convert_grayscale_stack_to_color(slice)
        circleOverlay = cv2.circle(tempColor, circleCenter, circleRadius, (255, 0, 0), -1)
        circleIndexMask = np.where(circleOverlay[:, :, 0] == 255)

        # The valid coordinates are all the coordinates inside the circle.
        validCoords = []
        for coord in range(0, len(circleIndexMask[0])):
            y = circleIndexMask[0][coord]
            x = circleIndexMask[1][coord]
            validCoords.append((y, x))


        if z == 0 or z == len(spaceball) - 1:
            continue

        x0 = spaceball[z].boundingCoords[0]
        y0 = spaceball[z].boundingCoords[1]
        x1 = spaceball[z].boundingCoords[2]
        y1 = spaceball[z].boundingCoords[3]

        spaceball[z].islands = num_islands(slice, x0, x1, y0, y1, validCoords)

    print("detect_islands_on_spaceball_slices(): Completed!")

def num_islands(graph, x0, x1, y0, y1, validCoords):

    row = y1 - y0
    col = x1 - x0
    islands = []

    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if graph[y][x] > 0 and (y, x) in validCoords:

                islandPixelCoords = []
                dfs(graph, row, col, y, x, islandPixelCoords, validCoords)
                newIsland = Island(islandPixelCoords)
                islands.append(newIsland)

    return islands

def dfs(graph, row, col, y, x, isLandPixelCoords, validCoords):

    if graph[y][x] == 0:
        return
    else:
        if (y, x) in validCoords:
            isLandPixelCoords.append((y, x))
        graph[y][x] = 0

    if y != 0:
        dfs(graph, row, col, y - 1, x, isLandPixelCoords, validCoords)

    if y != row - 1:
        dfs(graph, row, col, y + 1, x, isLandPixelCoords, validCoords)

    if x != 0:
        dfs(graph, row, col, y, x - 1, isLandPixelCoords, validCoords)

    if x != col - 1:
        dfs(graph, row, col, y, x + 1, isLandPixelCoords, validCoords)







    # Method 3:


# This method should check all the in-progress blobs and all the blobs
# on the current slice and take appropriate action based on the state of the blob
# object (Unchecked, In-Progress, Thrown Out, Counted). When scanning a new square slice,
# All the in progress blobs should be checked first. Once they're all taken care of, all the remaining
# blobs on the square slice should be checked. (See algorithm pdf for handle_islands() pseudocode).
# TODO: Thought of a 4th state machine case for blobs -> What if blob intersects sphere twice (goes in
# TODO: and then goes back out). Need case to handle this.
def handle_islands(squareSlice):
    pass

# Method 4:
# This method should take the total number of "Counted" blobs and feed that into the spaceballs algorithm.
def calculate_length_density():
    pass

# Method 5:
# This method should implement systematic random sampling of the
# scan and perform methods 1-5 for each sample.
# The results of each sample should be stored.
def systematic_random_spaceball_sample():
    pass


remove_all_pixels_below_threshold(stack, 24)
kernel_filter_2d(stack, (3, 3))
spaceball = gen_spaceball(stack, (1300, 500, 200), 100)
detect_islands_on_spaceball_slices(spaceball)



# BLOCK BELOW DISPLAYS ISLAND DETECTION VISUALLY
"""
cv2.namedWindow('test', cv2.WINDOW_NORMAL)
num = 0
for slice in spaceball:
    print("NEW SLICE")
    x0 = slice.boundingCoords[0]
    y0 = slice.boundingCoords[1]
    x1 = slice.boundingCoords[2]
    y1 = slice.boundingCoords[3]
    currentRadius = 1300 - x0

    colorSlice = convert_grayscale_stack_to_color(slice.originalSlice)
    circleOverlay = cv2.circle(colorSlice, (1300, 500), currentRadius, (255, 0, 0), -1)

    for island in slice.islands:
        for pixel in island.coords:
            circleOverlay[pixel[0]][pixel[1]][2] = 255
    if num == 0 or num == 199:
        num += 1
        continue
    num += 1
    cv2.imshow('test', circleOverlay[y0:y1, x0:x1])
    cv2.waitKey(0)
exit()
"""


#plt.hist(stack.ravel(), 256, [0, 256])
remove_all_pixels_below_threshold(stack, 24)
kernel_filter_2d(stack, (3, 3))
gen_signal_density_map_3d(stack, (5, 10, 10))
maxProjection = max_project(stack)
maxProjection = cv2.GaussianBlur(maxProjection, (101, 101), 0)
maxProjectionColor = convert_grayscale_stack_to_color(maxProjection)
maxProjectionColorMapped = cv2.applyColorMap(maxProjectionColor, 2)
cv2.imwrite('density_map.png', maxProjectionColorMapped)



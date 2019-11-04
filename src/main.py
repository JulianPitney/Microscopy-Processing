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



def max_project(stack):

    stackMax = np.max(stack, axis=0)
    return stackMax


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


    zLen = len(stack)
    yLen = len(stack[0])
    xLen = len(stack[0][0])
    centerZ = centerXYZ[2]
    centerY = centerXYZ[1]
    centerX = centerXYZ[0]
    currentRadius = radius
    spaceballSlices = [None] * (radius * 2)
    ind1 = radius
    ind2 = radius - 1


    # Check if spaceball is inside bounds of scan.
    if (centerZ + radius) > zLen or (centerZ - radius) < 0:
        print("Warning: Requested spaceball falls off the edge of the scan in Z. Aborting!")
        return 0
    elif (centerY + radius) > yLen or (centerY - radius) < 0:
        print("Warning: Requested spaceball falls off the edge of the scan in Y. Aborting!")
        return 0
    elif (centerX + radius) > xLen or (centerX - radius) < 0:
        print("Warning: Requested spaceball falls off the edge of the scan in X. Aborting!")
        return 0



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
# to the original slice.
def detect_islands_on_spaceball_slices(spaceball):

    print("detect_islands_on_spaceball_slices(): Starting...")


    for z in range(0, len(spaceball)):

        print("Detecting Islands on Slice# " + str(z))
        slice = spaceball[z].originalSlice.copy()
        circleCenter = spaceball[z].circleCenter
        circleRadius = spaceball[z].circleRadius
        tempColor = convert_grayscale_stack_to_color(slice)
        circleOverlay = cv2.circle(tempColor, circleCenter, circleRadius, (255, 0, 0), 2)
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

                if len(islandPixelCoords) > 25:
                    newIsland = Island(islandPixelCoords)
                    islands.append(newIsland)

    return islands

def dfs(graph, row, col, y, x, isLandPixelCoords, validCoords):

    if graph[y][x] == 0:
        return
    else:
        if (y, x) in validCoords:
            isLandPixelCoords.append([y, x])
            graph[y][x] = 0
        else:
            graph[y][x] = 0
            return


    if y != 0:
        dfs(graph, row, col, y - 1, x, isLandPixelCoords, validCoords)

    if y != row - 1:
        dfs(graph, row, col, y + 1, x, isLandPixelCoords, validCoords)

    if x != 0:
        dfs(graph, row, col, y, x - 1, isLandPixelCoords, validCoords)

    if x != col - 1:
        dfs(graph, row, col, y, x + 1, isLandPixelCoords, validCoords)





# Method 3:
# This method should ....?
def count_unique_spaceball_intersections(spaceball):

    print("count_unique_spaceball_intersections(): Starting...")
    numIntersections = 0

    for z in range(1, len(spaceball)):

        # TODO: Temp for visualization
        cv2.namedWindow('labeled', cv2.WINDOW_NORMAL)
        cv2.namedWindow('original', cv2.WINDOW_NORMAL)
        islandsTop = spaceball[z - 1].islands
        islandsBottom = spaceball[z].islands
        sliceTop = spaceball[z - 1].originalSlice
        boundingCoords = spaceball[z - 1].boundingCoords
        if z == 1 or z == 399:
            continue



        # If we're on the last slice and an island doesn't terminate in Z
        # then it will not get counted, so just add all the remaining islands
        # to the count and return.
        if z == len(spaceball) - 5:

            numIntersections += len(islandsTop)
            print(numIntersections)
            # TODO: Temp for visualization
            for islandTop in islandsTop:
                for pixel in islandTop.coords:
                    temp1[pixel[0]][pixel[1]][0] = 0
                    temp1[pixel[0]][pixel[1]][1] = 255
                    temp1[pixel[0]][pixel[1]][2] = 0
            cv2.imshow('labeled', temp1[y0:y1, x0:x1])
            cv2.imshow('original', spaceball[z - 1].originalSlice[y0:y1, x0:x1])
            cv2.waitKey(0)
            break

        for islandTop in islandsTop:

            # TODO: Temp for visualization
            temp1 = convert_grayscale_stack_to_color(sliceTop)
            temp1 = cv2.circle(temp1, spaceball[z - 1].circleCenter, spaceball[z - 1].circleRadius, (255, 0, 0), 2)

            for pixel in islandTop.coords:
                temp1[pixel[0]][pixel[1]][2] = 100
            x0 = boundingCoords[0]
            y0 = boundingCoords[1]
            x1 = boundingCoords[2]
            y1 = boundingCoords[3]


            # If there are no islands in the slice below this one,
            # Assume we terminate all the islands in the current slice.
            if len(islandsBottom) == 0:
                numIntersections += len(islandsTop)
                print(numIntersections)

                for pixel in islandTop.coords:
                    temp1[pixel[0]][pixel[1]][0] = 0
                    temp1[pixel[0]][pixel[1]][1] = 255
                    temp1[pixel[0]][pixel[1]][2] = 0

                cv2.imshow('labeled', temp1[y0:y1, x0:x1])
                cv2.imshow('original', spaceball[z - 1].originalSlice[y0:y1, x0:x1])
                cv2.waitKey(0)

                break

            for i in range(0, len(islandsBottom)):
                for pixel in islandsBottom[i].coords:
                    temp1[pixel[0]][pixel[1]][2] = 255


                if check_if_islands_overlap(islandTop, islandsBottom[i]):
                    cv2.imshow('labeled', temp1[y0:y1, x0:x1])
                    cv2.imshow('original', spaceball[z - 1].originalSlice[y0:y1, x0:x1])
                    cv2.waitKey(0)
                    break
                elif i == len(islandsBottom) - 1:
                    numIntersections += 1
                    for pixel in islandTop.coords:
                        temp1[pixel[0]][pixel[1]][0] = 0
                        temp1[pixel[0]][pixel[1]][1] = 255
                        temp1[pixel[0]][pixel[1]][2] = 0

                    print(numIntersections)
                cv2.imshow('labeled', temp1[y0:y1, x0:x1])
                cv2.imshow('original', spaceball[z - 1].originalSlice[y0:y1, x0:x1])
                cv2.waitKey(0)


    print("count_unique_spaceball_intersections(): Completed!")
    return numIntersections


def check_if_islands_overlap(island1, island2):

    island1 = island1.coords
    island2 = island2.coords

    pixelSearchSpaceTransformations = [
        [2, 0],
        [2, 1],
        [2, 2],
        [2, -1],
        [2, -2],
        [1, 0],
        [1, 1],
        [1, 2],
        [1, -1],
        [1, -2],
        [0, 0],
        [0, 1],
        [0, 2],
        [0, -1],
        [0, -2],
        [-1, 0],
        [-1, 1],
        [-1, 2],
        [-1, -1],
        [-1, -2],
        [-2, 0],
        [-2, 1],
        [-2, 2],
        [-2, -1],
        [-2, -2]
    ]

    for coord in island1:

        if coord in island2:
            return True

        temp = coord

        for transformation in pixelSearchSpaceTransformations:

            temp[0] += transformation[0]
            temp[1] += transformation[1]

            if temp in island2:
                return True

            temp = coord

    return False



# Method 4:
# This method should implement systematic random sampling of the
# scan and perform methods 1-5 for each sample.
# The results of each sample should be stored.
def systematic_random_sample_GUI(stack):

    cv2.namedWindow('Sampling Window', cv2.WINDOW_NORMAL)
    maxProjection = max_project(stack)
    cv2.imshow('Sampling Window', maxProjection)
    cv2.waitKey(0)
    exit()



# Method 5:
# This method should take the total number of "Counted" blobs and feed that into the spaceballs algorithm.
def calculate_length_density(listOfIntersectionsPerSection, numSections, volumeBoxAroundSpaceball, spaceballRadius, sectionSamplingFraction):

    n = numSections
    Q = listOfIntersectionsPerSection
    v = volumeBoxAroundSpaceball
    a = 4 * 3.14 * spaceballRadius * spaceballRadius
    ssf = sectionSamplingFraction

    totalLengthEstimate = 0
    for i in range(0, len(Q)):
        totalLengthEstimate += Q[i]

    totalLengthEstimate = 2 * totalLengthEstimate * (v/a) * (1/ssf)
    return totalLengthEstimate










remove_all_pixels_below_threshold(stack, 25)
kernel_filter_2d(stack, (3, 3))
#systematic_random_sample_GUI(stack)
#totalLengthEstimate = calculate_length_density()
spaceball = gen_spaceball(stack, (1500, 400, 200), 200)
detect_islands_on_spaceball_slices(spaceball)


# BLOCK BELOW DISPLAYS ISLAND DETECTION VISUALLY
cv2.namedWindow('test', cv2.WINDOW_NORMAL)
num = 0
for slice in spaceball:
    print("NEW SLICE")
    x0 = slice.boundingCoords[0]
    y0 = slice.boundingCoords[1]
    x1 = slice.boundingCoords[2]
    y1 = slice.boundingCoords[3]
    currentRadius = 1500 - x0

    colorSlice = convert_grayscale_stack_to_color(slice.originalSlice)
    circleOverlay = cv2.circle(colorSlice, (1500, 400), currentRadius, (255, 0, 0), 2)

    for island in slice.islands:
        for pixel in island.coords:
            circleOverlay[pixel[0]][pixel[1]][2] = 255
    if num == 0 or num == 399:
        num += 1
        continue
    num += 1
    cv2.imshow('test', circleOverlay[y0:y1, x0:x1])
    cv2.waitKey(0)    


count = count_unique_spaceball_intersections(spaceball)






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
"""



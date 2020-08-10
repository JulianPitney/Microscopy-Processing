import cv2
import tifffile
import numpy as np
import zstackUtils as zsu
import xlrd
from os import listdir
from os.path import isfile, join
from scipy.interpolate import interp1d

DEBUG = False

dataDir = "../data/"
outputDir = "../cubes/"
aiviaExcelResultsDir = "../cubes_excel/"
stackPath = dataDir + "mouse12_july30_1laser_2x3_stitched.tif"
stack = tifffile.imread(stackPath)

class Cube(object):

    def __init__(self, data, ozr, oyr, oxr, totalPathLength):

        self.data = data
        # These are tuples containing the coordinates where the cube was cut from the original scan.
        self.original_z_range = ozr
        self.original_y_range = oyr
        self.original_x_range = oxr

        self.totalPathLength = totalPathLength

def suggest_even_multiples(stack):

    z = stack.shape[0]
    y = stack.shape[1]
    x = stack.shape[2]

    zEvenMultiples = []
    yEvenMultiples = []
    xEvenMultiples = []

    for i in range(40, 400):

        if z % i == 0:
            zEvenMultiples.append(i)
        if y % i == 0:
            yEvenMultiples.append(i)
        if x % i == 0:
            xEvenMultiples.append(i)


    print ("Even Multiples of Z [40-400):")
    print(zEvenMultiples)
    print()
    print("Even Multiples of Y [40-400):")
    print(yEvenMultiples)
    print()
    print("Even Multiples of X [40-400):")
    print(xEvenMultiples)
    print()


def crop3D():

    cv2.namedWindow("3DCrop Utility", cv2.WINDOW_KEEPRATIO)
    cv2.resizeWindow("3DCrop Utility", (500, 700))
    max = zsu.max_project(stack)
    cv2.imwrite('temp.jpg', max)
    max = cv2.imread('temp.jpg')

    print("Scan Dimensions: ")
    print("zDim=" + str(stack.shape[0]))
    print("yDim=" + str(stack.shape[1]))
    print("xDim=" + str(stack.shape[2]))

    notFinished = True

    while notFinished:

        copyForPainting = max.copy()
        croppedCorners = []

        for i in range(0, 4):
            cv2.imshow("3DCrop Utility", max)
            cv2.waitKey(1)
            x = int(input("Input corner#" + str(i) + " X Coord: "))
            y = int(input("Input corner#" + str(i) + " Y Coord: "))
            croppedCorners.append((x, y))

        cv2.line(copyForPainting, croppedCorners[0], croppedCorners[1], 200, 3)
        cv2.line(copyForPainting, croppedCorners[1], croppedCorners[2], 200, 3)
        cv2.line(copyForPainting, croppedCorners[2], croppedCorners[3], 200, 3)
        cv2.line(copyForPainting, croppedCorners[3], croppedCorners[0], 200, 3)



        cv2.imshow("3DCrop Utility", copyForPainting)
        cv2.waitKey(1)
        menuOption = input("Are the bounding boxes correct? [y/n]: ")
        if menuOption == 'y':
            notFinished = False
        elif menuOption == 'n':
            continue


    z_cropCoords = cropZ()


    croppedStack = stack[z_cropCoords[0]:z_cropCoords[1], croppedCorners[0][1]:croppedCorners[2][1], croppedCorners[0][0]:croppedCorners[2][0]]
    return croppedStack


def cropZ():

    cv2.namedWindow("3DCrop Utility X PROJ", cv2.WINDOW_KEEPRATIO)
    cv2.resizeWindow("3DCrop Utility X PROJ", (500, 700))
    max = zsu.max_project_x(stack)
    cv2.imwrite('temp.jpg', max)
    max = cv2.imread('temp.jpg')

    print("Scan Dimensions: ")
    print("zDim=" + str(stack.shape[0]))
    print("yDim=" + str(stack.shape[1]))
    print("xDim=" + str(stack.shape[2]))

    cv2.imshow("3DCrop Utility X PROJ", max)
    cv2.waitKey(1)

    notFinished = True

    while notFinished:

        copyForPainting = max.copy()
        z0 = int(input("Input z0 crop coord: "))
        z1 = int(input("Input z1 crop coord: "))
        cv2.line(copyForPainting, (0, z0), (max.shape[1], z0), 200, 4)
        cv2.line(copyForPainting, (0, z1), (max.shape[1], z1), 200, 4)
        cv2.imshow("3DCrop Utility X PROJ", copyForPainting)
        cv2.waitKey(1)
        menuOption = input("Are the Z crop lines correct? [y/n]: ")
        if menuOption == 'y':
            notFinished = False
        elif menuOption == 'n':
            continue


    return (z0, z1)

def slice_into_cubes(stack, zCube, yCube, xCube):

    if (stack.shape[0] % zCube != 0) or zCube == 0:
        print("Error: slice_into_cubes(): zCube must evenly divide stack z size.")
        exit(0)
    elif (stack.shape[1] % yCube != 0) or yCube == 0:
        print("Error: slice_into_cubes(): yCube must evenly divide stack y size.")
        exit(0)
    elif (stack.shape[2] % xCube != 0) or xCube == 0:
        print("Error: slice_into_cubes(): xCube must evenly divide stack x size.")
        exit(0)

    cubes = []

    for z in range(0, stack.shape[0], zCube):
        for y in range(0, stack.shape[1], yCube):
            for x in range(0, stack.shape[2], xCube):

                zRange = (z, z+zCube)
                yRange = (y, y+yCube)
                xRange = (x, x+xCube)
                data = stack[zRange[0]:zRange[1], yRange[0]:yRange[1], xRange[0]:xRange[1]]
                tempCube = Cube(data, zRange, yRange, xRange, -1)
                cubes.append(tempCube)

    return cubes

def save_cubes_to_tif(cubes):

        for cube in cubes:

            fileName = "cube_" + str(cube.original_z_range[0]) + "-" + str(cube.original_z_range[1])
            fileName += "_" + str(cube.original_y_range[0]) + "-" + str(cube.original_y_range[1])
            fileName += "_" + str(cube.original_x_range[0]) + "-" + str(cube.original_x_range[1]) + ".tif"
            tifffile.imwrite(outputDir + fileName, cube.data)


def parse_coords_from_filename(filename):

    coords = []
    filename = filename[5:-18]
    temp = filename.split('_')
    for item in temp:
        coord = item.split('-')
        coords.append((int(coord[0]), int(coord[1])))

    return coords


def load_aivia_excel_results_into_cubes(cube_results_dir):

    files = [f for f in listdir(cube_results_dir) if isfile(join(cube_results_dir, f))]
    cubes = []

    for file in files:

        try:
            wb = xlrd.open_workbook(cube_results_dir + file)
        except PermissionError:
            if DEBUG:
                print("Permission was denied for opening: " + file)
                print("Suggestion: Remove this file from directory or change it's permissions and try again.")
            exit(0)

        try:
            sheet = wb.sheet_by_index(4)
        except IndexError:
            if DEBUG:
                print("Dendrite Set.Total Length (px) page not found in file: " + file + ". This generally means Aivia's detection didn't find anything.")
            coords = parse_coords_from_filename(file)
            cube = Cube(None, coords[0], coords[1], coords[2], 0)
            cubes.append(cube)
        else:

            rows = []
            rowIndex = 1
            while 1:
                name = sheet.cell_value(rowIndex,0)
                if "Segment" in name:
                    break
                else:
                    rows.append(rowIndex)
                    rowIndex += 1

            totalPathLength = 0
            for row in rows:
                totalPathLength += sheet.cell_value(row, 1)

            coords = parse_coords_from_filename(file)
            cube = Cube(None, coords[0], coords[1], coords[2], totalPathLength)
            cubes.append(cube)

    return cubes


def map_path_lengths_to_range(cubes):

    pathLengths = []
    for cube in cubes:
        pathLengths.append(cube.totalPathLength)

    minPathLength = min(pathLengths)
    maxPathLength = max(pathLengths)
    m = interp1d([minPathLength, maxPathLength], [0, 255])
    pathLengths = m(pathLengths)

    for i in range(0, len(cubes)):

        cubes[i].totalPathLength = pathLengths[i]

    return cubes





cropped = crop3D()
max = zsu.max_project(cropped)
cv2.imwrite("test.jpg", max)
max = cv2.imread("test.jpg")
print("Scan Dimensions: ")
print("zDim=" + str(cropped.shape[0]))
print("yDim=" + str(cropped.shape[1]))
print("xDim=" + str(cropped.shape[2]))
cv2.imshow("test", max)
cv2.waitKey(0)

# Do this first
#cubes = slice_into_cubes(stack, 70, 256, 272)
#save_cubes_to_tif(cubes)

# Then run the cubes through aivia

# Then run aivia's results through this
#cubes = load_aivia_excel_results_into_cubes(aiviaExcelResultsDir)
#map_path_lengths_to_range(cubes)
#for cube in cubes:

#    stack[cube.original_z_range[0]:cube.original_z_range[1], \
#    cube.original_y_range[0]:cube.original_y_range[1], \
#    cube.original_x_range[0]:cube.original_x_range[1]] = cube.totalPathLength


#max = zsu.max_project(stack)
#cv2.imwrite('test.png', max)

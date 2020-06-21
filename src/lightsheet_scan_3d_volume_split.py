import cv2
import tifffile
import numpy as np
import zstackUtils as zsu
import xlrd
from os import listdir
from os.path import isfile, join

dataDir = "../data/"
outputDir = "../cubes/"
aiviaExcelResultsDir = "../cubes_excel/"
stackPath = dataDir + "cubicR_Feb20_1laser_5umstep.tif"

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
                print(data.shape)
                exit(0)
                tempCube = Cube(data, zRange, yRange, xRange)
                cubes.append(tempCube)

    return cubes

def save_cubes_to_tif(cubes):

        for cube in cubes:

            fileName = "cube_" + str(cube.original_z_range[0]) + ":" + str(cube.original_z_range[1])
            fileName += "_" + str(cube.original_y_range[0]) + ":" + str(cube.original_y_range[1])
            fileName += "_" + str(cube.original_x_range[0]) + ":" + str(cube.original_x_range[1]) + ".tif"
            tifffile.imwrite(outputDir + fileName, cube.data)


def load_aivia_excel_results_into_cubes(cube_results_dir):

    files = [f for f in listdir(cube_results_dir) if isfile(join(cube_results_dir, f))]
    cubes = []

    for file in files:

        try:
            wb = xlrd.open_workbook(cube_results_dir + file)
        except PermissionError:
            print("Permission was denied for opening: " + file)
            print("Suggestion: Remove this file from directory or change it's permissions and try again.")
            exit(0)

        try:
            sheet = wb.sheet_by_index(4)
        except IndexError:
            print("Dendrite Set.Total Length (px) page not found. This generally means Aivia's detection didn't find anything.")
            print("Skipping file: " + file)
            # TODO: If we skip the file because no dendrites were found, we still need to create a cube object for those
            # coordinates and set the totalPathLength to 0.
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

            # TODO: Parse XYZ ranges from file names and put them into cube objects.
            cube = Cube(None, -1, -1, -1, totalPathLength)
            cubes.append(cube)

    return cubes

cubes = load_aivia_excel_results_into_cubes(aiviaExcelResultsDir)
for cube in cubes:
    print(cube.totalPathLength)
#cubes = slice_into_cubes(stack, 70, 256, 272)
#save_cubes_to_tif(cubes)

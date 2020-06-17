import cv2
import tifffile
import numpy as np
import zstackUtils as zsu



stackPath = "../data/cubicR_Feb20_1laser_5umstep.tif"
stack = tifffile.imread(stackPath)

class Cube(object):

    def __init__(self, data, ozr, oyr, oxr):

        self.data = data
        # These are tuples containing the coordinates where the cube was cut from the original scan.
        self.original_z_range = ozr
        self.original_y_range = oyr
        self.original_x_range = oxr

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
                tempCube = Cube(data, zRange, yRange, xRange)
                cubes.append(tempCube)

    return cubes

def save_cubes_to_tif(cubes):

        tifffile.imwrite('../data/test.tif', cubes[400].data)


cubes = slice_into_cubes(stack, 70, 256, 272)
save_cubes_to_tif(cubes)

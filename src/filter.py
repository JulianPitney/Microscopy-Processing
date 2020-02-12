import tifffile
import numpy as np
import sys


if len(sys.argv) < 5:
        print("Invalid number of arguments. Try Again.")
        print("Usage: python filter.py <input_file_name> <block_size_z> <intensity_band_max> <intensity_band_min>")
        exit(0)
try:
        BLOCK_SIZE_Z = int(sys.argv[2])
except ValueError:
        print("Invalid value for <block_size_z>. Try again.")
        exit(0)
try:
        INTENSITY_THRESHOLD_MAX = int(sys.argv[3])
except ValueError:
        print("Invalid value for <intensity_band_max>. Try again.")
        exit(0)
try:
        INTENSITY_THRESHOLD_MIN = int(sys.argv[4])
except ValueError:
        print("Invalid value for <intensity_band_min>. Try again.")
        exit(0)



stackPath = "..\\data\\" + sys.argv[1]
print("Loading stack...")
stack = tifffile.imread(stackPath)
print("Done loading.")

blockIndeces = []

print("Generating blocks...")
for z in range(0, len(stack), BLOCK_SIZE_Z):

        block = []

        for i in range(z, z + BLOCK_SIZE_Z):

                if i >= len(stack):
                        continue

                subMatrix = np.where((stack[i] <= INTENSITY_THRESHOLD_MAX) & (stack[i] >= INTENSITY_THRESHOLD_MIN))
                block.append(subMatrix)

        blockIndeces.append(block)

print("Done generating blocks.")
for blockIndex in range(0, len(blockIndeces)):

        print("Processing block " + str(blockIndex+1) + "/" + str(len(blockIndeces)))
        sliceCoords = []
        for slice in blockIndeces[blockIndex]:
                sliceCoords.append(list(zip(*slice)))


        rejectedCoordinates = []
        for coord in sliceCoords[0]:

                reject = True
                for i in range((blockIndex * BLOCK_SIZE_Z) - 1, (blockIndex * BLOCK_SIZE_Z) + BLOCK_SIZE_Z - 1):
                        if INTENSITY_THRESHOLD_MIN <= stack[i+1][coord[0]][coord[1]] <= INTENSITY_THRESHOLD_MAX:
                                continue
                        else:
                                reject = False
                                break
                if reject:
                        rejectedCoordinates.append(coord)




        for coord in rejectedCoordinates:

                sliceCoord = (blockIndex * BLOCK_SIZE_Z) - 1

                while INTENSITY_THRESHOLD_MIN <= stack[sliceCoord][coord[0]][coord[1]] <= INTENSITY_THRESHOLD_MAX:
                        stack[sliceCoord][coord[0]][coord[1]] = 0
                        sliceCoord += 1
                        if sliceCoord >= len(stack):
                                break





print("Saving stack...")
tifffile.imwrite(stackPath[:-4] + "_filtered.tif", stack, imagej=False)
print("Done saving.")
print("Filtering complete!")
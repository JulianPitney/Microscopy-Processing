import tifffile
import zstackUtils as zsu
import numpy as np

stackPath = "..\\data\\cropped.tif"
stack = tifffile.imread(stackPath)

# if pixel between max and min intensity
# for num slices
# if pixel falls outside range remove pixel block
# # increment z block and repeat

#stack = np.arange(80).reshape(5, 4, 4)
#print(stack)
BLOCK_SIZE_Z = 5
INTENSITY_THRESHOLD_MAX = 140
INTENSITY_THRESHOLD_MIN = 80

blockIndeces = []

for z in range(0, len(stack), BLOCK_SIZE_Z):

        print(z)
        block = []

        for i in range(z, z + BLOCK_SIZE_Z):

                if i == len(stack):
                        continue

                subMatrix = np.where((stack[i] <= INTENSITY_THRESHOLD_MAX) & (stack[i] >= INTENSITY_THRESHOLD_MIN))
                block.append(subMatrix)

        blockIndeces.append(block)

for blockIndex in range(0, len(blockIndeces)):

        sliceCoords = []
        for slice in blockIndeces[blockIndex]:
                sliceCoords.append(list(zip(*slice)))


        rejectedCoordinates = []
        for coord in sliceCoords[0]:
                if coord not in sliceCoords[1:len(sliceCoords)]:
                        rejectedCoordinates.append(coord)

        



maxProjection = zsu.max_project(stack)
zsu.display_stack(maxProjection, 1)

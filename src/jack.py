import tifffile
import zstackUtils as zsu
import numpy as np

stackPath = "..\\data\\filtered_highpass.tif"
stack = tifffile.imread(stackPath)

NUM_FRAMES_THRESHOLD = 15
INTENSITY_THRESHOLD = 90

for z in range(0, len(stack) - NUM_FRAMES_THRESHOLD):

        print("SLICE" + str(z))
        subMatrix = np.where(stack[z] < INTENSITY_THRESHOLD)

        pixel = 0
        total = len(subMatrix[0])

        for pixel in range(0, len(subMatrix[0])):
            X = subMatrix[0][pixel]
            Y = subMatrix[1][pixel]
            pixel += 1
            reject = True
            for i in range(z + 1, z + NUM_FRAMES_THRESHOLD + 1):
                if stack[i][X][Y] > INTENSITY_THRESHOLD:
                    reject = False
                    break

            if reject:
                stack[z][X][Y] = 0



zsu.save_stack(stack)

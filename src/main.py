import cv2
import numpy as np
import tifffile

im = tifffile.imread("../data/X0_Y0.tif")






for i in range(0, 400):

    for y in range(0, len(im[i])):

        for x in range(0, len(im[i][y])):

            if im[i][y][x] >= 20:
                im[i][y][x] = 255
    print(str(i))



cv2.namedWindow('stack', cv2.WINDOW_NORMAL)

for slice in im[0:400]:
    cv2.imshow('stack', slice)
    cv2.waitKey(0)

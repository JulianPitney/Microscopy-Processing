import sys
import tifffile
import cv2
import zstackUtils as zsu



if len(sys.argv) != 4:
    print("Invalid number of arguments, try again.")
    print("USAGE: binarize.py <stack_path> <threshold> <save_flag>")
    exit(0)


stackPath = sys.argv[1]
thresholdMin = int(sys.argv[2])
saveFlag = int(sys.argv[3])

if not isinstance(stackPath, str):
    print("stackPath argument is not a valid string, try again.")
    print("USAGE: binarize.py <stack_path> <threshold> <save_flag>")
    exit(0)
if not isinstance(thresholdMin, int):
    print("thresholdMin argument is not a valid integer, try again.")
    print("USAGE: binarize.py <stack_path> <threshold> <save_flag>")
    exit(0)
if not isinstance(saveFlag, int) or (saveFlag != 0 and saveFlag != 1):
    print("save_flag argument is not a valid value, try again.")
    print("USAGE: binarize.py <stack_path> <threshold> <save_flag>")
    exit(0)




def displaySlice(slice):
    cv2.namedWindow('slice', cv2.WINDOW_NORMAL)
    cv2.imshow('slice', slice)
    cv2.waitKey(0)

def binarize(stack):
    stack[stack > 0] = 255



stack = tifffile.imread(stackPath)
zsu.remove_all_pixels_below_threshold(stack, thresholdMin)
zsu.kernel_filter_2d(stack, (3, 3))
binarize(stack)
maxProjection = zsu.max_project(stack)
displaySlice(maxProjection)
if saveFlag:
    zsu.save_stack(stack)


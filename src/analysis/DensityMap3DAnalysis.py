import sys
import config
import cv2
import tifffile
import math
import numpy as np
import zstackUtils as zsu
import xlrd
from os import remove
from os import listdir
from os.path import isfile, join
from scipy.interpolate import interp1d

DEBUG = False

def save_and_reload_maxproj(stack):

    max = zsu.max_project(stack)
    cv2.imwrite("temp.jpg", max)
    max = cv2.imread("temp.jpg")
    remove('temp.jpg')
    return max

def save_and_reload_maxproj_x(stack):

    max = zsu.max_project_x(stack)
    cv2.imwrite("temp.jpg", max)
    max = cv2.imread("temp.jpg")
    remove('temp.jpg')
    return max

def gen_stack_dims_dict(stack):

    return dict({'z': stack.shape[0], 'y': stack.shape[1], 'x': stack.shape[2]})

def print_scan_dims(stackDimsDict):

    print("Scan Dimensions")
    print("zDim=" + str(stackDimsDict['z']))
    print("yDim=" + str(stackDimsDict['y']))
    print("xDim=" + str(stackDimsDict['x']))





stack = tifffile.imread(config.STACK_FULL_PATH)
zProj = save_and_reload_maxproj(stack)
xProj = save_and_reload_maxproj_x(stack)
zProjClone = zProj.copy()
xProjClone = xProj.copy()


stackDims = gen_stack_dims_dict(stack)
stackAspectRatio = stackDims['y'] / stackDims['x']
xProjDims = dict({'x': xProj.shape[0], 'y': xProj.shape[1]})
xProjAspectRatio = xProjDims['y'] / xProjDims['x']

# Cropping config
CROP_WINDOW_NAME_XY = "3D Crop Utility XY"
CROP_WINDOW_NAME_Z = "3D Crop Utility Z"
DISPLAY_WIDTH = config.DISPLAY_WIDTH
DISPLAY_HEIGHT = config.DISPLAY_HEIGHT
CROP_WINDOW_WIDTH_XY = int(DISPLAY_HEIGHT - 100 * stackAspectRatio)
CROP_WINDOW_HEIGHT_XY = DISPLAY_HEIGHT - 100
CROP_WINDOW_WIDTH_Z = DISPLAY_WIDTH - 100
CROP_WINDOW_HEIGHT_Z = int(DISPLAY_WIDTH - 100 / xProjAspectRatio)
# Cropping globals for cv2 mouse callbacks
refPt = [(0, 0), (0, 0)]
z0 = 0
z1 = 0
XY_CROPPING_WINDOW_LMB_DOWN = False
XY_CROPPING_WINDOW_ACTIVE = False
Z_CROPPING_WINDOW_ACTIVE_LEFT = False
Z_CROPPING_WINDOW_ACTIVE_RIGHT = False


class Cube(object):

    def __init__(self, data, ozr, oyr, oxr, totalPathLength):
        self.data = data
        # These are tuples containing the coordinates where the cube was cut from the original scan.
        self.original_z_range = ozr
        self.original_y_range = oyr
        self.original_x_range = oxr

        self.totalPathLength = totalPathLength


def calc_xy_crop_snap_value(x):

    return int(math.ceil(x / config.XY_CROP_SNAP_INCREMENT)) * int(config.XY_CROP_SNAP_INCREMENT)

def calc_z_crop_snap_value(x):

    return int(math.ceil(x / config.Z_CROP_SNAP_INCREMENT)) * int(config.Z_CROP_SNAP_INCREMENT)

def click_and_crop(event, x, y, flags, param):

    global refPt, XY_CROPPING_WINDOW_ACTIVE, XY_CROPPING_WINDOW_LMB_DOWN, stackDims

    if event == cv2.EVENT_LBUTTONDOWN:
        refPt[0] = refPt[1] = (calc_xy_crop_snap_value(x), calc_xy_crop_snap_value(y))
        XY_CROPPING_WINDOW_ACTIVE = True
        XY_CROPPING_WINDOW_LMB_DOWN = True

    if event == cv2.EVENT_MOUSEMOVE and XY_CROPPING_WINDOW_LMB_DOWN:

        # TODO detect if cropping has gone outside bounds of scan
        x = calc_xy_crop_snap_value(x)
        y = calc_xy_crop_snap_value(y)

        if x > stackDims['x'] or y > stackDims['y']:
            pass
        else:
            refPt[1] = (x, y)

    if event == cv2.EVENT_LBUTTONUP and XY_CROPPING_WINDOW_LMB_DOWN:
        XY_CROPPING_WINDOW_LMB_DOWN = False

def click_and_z_crop(event, x, y, flags, param):

    global z0, z1, Z_CROPPING_WINDOW_ACTIVE_RIGHT, Z_CROPPING_WINDOW_ACTIVE_LEFT, xProjDims

    if event == cv2.EVENT_LBUTTONDOWN:

        temp = calc_z_crop_snap_value(y)

        if temp > xProjDims['y']:
            pass
        else:
            Z_CROPPING_WINDOW_ACTIVE_LEFT = True
            z0 = temp

    if event == cv2.EVENT_RBUTTONDOWN:

        temp = calc_z_crop_snap_value(y)

        if temp > xProjDims['y']:
            pass
        else:
            Z_CROPPING_WINDOW_ACTIVE_RIGHT = True
            z1 = temp

def select_cropping_colors():

    XYTextColor = (236, 43, 146)
    XYCropLineColor = (0, 255, 0)
    ZTextColor = (236, 43, 146)
    ZCropLineColor = (0, 255, 0)

    # XY crop conditions not OK
    if refPt[0][0] >= refPt[1][0] or refPt[0][1] >= refPt[1][1]:
        XYTextColor = (0, 0, 255)
        XYCropLineColor = (0, 0, 255)

    # Z crop conditions not OK
    if z0 >= z1:
        ZTextColor = (0, 0, 255)
        ZCropLineColor = (0, 0, 255)

    return [XYTextColor, XYCropLineColor, ZTextColor, ZCropLineColor]


def paint_cropping_text_xy(zProj, colors):

    cv2.putText(zProj, "xSize=" + str(refPt[1][0] - refPt[0][0]), (refPt[1][0] + 10, refPt[1][1]), cv2.FONT_HERSHEY_SIMPLEX, 4.0, colors[0], 8)
    cv2.putText(zProj, "ySize=" + str(refPt[1][1] - refPt[0][1]), (refPt[1][0] + 10, refPt[1][1] - 120), cv2.FONT_HERSHEY_SIMPLEX, 4.0, colors[0], 8)

def paint_cropping_lines_xy(zProj, colors):

    cv2.rectangle(zProj, refPt[0], refPt[1], colors[1], 8)

def paint_cropping_text_z(xProj, colors):

    cv2.putText(xProj, "zSize=" + str(z1 - z0), ((int(xProj.shape[1] / 2)) + 10, z0 + int((z1 - z0) / 2) + int(config.Z_CROP_SNAP_INCREMENT / 8)), cv2.FONT_HERSHEY_SIMPLEX, 2.0, colors[2], 4)

def paint_cropping_line_lmb_z(xProj, colors):

    cv2.line(xProj, (0, z0), (stackDims['x'], z0), colors[3], 2)

def paint_cropping_line_rmb_z(xProj, colors):

    cv2.line(xProj, (0, z1), (stackDims['x'], z1), colors[3], 2)

def paint_cropping_overlays(zProj, xProj, colors):

    if XY_CROPPING_WINDOW_ACTIVE:
        paint_cropping_lines_xy(zProj, colors)
        paint_cropping_text_xy(zProj, colors)

    if Z_CROPPING_WINDOW_ACTIVE_RIGHT:
        paint_cropping_line_rmb_z(xProj, colors)

    if Z_CROPPING_WINDOW_ACTIVE_LEFT:
        paint_cropping_line_lmb_z(xProj, colors)

    if Z_CROPPING_WINDOW_ACTIVE_LEFT and Z_CROPPING_WINDOW_ACTIVE_RIGHT:
        paint_cropping_text_z(xProj, colors)


def crop3D():

    global zProj, xProj

    cv2.namedWindow(CROP_WINDOW_NAME_XY, cv2.WINDOW_NORMAL)
    cv2.namedWindow(CROP_WINDOW_NAME_Z, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(CROP_WINDOW_NAME_XY, CROP_WINDOW_WIDTH_XY, CROP_WINDOW_HEIGHT_XY)
    cv2.resizeWindow(CROP_WINDOW_NAME_Z, CROP_WINDOW_WIDTH_Z, CROP_WINDOW_HEIGHT_Z)


    cv2.moveWindow(CROP_WINDOW_NAME_XY, 0, 0)
    cv2.moveWindow(CROP_WINDOW_NAME_Z, CROP_WINDOW_WIDTH_XY, 0)

    cv2.setMouseCallback(CROP_WINDOW_NAME_XY, click_and_crop)
    cv2.setMouseCallback(CROP_WINDOW_NAME_Z, click_and_z_crop)

    while True:

        # Render the cropping overlays for next frames
        colors = select_cropping_colors()
        paint_cropping_overlays(zProj, xProj, colors)

        # Display the frames with cropping overlays
        cv2.imshow(CROP_WINDOW_NAME_XY, zProj)
        cv2.imshow(CROP_WINDOW_NAME_Z, xProj)
        key = cv2.waitKey(1) & 0xFF

        # Wipe the overlay so next overlay draw has fresh frame
        zProj = zProjClone.copy()
        xProj = xProjClone.copy()

        # Check for user keyboard action
        if key == ord("c"):

            # Check cropping coordinates to make sure they make sense.
            if z0 >= z1:
                print("Z Crop Error: Bottom cannot be above Top. Try again.")
                continue
            elif refPt[0][0] >= refPt[1][0] or refPt[0][1] >= refPt[1][1]:
                print("XY Crop Error: Drag cropping box starting from top-left of desired crop. Try again.")
                continue
            else:
                cv2.destroyAllWindows()
                break


    croppedStack = stack[z0:z1, refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
    croppedStackDims = gen_stack_dims_dict(croppedStack)
    tifffile.imwrite(config.STACK_FULL_PATH[:-4] + "_cropped.tif", croppedStack)
    print_scan_dims(croppedStackDims)
    return croppedStack





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
                zRange = (z, z + zCube)
                yRange = (y, y + yCube)
                xRange = (x, x + xCube)
                data = stack[zRange[0]:zRange[1], yRange[0]:yRange[1], xRange[0]:xRange[1]]
                tempCube = Cube(data, zRange, yRange, xRange, -1)
                cubes.append(tempCube)

    return cubes


def save_cubes_to_tif(cubes):
    for cube in cubes:
        fileName = "cube_" + str(cube.original_z_range[0]) + "-" + str(cube.original_z_range[1])
        fileName += "_" + str(cube.original_y_range[0]) + "-" + str(cube.original_y_range[1])
        fileName += "_" + str(cube.original_x_range[0]) + "-" + str(cube.original_x_range[1]) + ".tif"
        tifffile.imwrite(config.CUBE_OUTPUT_DIR + fileName, cube.data)


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

        if ".tif" in file or ".xlsx" not in file:
            print("Skipping non-excel file")
            continue

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
                print(
                    "Dendrite Set.Total Length (px) page not found in file: " + file + ". This generally means Aivia's detection didn't find anything.")
            coords = parse_coords_from_filename(file)
            cube = Cube(None, coords[0], coords[1], coords[2], 0)
            cubes.append(cube)
        else:

            rows = []
            rowIndex = 1
            while 1:
                name = sheet.cell_value(rowIndex, 0)
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



# Do this first
cropped = crop3D()
cubes = slice_into_cubes(cropped, config.CUBE_DIM_Z, config.CUBE_DIM_Y, config.CUBE_DIM_X)
save_cubes_to_tif(cubes)


# Then run the cubes through aivia

# Then run aivia's results through this
# cubes = load_aivia_excel_results_into_cubes(config.AIVIA_EXCEL_RESULTS_DIR)
# map_path_lengths_to_range(cubes)
# for cube in cubes:

#    stack[cube.original_z_range[0]:cube.original_z_range[1], \
#    cube.original_y_range[0]:cube.original_y_range[1], \
#    cube.original_x_range[0]:cube.original_x_range[1]] = cube.totalPathLength


# max = zsu.max_project(stack)
# cv2.imwrite('test.png', max)

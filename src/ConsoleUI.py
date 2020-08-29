import AbstractPackages as AP
import LightsheetPackages as LP
from PackageFactory import PackageFactory
import config
from consolemenu import ConsoleMenu, SelectionMenu
from consolemenu.items import SubmenuItem, FunctionItem
from pathlib import Path
import cv2
from pathlib import Path
from time import sleep
from distutils.dir_util import copy_tree



def load_packages_directory():
    packagePaths = []
    packages = []
    displayNames = []
    p = Path('../packages/')
    for child in p.iterdir():
        scanPath = Path(child.joinpath(child.stem + ".p")).as_posix()
        print(scanPath)
        scan = AP.Package.load_package(scanPath)
        packagePaths.append(scanPath)
        packages.append(scan)
        displayName = scan.get_name() + "_" + scan.get_creationDate()
        displayNames.append(displayName)

    return packagePaths, packages, displayNames


def perform_new_analysis(analysisList):

    selection = SelectionMenu.get_selection(analysisList)
    print("Starting new " + str(selection) + " analysis!")

def select_existing_analysis(analysisList):

    selection = SelectionMenu.get_selection(analysisList)
    print("Getting " + str(selection) + "!")

def download_scan(scanUniqueID):

    # Start by assuming True, then go through a series of checks,
    # switching to False is any of them fail.
    downloadSuccess = True

    if not Path.is_dir(Path(config.DOWNLOADS_DIR)):
        downloadSuccess = False

    packageSrc = Path(config.PACKAGE_DIR).joinpath(scanUniqueID)
    packageDst = Path(config.DOWNLOADS_DIR).joinpath(scanUniqueID)
    if not Path.is_dir(packageSrc):
        downloadSuccess = False

    print("Downloading " + str(scanUniqueID))
    print("Source: AWS Cloud Database")
    print("Destination: " + str(packageDst))
    copy_tree(str(packageSrc), str(packageDst))
    if not Path.is_dir(packageDst):
        downloadSuccess = False


    if downloadSuccess:
        print("Download completed.")
    else:
        print("Download failed.")
    sleep(3)
def show_scan_metadata(attribs):

    for attrib in attribs.items():
        print(str(attrib[0]) + ": " + str(attrib[1]))

    input("\n\nPress enter to return")


def show_scan_maxproj(maxProjPath, displayName):

    maxProj = cv2.imread(maxProjPath, 0)
    cv2.namedWindow(displayName, cv2.WINDOW_NORMAL)
    cv2.moveWindow(displayName, 0, 0)
    cv2.resizeWindow(displayName, 500, 500)
    cv2.imshow(displayName, maxProj)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def select_scan():

    global lightsheetPackages, lightsheetScanPaths, displayNames

    scanIndex = SelectionMenu.get_selection(displayNames)

    if scanIndex >= len(displayNames):
        return None

    scanName = displayNames[scanIndex]
    scan = lightsheetPackages[scanIndex]
    attribs = scan.get_filled_attr_dict()


    # TODO: Open the scan and spawn the GUI showing the metadata and thumbnail

    analysisList = ['3D Density Map', 'Stroke Volume', 'Vessel Diameter']

    scanMenu = ConsoleMenu(scanName, exit_option_text="Close Scan")
    viewAttribsItem = FunctionItem("View Metadata", show_scan_metadata, [attribs])
    viewMaxProjItem = FunctionItem("View Max-Proj", show_scan_maxproj, [attribs['maxProjPath'], attribs['name']])
    #selectAnalysisPackageItem = FunctionItem("View Analysis", select_existing_analysis, [analysisList])
    #createNewAnalysisPackageItem = FunctionItem("Import Analysis", perform_new_analysis, [analysisList])
    downloadScanItem = FunctionItem("Download Copy", download_scan, [scan.get_uniqueID()])
    scanMenu.append_item(viewAttribsItem)
    scanMenu.append_item(viewMaxProjItem)
    #scanMenu.append_item(selectAnalysisPackageItem)
    #scanMenu.append_item(createNewAnalysisPackageItem)
    scanMenu.append_item(downloadScanItem)
    scanMenu.show()
    # TODO: Tear down the scan GUI and anything else that needs to be done to close it.

def create_scan():
    global lightsheetScanPaths, lightsheetPackages, displayNames

    packageFactory = PackageFactory()
    scan = packageFactory.create_package(LP.LightsheetBrainVasculatureScan)
    if scan == None:
        print("Failed to create LightsheetScan.")
    else:
        print("Successfully created LightsheetScan object in " + scan.get_relativePath())
        packagePath = scan.get_relativePath() + scan.get_uniqueID() + ".p"
        lightsheetScanPaths.append(packagePath)
        lightsheetPackages.append(scan)
        displayName = scan.get_name() + "_" + scan.get_creationDate()
        displayNames.append(displayName)

    sleep(3)


lightsheetScanPaths, lightsheetPackages, displayNames = load_packages_directory()

mainMenuTitle = "Data Manager"
mainMenuSubTitle = "v0.1"
mainMenuPrologue = "This program is designed to help the user organize and secure their scientific data."
mainMenuEpilogue = ""

lightsheetMenuTitle = "Lightsheet Data"
lightsheetPrologue = "This menu contains everything related to Lightsheet data."
lightsheetEpilogue = ""

mainMenu = ConsoleMenu(mainMenuTitle, mainMenuSubTitle, prologue_text=mainMenuPrologue, epilogue_text=mainMenuEpilogue)
lightsheetMenu = ConsoleMenu(lightsheetMenuTitle, prologue_text=lightsheetPrologue, epilogue_text=lightsheetEpilogue, exit_option_text="Main Menu")
lightsheetItem = SubmenuItem("Lightsheet Data", lightsheetMenu, mainMenu)
ephysMenu = ConsoleMenu("EPhys Data [Not Implemented]", exit_option_text="Main Menu")
ephysItem = SubmenuItem("Ephys Data", ephysMenu, mainMenu)
confocalMenu = ConsoleMenu("Confocal Data [Not Implemented]", exit_option_text="Main Menu")
confocalItem = SubmenuItem("Confocal Data", confocalMenu, mainMenu)
behaviorMenu = ConsoleMenu("Behavior Data [Not Implemented]", exit_option_text="Main Menu")
behaviorItem = SubmenuItem("Behavior Data", behaviorMenu, mainMenu)
cellCultureMenu = ConsoleMenu("Cell Culture Data [Not Implemented]", exit_option_text="Main Menu")
cellCultureItem = SubmenuItem("Cell Culture Data", cellCultureMenu, mainMenu)

openScanMenuItem = FunctionItem("Open Scan", select_scan, [], menu=lightsheetMenu)
importScanMenuItem = FunctionItem("Import Scan", create_scan, [])


mainMenu.append_item(lightsheetItem)
mainMenu.append_item(ephysItem)
mainMenu.append_item(confocalItem)
mainMenu.append_item(behaviorItem)
mainMenu.append_item(cellCultureItem)
lightsheetMenu.append_item(openScanMenuItem)
lightsheetMenu.append_item(importScanMenuItem)




mainMenu.show()


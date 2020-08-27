import AbstractPackages as AP
import LightsheetPackages as LP
from PackageFactory import PackageFactory
from consolemenu import ConsoleMenu, SelectionMenu
from consolemenu.items import SubmenuItem, FunctionItem
import consolemenu
from pathlib import Path
from time import sleep

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

    print("Downloading " + str(scanUniqueID) + " from the cloud!")

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
    downloadScanItem = FunctionItem("Download Scan", download_scan, [scan.get_uniqueID()])
    selectAnalysisPackageItem = FunctionItem("View Existing Analyses", select_existing_analysis, [analysisList])
    createNewAnalysisPackageItem = FunctionItem("Perform New Analysis", perform_new_analysis, [analysisList])
    scanMenu.append_item(downloadScanItem)
    scanMenu.append_item(selectAnalysisPackageItem)
    scanMenu.append_item(createNewAnalysisPackageItem)
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

def delete_scan():

    print("Deleting a scan!")


lightsheetScanPaths, lightsheetPackages, displayNames = load_packages_directory()

mainMenuTitle = "Data Goblins"
mainMenuSubTitle = "v0.1"
mainMenuPrologue = "This program is designed to help the user organize and secure their scientific data."
mainMenuEpilogue = ""

lightsheetMenuTitle = "Lightsheet Data"
lightsheetPrologue = "This menu contains everything related to Lightsheet data."
lightsheetEpilogue = ""

mainMenu = ConsoleMenu(mainMenuTitle, mainMenuSubTitle, prologue_text=mainMenuPrologue, epilogue_text=mainMenuEpilogue)
lightsheetMenu = ConsoleMenu(lightsheetMenuTitle, prologue_text=lightsheetPrologue, epilogue_text=lightsheetEpilogue)
lightsheetItem = SubmenuItem("Lightsheet Data", lightsheetMenu, mainMenu)
ephysMenu = ConsoleMenu("EPhys Data")
ephysItem = SubmenuItem("Ephys Data", ephysMenu, mainMenu)
confocalMenu = ConsoleMenu("Confocal Data")
confocalItem = SubmenuItem("Confocal Data", confocalMenu, mainMenu)
behaviorMenu = ConsoleMenu("Behavior Data")
behaviorItem = SubmenuItem("Behavior Data", behaviorMenu, mainMenu)
cellCultureMenu = ConsoleMenu("Cell Culture Data")
cellCultureItem = SubmenuItem("Cell Culture Data", cellCultureMenu, mainMenu)

openScanMenuItem = FunctionItem("Open Scan", select_scan, [], menu=lightsheetMenu)
importScanMenuItem = FunctionItem("Create Scan", create_scan, [])
deleteScanMenuItem = FunctionItem("Delete Scan", delete_scan, [])

mainMenu.append_item(lightsheetItem)
mainMenu.append_item(ephysItem)
mainMenu.append_item(confocalItem)
mainMenu.append_item(behaviorItem)
mainMenu.append_item(cellCultureItem)
lightsheetMenu.append_item(openScanMenuItem)
lightsheetMenu.append_item(importScanMenuItem)
lightsheetMenu.append_item(deleteScanMenuItem)




mainMenu.show()


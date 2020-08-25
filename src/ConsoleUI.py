import AbstractPackages as AP
import LightsheetPackages as LP
from PackageFactory import PackageFactory
from consolemenu import ConsoleMenu, SelectionMenu
from consolemenu.items import SubmenuItem, FunctionItem
from pathlib import Path
from time import sleep

def load_packages_directory():
    packagePaths = []
    packages = []
    p = Path('../packages/')
    for child in p.iterdir():
        scanPath = Path(child.joinpath(child.stem + ".p")).as_posix()
        print(scanPath)
        scan = AP.Package.load_package(scanPath)
        packagePaths.append(scanPath)
        packages.append(scan)
    return packagePaths, packages


def perform_new_analysis(analysisList):

    selection = SelectionMenu.get_selection(analysisList)
    print("Starting new " + str(selection) + " analysis!")

def select_existing_analysis(analysisList):

    selection = SelectionMenu.get_selection(analysisList)
    print("Getting " + str(selection) + "!")

def download_scan(scanName):

    print("Downloading " + str(scanName) + " from the cloud!")

def select_scan():

    global lightsheetPackages, lightsheetScanPaths

    scanIndex = SelectionMenu.get_selection(lightsheetScanPaths)

    if scanIndex >= len(lightsheetScanPaths):
        return None

    scanName = lightsheetScanPaths[scanIndex]
    scan = lightsheetPackages[scanIndex]
    # TODO: Open the scan and spawn the GUI showing the metadata and thumbnail

    analysisList = ['3D Density Map', 'Stroke Volume', 'Vessel Diameter']

    scanMenu = ConsoleMenu(scan.attrDict['name'], exit_option_text="Close Scan")
    downloadScanItem = FunctionItem("Download Scan", download_scan, [scanName])
    selectAnalysisPackageItem = FunctionItem("View Existing Analyses", select_existing_analysis, [analysisList])
    createNewAnalysisPackageItem = FunctionItem("Perform New Analysis", perform_new_analysis, [analysisList])
    scanMenu.append_item(downloadScanItem)
    scanMenu.append_item(selectAnalysisPackageItem)
    scanMenu.append_item(createNewAnalysisPackageItem)
    scanMenu.show()
    # TODO: Tear down the scan GUI and anything else that needs to be done to close it.

def create_scan():
    global lightsheetScanPaths, lightsheetPackages

    packageFactory = PackageFactory()
    scan = packageFactory.create_package(LP.LightsheetBrainVasculatureScan)
    if scan == None:
        print("Failed to create LightsheetScan.")
    else:
        print("Successfully created LightsheetScan object in " + scan.get_relativePath())
        packagePath = scan.attrDict['relativePath'] + scan.attrDict['uniqueID'] + ".p"
        lightsheetScanPaths.append(packagePath)
        lightsheetPackages.append(scan)

    sleep(3)

def delete_scan():

    print("Deleting a scan!")


lightsheetScanPaths, lightsheetPackages = load_packages_directory()

mainMenuTitle = "Data Manager"
mainMenuSubTitle = "v0.1"
mainMenuPrologue = "This program is designed to ensure to organization, integrity and security of arbitrary sets of data. "
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


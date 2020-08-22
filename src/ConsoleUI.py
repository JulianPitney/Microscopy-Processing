from consolemenu import ConsoleMenu, SelectionMenu
from consolemenu.items import SubmenuItem, FunctionItem

def perform_new_analysis(analysisList):

    selection = SelectionMenu.get_selection(analysisList, show_exit_option=False)
    print("Starting new " + str(selection) + " analysis!")

def select_existing_analysis(analysisList):

    selection = SelectionMenu.get_selection(analysisList, show_exit_option=False)
    print("Getting " + str(selection) + "!")

def download_scan(scanName):

    print("Downloading " + str(scanName) + " from the cloud!")

def select_scan(scanStringList):
    scanIndex = SelectionMenu.get_selection(scanStringList, show_exit_option=False)
    scanName = scanStringList[scanIndex]
    # TODO: Open the scan and spawn the GUI showing the metadata and thumbnail

    analysisList = ['3D Density Map', 'Stroke Volume', 'Vessel Diameter']

    scanMenu = ConsoleMenu(scanName, exit_option_text="Close Scan")
    downloadScanItem = FunctionItem("Download Scan", download_scan, [scanName])
    selectAnalysisPackageItem = FunctionItem("View Existing Analyses", select_existing_analysis, [analysisList])
    createNewAnalysisPackageItem = FunctionItem("Perform New Analysis", perform_new_analysis, [analysisList])
    scanMenu.append_item(downloadScanItem)
    scanMenu.append_item(selectAnalysisPackageItem)
    scanMenu.append_item(createNewAnalysisPackageItem)
    scanMenu.show()
    # TODO: Tear down the scan GUI and anything else that needs to be done to close it.

def import_scan():

    print("Importing a scan!")

def delete_scan():

    print("Deleting a scan!")



lightsheetScans = ["scan1", 'scan2', 'scan3']

mainMenuTitle = "Data Manager"
mainMenuSubTitle = "v0.1"
mainMenuPrologue = "This program is designed to help our lab manage data."
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

openScanMenuItem = FunctionItem("Open Scan", select_scan, [lightsheetScans], menu=lightsheetMenu)
importScanMenuItem = FunctionItem("Import Scan", import_scan, [])
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


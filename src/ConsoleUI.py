from consolemenu import ConsoleMenu, SelectionMenu
from consolemenu.items import SubmenuItem, FunctionItem


def select_scan(scanStringList):
    scanIndex = SelectionMenu.get_selection(scanStringList, show_exit_option=False)
    print(scanIndex)

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

openScanMenuItem = FunctionItem("Open Scan", select_scan, [lightsheetScans], menu=lightsheetMenu)

mainMenu.append_item(lightsheetItem)
lightsheetMenu.append_item(openScanMenuItem)
mainMenu.show()


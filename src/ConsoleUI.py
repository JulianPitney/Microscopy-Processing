from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem, SubmenuItem, CommandItem


mainMenu0 = ConsoleMenu("Data Manager", "v0.1")
lightsheetScansSubmenu1 = ConsoleMenu("Lightsheet Scans")
confocalScansSubMenu1 = ConsoleMenu("Confocal Scans")
behaviorTrialsSubmenu1 = ConsoleMenu("Behavior Trials")
ephysTrialsSubMenu1 = ConsoleMenu("Ephys Trials")
cellCultureTrialsSubMenu1 = ConsoleMenu("Cell Culture Trials")
importLightsheetScanSubmenu2 = ConsoleMenu("Import Lightsheet Scan(s)")
selectLightsheetScanSubmenu2 = ConsoleMenu("Select Lightsheet Scan(s)")
exportLightsheetScanSubmenu2 = ConsoleMenu("Export Lightsheet Scan(s)")


lightsheetScansSubmenu1_item = SubmenuItem("Lightsheet Scans", lightsheetScansSubmenu1, menu=mainMenu0)
confocalScansSubMenu1_item = SubmenuItem("Confocal Scans", confocalScansSubMenu1, menu=mainMenu0)
behaviorTrialsSubmenu1_item = SubmenuItem("Behavior Trials", behaviorTrialsSubmenu1, menu=mainMenu0)
ephysTrialsSubMenu1_item = SubmenuItem("Ephys Trials", ephysTrialsSubMenu1, menu=mainMenu0)
cellCultureTrialsSubMenu1_item = SubmenuItem("Cell Culture Trials", cellCultureTrialsSubMenu1, menu=mainMenu0)
importLightsheetScanSubmenu2_item = SubmenuItem("Import Lightsheet Scan(s)", importLightsheetScanSubmenu2, menu=lightsheetScansSubmenu1)
selectLightsheetScanSubmenu2_item = SubmenuItem("Select Lightsheet Scan(s)", selectLightsheetScanSubmenu2, menu=lightsheetScansSubmenu1)
exportLightsheetScanSubmenu2_item = SubmenuItem("Export Lightsheet Scan(s)", exportLightsheetScanSubmenu2, menu=lightsheetScansSubmenu1)


mainMenu0.append_item(lightsheetScansSubmenu1_item)
mainMenu0.append_item(confocalScansSubMenu1_item)
mainMenu0.append_item(behaviorTrialsSubmenu1_item)
mainMenu0.append_item(ephysTrialsSubMenu1_item)
mainMenu0.append_item(cellCultureTrialsSubMenu1_item)
lightsheetScansSubmenu1.append_item(importLightsheetScanSubmenu2_item)
lightsheetScansSubmenu1.append_item(selectLightsheetScanSubmenu2_item)
lightsheetScansSubmenu1.append_item(exportLightsheetScanSubmenu2_item)

mainMenu0.show()

#command_item = CommandItem("Run a console command", "touch hello.txt")
#function_item = FunctionItem("Call a function", test_func, [-15])

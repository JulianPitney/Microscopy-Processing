import AnalysisPackage
import pickle


class LightsheetDensityMap3DAnalysisPackage(AnalysisPackage.AnalysisPackage):

    def __init__(self, name, uniqueID, relativePath, fullPath, sizeGB, startDate, completionDate):
        super().__init__(name, uniqueID, relativePath, fullPath, sizeGB, startDate, completionDate)

    def __del__(self):
        super().__del__()

    def load_package(self):
        pass

    def save_package(self):
        pass


class LightsheetStrokeVolumeAnalysisPackage(AnalysisPackage.AnalysisPackage):

    def __init__(self, name, uniqueID, relativePath, fullPath, sizeGB, startDate, completionDate):
        super().__init__(name, uniqueID, relativePath, fullPath, sizeGB, startDate, completionDate)

    def __del__(self):
        super().__del__()

    def load_package(self):
        pass

    def save_package(self):
        pass


class LightsheetVesselDiameterAnalysisPackage(AnalysisPackage.AnalysisPackage):

    def __init__(self, name, uniqueID, relativePath, fullPath, sizeGB, startDate, completionDate):
        super().__init__(name, uniqueID, relativePath, fullPath, sizeGB, startDate, completionDate)

    def __del__(self):
        super().__del__()

    def load_package(self):
        pass

    def save_package(self):
        pass


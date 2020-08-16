from AbstractPackages import Package, DataPackage, AnalysisPackage
from LightsheetPackages import LightsheetScan, LengthDensityMap3DAnalysis, StrokeVolumeAnalysis, VesselDiameterAnalysis


class PackageFactory(object):

    def create_package(self, packageType):

        if issubclass(packageType, Package):
            packageCreator = self.get_package_creator(packageType)
            return packageCreator(packageType)
        else:
            return None

    def get_package_creator(self, packageType):

        if issubclass(packageType, DataPackage):
            return self.get_DataPackage_creator(packageType)
        elif issubclass(packageType, AnalysisPackage):
            return self.get_AnalysisPackage_creator(packageType)
        else:
            return None

    def get_DataPackage_creator(self, packageType):

        if packageType == LightsheetScan:
            return self.create_LightsheetScan
        else:
            return None

    def get_AnalysisPackage_creator(self, packageType):

        if packageType == LengthDensityMap3DAnalysis:
            return self.create_LengthDensityMap3DAnalysis
        elif packageType == StrokeVolumeAnalysis:
            return self.create_StrokeVolumeAnalysis
        elif packageType == VesselDiameterAnalysis:
            return self.create_VesselDiameterAnalysis
        else:
            return None

    def create_LightsheetScan(self, packageType):
        print("Created LightsheetScan")
        attrDict = LightsheetScan.get_attr_dict()
        return LightsheetScan(attrDict)

    def create_LengthDensityMap3DAnalysis(self, packageType):
        print("Created LengthDensityMap3DAnalysis")
        attrDict = LengthDensityMap3DAnalysis.get_attr_dict()
        return LengthDensityMap3DAnalysis(attrDict)

    def create_StrokeVolumeAnalysis(self, packageType):
        print("Created StrokeVolumeAnalysis")
        attrDict = StrokeVolumeAnalysis.get_attr_dict()
        return StrokeVolumeAnalysis(attrDict)

    def create_VesselDiameterAnalysis(self, packageType):
        print("Created VesselDiameterAnalysis")
        attrDict = VesselDiameterAnalysis.get_attr_dict()
        return VesselDiameterAnalysis(attrDict)

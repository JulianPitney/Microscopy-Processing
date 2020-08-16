from uuid import uuid4

from AbstractPackages import Package, DataPackage, AnalysisPackage
from LightsheetPackages import LightsheetScan, LengthDensityMap3DAnalysis, StrokeVolumeAnalysis, VesselDiameterAnalysis
import config
from pathlib import Path

class PackageFactory(object):

#---------------------------------------------------------------------------------------------#
# Functions that are general to all Package types.                                            #
#---------------------------------------------------------------------------------------------#
    def print_error_message(self, msg):
        print("PackageFactory Error: " + msg)

    def gen_unique_Package_ID(self):
        # TODO: Implement proper unique package ID function
        uuid = str(uuid4())
        print(uuid)
        return uuid

    def create_Package_directory(self):

        rootDir = config.PACKAGE_DIR
        uniqueID = self.gen_unique_Package_ID()
        relativePath = rootDir + uniqueID + "/"

        try:
            Path(relativePath).mkdir(parents=False, exist_ok=False)
        except FileExistsError:
            self.print_error_message("FileExistsError. Package directory creation failed.")
        except FileNotFoundError:
            self.print_error_message("FileNotFoundError. Package directory creation failed.")
        except:
            self.print_error_message("UnknownError. Package directory creation failed.")
        else:
            return uniqueID, relativePath

        return None, None

#---------------------------------------------------------------------------------------------#
# Functions for selecting which PackageCreator function we want to use                        #
#---------------------------------------------------------------------------------------------#
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

#---------------------------------------------------------------------------------------------#
# LightsheetScan creation is handled here.                                                    #
#---------------------------------------------------------------------------------------------#
    def create_LightsheetScan(self, packageType):

        # TODO: Creator methods should ensure all the required attributes are set
        #  and valid before passing the attrDict to the class's constructor.
        #  Once all the required attributes are set and validated, object initialization
        #  is passed off to the class's __init__().
        #  Think of this like the Essence pattern for object creation.
        #  The attrDict is the essence and the creator method
        #  is responsible for initializing the essence. This
        #  ensures we never accidentally create objects with
        #  an invalid state and gives a clear separation of
        #  responsibility (Creator ensures everything needed for object creation
        #  is present, while object __init__ handles actual creation).

        objectCreationSuccess = True
        attrDict = LightsheetScan.get_empty_attr_dict()
        requiredAttributes = [
            'name',
            'uniqueID',
            'sizeGB',
            'stitchedPath',
            'tilesPath',
            'relativePath',
            'creationDate'
        ]

        attrDict['name'] = "LightsheetScan"
        attrDict['sizeGB'] = 9001
        attrDict['creationDate'] = "madeup:date"
        attrDict['uniqueID'], attrDict['relativePath'] = self.create_Package_directory()

        attrDict['tilesPath'] = input("Input tiles full path: ")
        attrDict['stitchedPath'] = input("Input stitched scan full path: ")
        stitchImportSuccess = self.import_stitched_LightsheetScan(attrDict['stitchedPath'], attrDict['relativePath'])
        tilesImportSuccess = self.import_tiles_LightsheetScan(attrDict['tilesPath'], attrDict['relativePath'])

        if stitchImportSuccess and tilesImportSuccess:
            pass
        else:
            objectCreationSuccess = False
            self.print_error_message("ObjectCreationError. LightsheetScan object creation failed because the scan files could not be imported.")

        # Based on the result of the Essence setup, decide whether to proceed
        # with object creation.
        if objectCreationSuccess:
            return LightsheetScan(attrDict)
        else:
            return None


    def import_stitched_LightsheetScan(self, stitchedPath, lightsheetScanPath):

        fileImportSuccess = True
        stitchedPath = Path(stitchedPath)
        lightsheetScanPath = Path(lightsheetScanPath)

        if not stitchedPath.exists():
            fileImportSuccess = False

        if not lightsheetScanPath.exists():
            fileImportSuccess = False

        outputStitchedPath = Path(lightsheetScanPath.joinpath('Stitched/'))

        try:
            outputStitchedPath.mkdir(parents=False, exist_ok=False)
        except FileExistsError:
            self.print_error_message("FileExistsError. Stitched scan directory creation failed.")
            fileImportSuccess = False
        except FileNotFoundError:
            self.print_error_message("FileNotFoundError. Stitched scan directory creation failed.")
            fileImportSuccess = False
        except:
            self.print_error_message("UnknownError. Stitched scan directory creation failed.")
            fileImportSuccess = False

        stitchedScanFileName = stitchedPath.stem + stitchedPath.suffix
        stitchedPath.rename(outputStitchedPath.joinpath(stitchedScanFileName))

        return fileImportSuccess


    def import_tiles_LightsheetScan(self, tilesPath, lightsheetScanPath):
        return True



#---------------------------------------------------------------------------------------------#
# LengthDensityMap3DAnalysis creation is handled here.                                        #
#---------------------------------------------------------------------------------------------#
    def create_LengthDensityMap3DAnalysis(self, packageType):
        print("Created LengthDensityMap3DAnalysis")
        attrDict = LengthDensityMap3DAnalysis.get_empty_attr_dict()
        return LengthDensityMap3DAnalysis(attrDict)

#---------------------------------------------------------------------------------------------#
# StrokeVolumeAnalysis creation is handled here.                                              #
#---------------------------------------------------------------------------------------------#
    def create_StrokeVolumeAnalysis(self, packageType):
        print("Created StrokeVolumeAnalysis")
        attrDict = StrokeVolumeAnalysis.get_empty_attr_dict()
        return StrokeVolumeAnalysis(attrDict)

#---------------------------------------------------------------------------------------------#
# VesselDiameterAnalysis creation is handled here.                                            #
#---------------------------------------------------------------------------------------------#
    def create_VesselDiameterAnalysis(self, packageType):
        print("Created VesselDiameterAnalysis")
        attrDict = VesselDiameterAnalysis.get_empty_attr_dict()
        return VesselDiameterAnalysis(attrDict)




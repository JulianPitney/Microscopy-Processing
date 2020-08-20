from uuid import uuid4
from AbstractPackages import Package, DataPackage, AnalysisPackage
from LightsheetPackages import LightsheetScan, LengthDensityMap3DAnalysis, StrokeVolumeAnalysis, VesselDiameterAnalysis
import config
from pathlib import Path

class PackageFactory(object):

#---------------------------------------------------------------------------------------------#
# Functions that are general to all Package types.                                            #
#---------------------------------------------------------------------------------------------#
    @staticmethod
    def print_error_message(msg):
        print("PackageFactory Error: " + msg)

    # Takes a libpath Path object and attempts to create the directory.
    # Returns false on failure and true on success.
    def create_directory(self, pathObj):

        try:
            Path(pathObj).mkdir(parents=False, exist_ok=False)
        except FileExistsError:
            self.print_error_message("FileExistsError. Package directory creation failed.")
        except FileNotFoundError:
            self.print_error_message("FileNotFoundError. Package directory creation failed.")
        except:
            self.print_error_message("UnknownError. Package directory creation failed.")
        else:
            return True

        return False

    def create_Package_directory_and_UID(self):

        rootDir = config.PACKAGE_DIR
        uniqueID = self.gen_unique_Package_ID()
        relativePath = rootDir + uniqueID + "//"

        dirCreationSuccess = self.create_directory(relativePath)
        if dirCreationSuccess:
            return uniqueID, relativePath

        return None, None

    def gen_unique_Package_ID(self):
        # TODO: Implement proper unique package ID function
        return str(uuid4())

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
# LightsheetScan creation is done here.                                                    #
#---------------------------------------------------------------------------------------------#

    # This function attempts to create a LightsheetScan object. It will attempt to set and validate
    # all the required parameters for creating a LightsheetScan object. If it fails to set and validate
    # any of the required parameters, it will return None. If it succeeds, it will return a valid
    # LightsheetScan object.
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
        #  is present, while object __init__() handles actual creation).

        # Default success is true, then we go through a list of checks that
        # will flip this to false if any of them fail.
        objectCreationSuccess = True
        lightsheetScan = None

        # Get a dictionary that contains all the attributes our object has. All attributes
        # default to None.
        attrDict = LightsheetScan.get_empty_attr_dict()

        # This list specifies which attributes MUST be set and valid before object creation can be
        # attempted.
        requiredAttributes = [
            'name',
            'uniqueID',
            'sizeGB',
            'stitchedPath',
            'tilesPath',
            'relativePath',
            'creationDate'
        ]

        # Attempt to set and validate all required attributes.
        # TODO: Setting everything manually until this gets hooked up to some front end that can set them automatically
        attrDict['name'] = "LightsheetScan"
        attrDict['sizeGB'] = 9001
        attrDict['creationDate'] = "madeup:date"
        attrDict['uniqueID'], attrDict['relativePath'] = self.create_Package_directory_and_UID()
        attrDict['tilesPath'] = input("Input tiles full path: ")
        attrDict['stitchedPath'] = input("Input stitched scan full path: ")


        stitchImportSuccess, stitchScanFinalPath = self.import_stitched_LightsheetScan(attrDict['stitchedPath'], attrDict['relativePath'])
        tilesImportSuccess, tilesFinalPath = self.import_tiles_LightsheetScan(attrDict['tilesPath'], attrDict['relativePath'])
        if not stitchImportSuccess or not tilesImportSuccess:
            objectCreationSuccess = False

        # If objectCreationSuccess has not been set to false, we're safe to attempt object creation.
        if objectCreationSuccess:
            attrDict['stitchedPath'] = stitchScanFinalPath
            attrDict['tilesPath'] = tilesFinalPath
            lightsheetScan = LightsheetScan(attrDict)
            lightsheetScanObjDumpPath = Path(attrDict['relativePath']).joinpath(Path(attrDict['uniqueID'] + '.p'))
            objectCreationSuccess = lightsheetScan.save_package(lightsheetScanObjDumpPath)

        return lightsheetScan

    def import_stitched_LightsheetScan(self, inputStitchedScanPath, objectRootDir):

        # Default success is true, then we go through a list of checks that
        # will flip this to false if any of them fail.
        fileImportSuccess = True
        outputStitchedScanPath = None

        # Make sure the file to be imported exists and that the location it's being imported to
        # exists as well.
        inputStitchedScanPath = Path(inputStitchedScanPath)
        objectRootDir = Path(objectRootDir)

        if not inputStitchedScanPath.exists():
            fileImportSuccess = False
        if not objectRootDir.exists():
            fileImportSuccess = False

        # Create the subdirectory where the file is going to be imported to.
        outputStitchedScanPath = Path(objectRootDir.joinpath('Stitched/'))
        dirCreationSuccess = self.create_directory(outputStitchedScanPath)
        if not dirCreationSuccess:
            fileImportSuccess = False

        # If everything above worked properly, import the file.
        if fileImportSuccess:
            stitchedScanFileName = inputStitchedScanPath.stem + inputStitchedScanPath.suffix
            outputStitchedScanPath = outputStitchedScanPath.joinpath(stitchedScanFileName)
            inputStitchedScanPath.rename(outputStitchedScanPath)

        # Return code specifies whether import failed or succeeded.
        return fileImportSuccess, outputStitchedScanPath


    def import_tiles_LightsheetScan(self, inputTilesScanPath, objectRootDir):

        # Default success is true, then we go through a list of checks that
        # will flip this to false if any of them fail.
        fileImportSuccess = True
        outputTilesPath = None

        # Make sure the file to be imported exists and that the location it's being imported to
        # exists as well.
        inputTilesScanPath = Path(inputTilesScanPath)
        objectRootDir = Path(objectRootDir)

        if not inputTilesScanPath.exists():
            fileImportSuccess = False
        if not objectRootDir.exists():
            fileImportSuccess = False

        # If everything above worked properly, import the file.
        if fileImportSuccess:
            stitchedScanFileName = inputTilesScanPath.stem + inputTilesScanPath.suffix
            outputTilesPath = objectRootDir.joinpath(stitchedScanFileName)
            inputTilesScanPath.rename(outputTilesPath)

        # Return code specifies whether import failed or succeeded.
        return fileImportSuccess, outputTilesPath






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




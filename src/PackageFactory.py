from AbstractPackages import Package, DataPackage, AnalysisPackage
import LightsheetPackages as LP
import config
from pathlib import Path
from uuid import uuid4

class PackageFactory(object):

#---------------------------------------------------------------------------------------------#
# Functions that are general to all Package types.                                            #
#---------------------------------------------------------------------------------------------#
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
        relativePath = rootDir + uniqueID + "/"

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

        if issubclass(packageType, LP.LightsheetScan):
            return self.get_LightsheetScan_creator(packageType)
        else:
            return None

    def get_AnalysisPackage_creator(self, packageType):

        if packageType == LP.LengthDensityMap3DAnalysis:
            return self.create_LengthDensityMap3DAnalysis
        elif packageType == LP.StrokeVolumeAnalysis:
            return self.create_StrokeVolumeAnalysis
        elif packageType == LP.VesselDiameterAnalysis:
            return self.create_VesselDiameterAnalysis
        else:
            return None

    def get_LightsheetScan_creator(self, packageType):
        if packageType == LP.LightsheetBrainVasculatureScan:
            return self.create_LightsheetBrainVasculatureScan


#---------------------------------------------------------------------------------------------#
# LightsheetBrainVasculatureScan creation is done here.                                                    #
#---------------------------------------------------------------------------------------------#

    # This function attempts to create a LightsheetScan object. It will attempt to set and validate
    # all the required parameters for creating a LightsheetScan object. If it fails to set and validate
    # any of the required parameters, it will return None. If it succeeds, it will return a valid
    # LightsheetScan object.
    def create_LightsheetBrainVasculatureScan(self, packageType):

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
        #
        #   TODO: This function sucks because it depends on details internal to LightsheetBrainVasculatureScan objects.
        #       This function should be told which values need to be set by the LightsheetBrainVasculatureScan class to
        #       eliminate the dependency.

        # Default success is true, then we go through a list of checks that
        # will flip this to false if any of them fail.
        objectCreationSuccess = True
        scan = None
        # Get a dictionary that contains all the attributes our object has. All attributes
        # default to None.
        attrDict = LP.LightsheetBrainVasculatureScan.get_empty_attr_dict()

        # Attempt to set and validate all required attributes.
        # TODO: Setting everything manually until this gets hooked up to some front end that can set them automatically
        #   These are also missing any kind of sanitization/validation.
        #   Also missing any kind of user guide/descriptions.
        attrDict['name'] = str(input("Input Scan Name: "))
        attrDict['uniqueID'], attrDict['relativePath'] = self.create_Package_directory_and_UID()
        attrDict['creationDate'] = str(input("Input Creation Date: "))
        attrDict['stitchedPath'] = str(input("Input Stitched Path: "))
        attrDict['tilesPath'] = str(input("Input Tiles Path: "))
        attrDict['numTiles'] = str(input("Input Tile Dims: "))
        attrDict['tileSizeZ'] = int(input("Input tileSizeZ: "))
        attrDict['tileSizeY'] = int(input("Input tileSizeY: "))
        attrDict['tileSizeX'] = int(input("Input tileSizeX: "))
        attrDict['bitDepth'] = int(input("Input bitDepth: "))
        attrDict['authorName'] = str(input("Input authorName: "))
        attrDict['specimenName'] = str(input("Input specimenName: "))
        attrDict['specimenPrepProtocol'] = str(input("Input Protocol Name: "))
        attrDict['notes'] = str(input("Input notes: "))
        attrDict['umStepSizeZ'] = float(input("Input umStepSizeZ: "))
        attrDict['umPerStep'] = float(input("Input umPerStep: "))
        attrDict['scanStepSpeed'] = float(input("Input scanStepSpeed: "))
        attrDict['sleepDurationAfterMovement'] = float(input("Input sleepDurationAfterMovement: "))
        attrDict['timelapseN'] = int(input("Input timelapseN: "))
        attrDict['timelapseIntervalS'] = int(input("Input timelapseIntervalS: "))
        attrDict['tileScanDimensions'] = str(input("Input tileScanDims: "))
        attrDict['imagingObjectiveMagnification'] = float(input("Input Imaging Objective Mag: "))
        attrDict['umPerPixel'] = float(input("Input umPerPixel: "))
        attrDict['refractiveIndexImmersion'] = float(input("Input Refractive Index Immersion: "))
        attrDict['numericalAperture'] = float(input("Input Numerical Aperture Collection: "))
        attrDict['fluorescenceWavelength'] = int(input("Input Fluorescence Wavelength: "))
        attrDict['umTileOverlapX'] = float(input("Input Tile Overlap X µm: "))
        attrDict['umTileOverlapY'] = float(input("Input Tile Overlap Y µm: "))

        stitchImportSuccess, stitchScanFinalPath = self.import_stitched_LightsheetScan(attrDict['stitchedPath'], attrDict['relativePath'])
        tilesImportSuccess, tilesFinalPath = self.import_tiles_LightsheetScan(attrDict['tilesPath'], attrDict['relativePath'])
        if not stitchImportSuccess or not tilesImportSuccess:
            objectCreationSuccess = False

        # If objectCreationSuccess has not been set to false, we're safe to attempt object creation.
        if objectCreationSuccess:
            attrDict['stitchedPath'] = stitchScanFinalPath
            attrDict['tilesPath'] = tilesFinalPath
            scan = LP.LightsheetBrainVasculatureScan(attrDict)
            lightsheetScanObjDumpPath = Path(attrDict['relativePath']).joinpath(Path(attrDict['uniqueID'] + '.p'))
            objectCreationSuccess = scan.save_package(lightsheetScanObjDumpPath)

        return scan

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
        attrDict = LP.LengthDensityMap3DAnalysis.get_empty_attr_dict()
        return LP.LengthDensityMap3DAnalysis(attrDict)

#---------------------------------------------------------------------------------------------#
# StrokeVolumeAnalysis creation is handled here.                                              #
#---------------------------------------------------------------------------------------------#
    def create_StrokeVolumeAnalysis(self, packageType):
        print("Created StrokeVolumeAnalysis")
        attrDict = LP.StrokeVolumeAnalysis.get_empty_attr_dict()
        return LP.StrokeVolumeAnalysis(attrDict)

#---------------------------------------------------------------------------------------------#
# VesselDiameterAnalysis creation is handled here.                                            #
#---------------------------------------------------------------------------------------------#
    def create_VesselDiameterAnalysis(self, packageType):
        print("Created VesselDiameterAnalysis")
        attrDict = LP.VesselDiameterAnalysis.get_empty_attr_dict()
        return LP.VesselDiameterAnalysis(attrDict)




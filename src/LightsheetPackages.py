from AbstractPackages import Package, DataPackage, AnalysisPackage
from PackageExceptions import PackageError
from pathlib import Path
from zStackUtils import load_stack, max_project, save_and_reload_maxproj, save_png

class LightsheetScan(DataPackage):

    attrDict = {
        'stitchedPath': None,
        'tilesPath': None,
        'maxProjPath': None,
        'analysisPackagesPath': None,
        'numTiles': None,
        'tileSizeZ': None,
        'tileSizeY': None,
        'tileSizeX': None,
        'bitDepth': None,
        'authorName': None,
        'specimenName': None,
        'specimenPrepProtocol': None,
        'notes': None,
        'umStepSizeZ': None,
        'umPerStep': None,
        'scanStepSpeed': None,
        'sleepDurationAfterMovement': None,
        'timelapseN': None,
        'timelapseIntervalS': None,
        'tileScanDimensions': None,
        'imagingObjectiveMagnification': None,
        'umPerPixel': None,
        'refractiveIndexImmersion': None,
        'numericalAperture': None,
        'fluorescenceWavelength': None,
        'umTileOverlapX': None,
        'umTileOverlapY': None
    }

    def __init__(self, attrDict):

        super().__init__(attrDict)
        self.set_stitchedPath(attrDict['stitchedPath'])
        self.set_tilesPath(attrDict['tilesPath'])
        self.set_maxProjPath(attrDict['maxProjPath'])
        self.set_analysisPackagesPath(attrDict['analysisPackagesPath'])
        self.set_numTiles(attrDict['numTiles'])
        self.set_tileSizeZ(attrDict['tileSizeZ'])
        self.set_tileSizeY(attrDict['tileSizeY'])
        self.set_tileSizeX(attrDict['tileSizeX'])
        self.set_bitDepth(attrDict['bitDepth'])
        self.set_authorName(attrDict['authorName'])
        self.set_specimenName(attrDict['specimenName'])
        self.set_specimenPrepProtocol(attrDict['specimenPrepProtocol'])
        self.set_notes(attrDict['notes'])
        self.set_umStepSizeZ(attrDict['umStepSizeZ'])
        self.set_umPerStep(attrDict['umPerStep'])
        self.set_scanStepSpeed(attrDict['scanStepSpeed'])
        self.set_sleepDurationAfterMovement(attrDict['sleepDurationAfterMovement'])
        self.set_timeLapseN(attrDict['timelapseN'])
        self.set_timelapseIntervalS(attrDict['timelapseIntervalS'])
        self.set_tileScanDimensions(attrDict['tileScanDimensions'])
        self.set_imagingObjectiveMagnification(attrDict['imagingObjectiveMagnification'])
        self.set_umPerPixel(attrDict['umPerPixel'])
        self.set_refrativeIndexImmersion(attrDict['refractiveIndexImmersion'])
        self.set_numericalAperture(attrDict['numericalAperture'])
        self.set_fluorescenceWavelength(attrDict['fluorescenceWavelength'])
        self.set_umTileOverlapX(attrDict['umTileOverlapX'])
        self.set_umTileOverlapY(attrDict['umTileOverlapY'])


        # Any time we initialize a Package we should check
        # that all attributes are initialized to a valid state.
        try:
            self.resource_wellness_check()
        except PackageError as e: print(e)

        # If all the attributes seem okay, generate a thumbnail for the package.
        self.gen_maxproj_thumbnail()

    def __del__(self):
        super().__del__()

    @staticmethod
    def get_empty_attr_dict():
        concatenatedDict = {}
        parentDict = DataPackage.get_empty_attr_dict()
        childDict = {
            'stitchedPath': None,
            'tilesPath': None,
            'maxProjPath': None,
            'analysisPackagesPath': None,
            'numTiles': None,
            'tileSizeZ': None,
            'tileSizeY': None,
            'tileSizeX': None,
            'bitDepth': None,
            'authorName': None,
            'specimenName': None,
            'specimenPrepProtocol': None,
            'notes': None,
            'umStepSizeZ': None,
            'umPerStep': None,
            'scanStepSpeed': None,
            'sleepDurationAfterMovement': None,
            'timelapseN': None,
            'timelapseIntervalS': None,
            'tileScanDimensions': None,
            'imagingObjectiveMagnification': None,
            'umPerPixel': None,
            'refractiveIndexImmersion': None,
            'numericalAperture': None,
            'fluorescenceWavelength': None,
            'umTileOverlapX': None,
            'umTileOverlapY': None
        }
        concatenatedDict.update(parentDict)
        concatenatedDict.update(childDict)
        return concatenatedDict

    # This should be called immediately after
    # loading an object. This will verify
    # that the resources pointed to by the
    # object still exist. This may not be necessary
    # once we move away from the raw filesystem
    # for storing data.
    #
    # Returns True if object is valid
    def resource_wellness_check(self):

        resourcesToCheck = [
            'relativePath',
            'stitchedPath',
            'maxProjPath',
            'tilesPath',
            'maxProjPath',
            'analysisPackagesPath'
        ]

        for attr in resourcesToCheck:
            resourcePath = self.attrDict[attr]
            print(resourcePath)
            # If the resource isn't initialized to anything we don't have to worry about it.
            # If it is initialized, check that everything is cool.
            if resourcePath == None:
                continue
            elif not Path(resourcePath).exists():
                raise PackageError("A lightsheetScan object has failed to find it's [" + attr + "] resource at: " + str(resourcePath))

    def gen_maxproj_thumbnail(self):

        full_path = self.get_stitchedPath().absolute()
        full_path = full_path.as_posix()
        stitchedStack = load_stack(full_path)
        maxProj = save_and_reload_maxproj(stitchedStack)
        maxProjPath = self.get_relativePath() + "thumbnail.png"
        save_png(maxProjPath, maxProj)
        self.set_maxProjPath(maxProjPath)



    # Setters
    def set_stitchedPath(self, stitchedPath):
        self.attrDict['stitchedPath'] = stitchedPath

    def set_tilesPath(self, tilesPath):
        self.attrDict['tilesPath'] = tilesPath

    def set_maxProjPath(self, maxProjPath):
        self.attrDict['maxProjPath'] = maxProjPath

    def set_analysisPackagesPath(self, analysisPackagesPath):
        self.attrDict['analysisPackagesPath'] = analysisPackagesPath

    def set_numTiles(self, numTiles):
        self.attrDict['numTiles'] = numTiles

    def set_tileSizeZ(self, tileSizeZ):
        self.attrDict['tileSizeZ'] = tileSizeZ

    def set_tileSizeY(self, tileSizeY):
        self.attrDict['tileSizeY'] = tileSizeY

    def set_tileSizeX(self, tileSizeX):
        self.attrDict['tileSizeX'] = tileSizeX

    def set_bitDepth(self, bitDepth):
        self.attrDict['bitDepth'] = bitDepth

    def set_authorName(self, authorName):
        self.attrDict['authorName'] = authorName

    def set_specimenName(self, specimenName):
        self.attrDict['specimenName'] = specimenName

    def set_specimenPrepProtocol(self, specimenPrepProtocol):
        self.attrDict['specimenPrepProtocol'] = specimenPrepProtocol

    def set_notes(self, notes):
        self.attrDict['notes'] = notes

    def set_umStepSizeZ(self, umStepSizeZ):
        self.attrDict['umStepSizeZ'] = umStepSizeZ

    def set_umPerStep(self, umPerStep):
        self.attrDict['umPerStep'] = umPerStep

    def set_scanStepSpeed(self, scanStepSpeed):
        self.attrDict['scanStepSpeed'] = scanStepSpeed

    def set_sleepDurationAfterMovement(self, sleepDurationAfterMovement):
        self.attrDict['sleepDurationAfterMovement'] = sleepDurationAfterMovement

    def set_timeLapseN(self, timeLapseN):
        self.attrDict['timeLapseN'] = timeLapseN

    def set_timelapseIntervalS(self, timelapseIntervalS):
        self.attrDict['timelapseIntervalS'] = timelapseIntervalS

    def set_tileScanDimensions(self, tileScanDimensions):
        self.attrDict['tileScanDimensions'] = tileScanDimensions

    def set_imagingObjectiveMagnification(self, imagingObjectiveMagnification):
        self.attrDict['imagingObjectiveMagnification'] = imagingObjectiveMagnification

    def set_umPerPixel(self, umPerpixel):
        self.attrDict['umPerPixel'] = umPerpixel

    def set_refrativeIndexImmersion(self, refractiveIndexImmersion):
        self.attrDict['refractiveIndexImmersion'] = refractiveIndexImmersion

    def set_numericalAperture(self, numericalAperture):
        self.attrDict['numericalAperture'] = numericalAperture

    def set_fluorescenceWavelength(self, fluorescenceWavelength):
        self.attrDict['fluorescenceWavelength'] = fluorescenceWavelength

    def set_umTileOverlapX(self, umTileOverlapX):
        self.attrDict['umTileOverlapX'] = umTileOverlapX

    def set_umTileOverlapY(self, umTileOverlapY):
        self.attrDict['umTileOverlapY'] = umTileOverlapY

        # Getters
    def get_stitchedPath(self):
        return self.attrDict['stitchedPath']

    def get_tilesPath(self):
        return self.attrDict['tilesPath']

    def get_maxProjPath(self):
        return self.attrDict['maxProjPath']

    def get_analysisPackagesPath(self):
        return self.attrDict['analysisPackagesPath']

    def get_numTiles(self):
        return self.attrDict['numTiles']

    def get_tileSizeZ(self):
        return self.attrDict['tileSizeZ']

    def get_tileSizeY(self):
        return self.attrDict['tileSizeY']

    def get_tileSizeX(self):
        return self.attrDict['tileSizeX']

    def get_bitDepth(self):
        return self.attrDict['bitDepth']

    def get_authorName(self):
        return self.attrDict['authorName']

    def get_specimenName(self):
        return self.attrDict['specimenName']

    def get_specimenPrepProtocol(self):
        return self.attrDict['specimenPrepProtocol']

    def get_notes(self):
        return self.attrDict['notes']

    def get_umStepSizeZ(self):
        return self.attrDict['umStepSizeZ']

    def get_umPerStep(self):
        return self.attrDict['umPerStep']

    def get_scanStepSpeed(self):
        return self.attrDict['scanStepSpeed']

    def get_sleepDurationAfterMovement(self):
        return self.attrDict['sleepDurationAfterMovement']

    def get_timeLapseN(self):
        return self.attrDict['timeLapseN']

    def get_timelapseIntervalS(self):
        return self.attrDict['timelapseIntervalS']

    def get_tileScanDimensions(self):
        return self.attrDict['tileScanDimensions']

    def get_imagingObjectiveMagnification(self):
        return self.attrDict['imagingObjectiveMagnification']

    def get_umPerPixel(self):
        return self.attrDict['umPerPixel']

    def get_refractiveIndexImmersion(self):
        return self.attrDict['refractiveIndexImmersion']

    def get_numericalApperture(self):
        return self.attrDict['numericalAperture']

    def get_fluorescenceWavelength(self):
        return self.attrDict['fluorescenceWavelength']

    def get_umTileOverlapX(self):
        return self.attrDict['umTileOverlapX']

    def get_umTileOverlapY(self):
        return self.attrDict['umTileOverlapY']


class LengthDensityMap3DAnalysis(AnalysisPackage):

    attrDict = {

    }

    def __init__(self, attrDict):
        super().__init__(attrDict)

    def __del__(self):
        super().__del__()

    @staticmethod
    def get_empty_attr_dict():
        concatenatedDict = {}
        parentDict = AnalysisPackage.get_empty_attr_dict()
        childDict = {

        }
        concatenatedDict.update(parentDict)
        concatenatedDict.update(childDict)
        return concatenatedDict


class StrokeVolumeAnalysis(AnalysisPackage):

    attrDict = {

    }

    def __init__(self, attrDict):
        super().__init__(attrDict)

    def __del__(self):
        super().__del__()

    @staticmethod
    def get_empty_attr_dict():
        concatenatedDict = {}
        parentDict = AnalysisPackage.get_empty_attr_dict()
        childDict = {

        }
        concatenatedDict.update(parentDict)
        concatenatedDict.update(childDict)
        return concatenatedDict


class VesselDiameterAnalysis(AnalysisPackage):

    attrDict = {

    }

    def __init__(self, attrDict):
        super().__init__(attrDict)

    def __del__(self):
        super().__del__()

    @staticmethod
    def get_empty_attr_dict():
        concatenatedDict = {}
        parentDict = AnalysisPackage.get_empty_attr_dict()
        childDict = {

        }
        concatenatedDict.update(parentDict)
        concatenatedDict.update(childDict)
        return concatenatedDict

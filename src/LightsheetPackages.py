from AbstractPackages import Package, DataPackage, AnalysisPackage


class LightsheetScan(DataPackage):

    # Scan Info
    numTiles = None
    tileSizeZ = None
    tileSizeY = None
    tileSizeX = None
    bitDepth = None

    # Lightsheet Config
    umStepSizeZ = None
    umPerStep = None
    scanStepSpeed = None
    sleepDurationAfterMovement = None
    timelapseN = None
    timelapseIntervalS = None
    tileScanDimensions = None
    imagingObjectiveMagnification = None
    umPerPixel = None
    refractiveIndexImmersion = None
    numericalAperture = None
    fluorescenceWavelength = None
    umTileOverlapX = None
    umTileOverlapY = None

    def __init__(self, attrDict):
        super().__init__(attrDict)
        self.set_numTiles(attrDict['numTiles'])
        self.set_tileSizeZ(attrDict['tileSizeZ'])
        self.set_tileSizeY(attrDict['tileSizeY'])
        self.set_tileSizeX(attrDict['tileSizeX'])
        self.set_bitDepth(attrDict['bitDepth'])
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

    def __del__(self):
        super().__del__()

    @staticmethod
    def get_attr_dict():
        concatenatedDict = {}
        parentDict = DataPackage.get_attr_dict()
        childDict = {
            'numTiles': None,
            'tileSizeZ': None,
            'tileSizeY': None,
            'tileSizeX': None,
            'bitDepth': None,
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

    # Setters
    def set_numTiles(self, numTiles):
        self.numTiles = numTiles

    def set_tileSizeZ(self, tileSizeZ):
        self.tileSizeZ = tileSizeZ

    def set_tileSizeY(self, tileSizeY):
        self.tileSizeY = tileSizeY

    def set_tileSizeX(self, tileSizeX):
        self.tileSizeX = tileSizeX

    def set_bitDepth(self, bitDepth):
        self.bitDepth = bitDepth

    def set_umStepSizeZ(self, umStepSizeZ):
        self.umStepSizeZ = umStepSizeZ

    def set_umPerStep(self, umPerStep):
        self.umPerStep = umPerStep

    def set_scanStepSpeed(self, scanStepSpeed):
        self.scanStepSpeed = scanStepSpeed

    def set_sleepDurationAfterMovement(self, sleepDurationAfterMovement):
        self.sleepDurationAfterMovement = sleepDurationAfterMovement

    def set_timeLapseN(self, timeLapseN):
        self.timelapseN = timeLapseN

    def set_timelapseIntervalS(self, timelapseIntervalS):
        self.timelapseIntervalS = timelapseIntervalS

    def set_tileScanDimensions(self, tileScanDimensions):
        self.tileScanDimensions = tileScanDimensions

    def set_imagingObjectiveMagnification(self, imagingObjectiveMagnification):
        self.imagingObjectiveMagnification = imagingObjectiveMagnification

    def set_umPerPixel(self, umPerpixel):
        self.umPerPixel = umPerpixel

    def set_refrativeIndexImmersion(self, refractiveIndexImmersion):
        self.refractiveIndexImmersion = refractiveIndexImmersion

    def set_numericalAperture(self, numericalAperture):
        self.numericalAperture = numericalAperture

    def set_fluorescenceWavelength(self, fluorescenceWavelength):
        self.fluorescenceWavelength = fluorescenceWavelength

    def set_umTileOverlapX(self, umTileOverlapX):
        self.umTileOverlapX = umTileOverlapX

    def set_umTileOverlapY(self, umTileOverlapY):
        self.umTileOverlapY = umTileOverlapY

    # Getters
    def get_numTiles(self):
        return self.numTiles

    def get_tileSizeZ(self):
        return self.tileSizeZ

    def get_tileSizeY(self):
        return self.tileSizeY

    def get_tileSizeX(self):
        return self.tileSizeX

    def get_bitDepth(self):
        return self.bitDepth

    def get_umStepSizeZ(self):
        return self.umStepSizeZ

    def get_umPerStep(self):
        return self.umPerStep

    def get_scanStepSpeed(self):
        return self.scanStepSpeed

    def get_sleepDurationAfterMovement(self):
        return self.sleepDurationAfterMovement

    def get_timeLapseN(self):
        return self.timelapseN

    def get_timelapseIntervalS(self):
        return self.timelapseIntervalS

    def get_tileScanDimensions(self):
        return self.tileScanDimensions

    def get_imagingObjectiveMagnification(self):
        return self.imagingObjectiveMagnification

    def get_umPerPixel(self):
        return self.umPerPixel

    def get_refrativeIndexImmersion(self):
        return self.refractiveIndexImmersion

    def get_numericalApperture(self):
        return self.numericalAperture

    def get_fluorescenceWavelength(self):
        return self.fluorescenceWavelength

    def get_umTileOverlapX(self):
        return self.umTileOverlapX

    def get_umTileOverlapY(self):
        return self.umTileOverlapY


class LengthDensityMap3DAnalysis(AnalysisPackage):

    def __init__(self, attrDict):
        super().__init__(attrDict)

    def __del__(self):
        super().__del__()

    @staticmethod
    def get_attr_dict():
        concatenatedDict = {}
        parentDict = AnalysisPackage.get_attr_dict()
        childDict = {

        }
        concatenatedDict.update(parentDict)
        concatenatedDict.update(childDict)
        return concatenatedDict


class StrokeVolumeAnalysis(AnalysisPackage):

    def __init__(self, attrDict):
        super().__init__(attrDict)

    def __del__(self):
        super().__del__()

    @staticmethod
    def get_attr_dict():
        concatenatedDict = {}
        parentDict = AnalysisPackage.get_attr_dict()
        childDict = {

        }
        concatenatedDict.update(parentDict)
        concatenatedDict.update(childDict)
        return concatenatedDict


class VesselDiameterAnalysis(AnalysisPackage):

    def __init__(self, attrDict):
        super().__init__(attrDict)

    def __del__(self):
        super().__del__()

    @staticmethod
    def get_attr_dict():
        concatenatedDict = {}
        parentDict = AnalysisPackage.get_attr_dict()
        childDict = {

        }
        concatenatedDict.update(parentDict)
        concatenatedDict.update(childDict)
        return concatenatedDict

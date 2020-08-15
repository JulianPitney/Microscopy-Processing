import DataPackage
import pickle


class LightsheetDataPackage(DataPackage.DataPackage):

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
    fluoresenceWavelength = None
    umTileOverlapX = None
    umTileOverlapY = None

    analysisPackages = []

    def __init__(self, name, uniqueID, relativePath, fullPath, creationDate, sizeGB, numTiles,
                 tileSizeZ, tileSizeY, tileSizeX, bitDepth, umStepSizeZ, umPerStep, scanStepSpeed,
                 sleepDurationAfterMovement, timelapseN, timelapseIntervalS, tileScanDimensions,
                 imagingObjectiveMagnification, umPerPixel, refractiveIndexImmersion,
                 numericalAperture, fluoresenceWavelength, umTileOverlapX, umTileOverlapY,):

        super().__init__(name, uniqueID, relativePath, fullPath, creationDate, sizeGB)
        self.set_numTiles(numTiles)
        self.set_tileSizeZ(tileSizeZ)
        self.set_tileSizeY(tileSizeY)
        self.set_tileSizeX(tileSizeX)
        self.set_bitDepth(bitDepth)
        self.set_umStepSizeZ(umStepSizeZ)
        self.set_umPerStep(umPerStep)
        self.set_scanStepSpeed(scanStepSpeed)
        self.set_sleepDurationAfterMovement(sleepDurationAfterMovement)
        self.set_timeLapseN(timelapseN)
        self.set_timelapseIntervalS(timelapseIntervalS)
        self.set_tileScanDimensions(tileScanDimensions)
        self.set_imagingObjectiveMagnification(imagingObjectiveMagnification)
        self.set_umPerPixel(umPerPixel)
        self.set_refrativeIndexImmersion(refractiveIndexImmersion)
        self.set_numericalApperture(numericalAperture)
        self.set_fluoresenceWavelength(fluoresenceWavelength)
        self.set_umTileOverlapX(umTileOverlapX)
        self.set_umTileOverlapY(umTileOverlapY)

    def __del__(self):
        super().__del__()

    # I/O
    @staticmethod
    def load_package():
        return pickle.load(open("LightsheetDataPackage.p", 'rb'))

    def save_package(self):
        pickle.dump(self, open("LightsheetDataPackage.p", 'wb'))

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

    def set_numericalApperture(self, numericalApperture):
        self.numericalAperture = numericalApperture

    def set_fluoresenceWavelength(self, fluoresenceWavelength):
        self.fluoresenceWavelength = fluoresenceWavelength

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

    def get_fluoresenceWavelength(self):
        return self.fluoresenceWavelength

    def get_umTileOverlapX(self):
        return self.umTileOverlapX

    def get_umTileOverlapY(self):
        return self.umTileOverlapY

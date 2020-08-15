import LightsheetDataPackage
import LightsheetAnalysisPackages


def main():

    name = "test"
    uniqueID = 42
    relativePath = None
    fullPath = None
    creationDate = None
    sizeGB = None

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

    scan = LightsheetDataPackage.LightsheetDataPackage(name, uniqueID, relativePath, fullPath, creationDate, sizeGB,
                                                       numTiles, tileSizeZ, tileSizeY, tileSizeX, bitDepth,
                                                       umStepSizeZ, umPerStep, scanStepSpeed,
                                                       sleepDurationAfterMovement, timelapseN, timelapseIntervalS,
                                                       tileScanDimensions, imagingObjectiveMagnification,
                                                       umPerPixel, refractiveIndexImmersion, numericalAperture,
                                                       fluoresenceWavelength, umTileOverlapX, umTileOverlapY)

    scan.save_package()
    del scan
    scan = LightsheetDataPackage.LightsheetDataPackage.load_package()
    print(scan.name)


if __name__ == '__main__':
    main()

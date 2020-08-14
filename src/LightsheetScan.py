
class AnalysisPackage(object):

    relativePath = None
    fullPath = None
    sizeGB = None
    startDate = None
    completionDate = None

    def __init__(self):
        print("Created AnalysisPackage object")

    def __del__(self):
        print("Destroyed AnalysisPackage object!")


class DensityMap3DPackage(AnalysisPackage):

    def __init__(self):
        super().__init__()
        print("Created DensityMap3DPackage object")

    def __del__(self):
        print("Destroyed DensityMap3DPackage object!")


class StrokeVolumePackage(AnalysisPackage):

    def __init__(self):
        super().__init__()
        print("Created StrokeVolumePackage object")

    def __del__(self):
        print("Destroyed StrokeVolumePackage object!")


class VesselDiameterPackage(AnalysisPackage):

    def __init__(self):
        super().__init__()
        print("Created VesselDiameterPackage object")

    def __del__(self):
        print("Destroyed VesselDiameterPackage object!")


class LightsheetScan(object):

    # Scan Info
    scanFileName = None
    scanRelativePath = None
    scanFullPath = None
    scanCreationDate = None
    analysisPackages = []

    def __init__(self):
        print("Created LightsheetScan object!")

    def __del__(self):
        print("Destroyed LightsheetScan object!")


scans = []
for i in range(0, 10):
    scans.append(LightsheetScan())
    scans[i].analysisPackages.append(DensityMap3DPackage())
    scans[i].analysisPackages.append(StrokeVolumePackage())
    scans[i].analysisPackages.append(VesselDiameterPackage())

from PackageFactory import PackageFactory
from LightsheetPackages import LightsheetScan, LengthDensityMap3DAnalysis

def main():

    packageFactory = PackageFactory()

    scans = []
    for i in range(0, 5):
        temp = packageFactory.create_package(LightsheetScan)




if __name__ == '__main__':
    main()

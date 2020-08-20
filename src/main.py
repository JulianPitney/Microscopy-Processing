from AbstractPackages import Package
from PackageExceptions import PackageError
from PackageFactory import PackageFactory
from LightsheetPackages import LightsheetScan, LengthDensityMap3DAnalysis


def main():

    packageFactory = PackageFactory()
    scan = packageFactory.create_package(LightsheetScan)

if __name__ == '__main__':
    main()

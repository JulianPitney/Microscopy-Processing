from PackageFactory import PackageFactory
from AbstractPackages import Package
from LightsheetPackages import LightsheetScan, LengthDensityMap3DAnalysis


def main():

    packageFactory = PackageFactory()
    scan = packageFactory.create_package(LightsheetScan)


if __name__ == '__main__':
    main()

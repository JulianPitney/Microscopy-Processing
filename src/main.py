from AbstractPackages import Package
from PackageExceptions import PackageError
from PackageFactory import PackageFactory
from LightsheetPackages import LightsheetBrainVasculatureScan


def main():

# Create new package
    packageFactory = PackageFactory()
    scan = packageFactory.create_package(LightsheetBrainVasculatureScan)


# Load existing package
"""
    scan = Package.load_package("C:\Projects\Microscopy-Processing\packages\e0cae438-9ea7-4839-8ac4-7fb8dffdb263\e0cae438-9ea7-4839-8ac4-7fb8dffdb263.p")
    for key, val in scan.attrDict.items():
        print(str(key) + ": " + str(val))
"""

if __name__ == '__main__':
    main()

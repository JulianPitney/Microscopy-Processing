import pickle


class Package(object):

    name = None
    uniqueID = None
    relativePath = None
    fullPath = None
    creationDate = None
    sizeGB = None

    def __init__(self, attrDict):
        self.set_name(attrDict['name'])
        self.set_uniqueID(attrDict['uniqueID'])
        self.set_relativePath(attrDict['relativePath'])
        self.set_fullPath(attrDict['fullPath'])
        self.set_creationDate(attrDict['creationDate'])
        self.set_sizeGB(attrDict['sizeGB'])

    def __del__(self):
        pass

    @staticmethod
    def get_attr_dict():
        return {
            'name': None,
            'uniqueID': None,
            'relativePath': None,
            'fullPath': None,
            'creationDate': None,
            'sizeGB': None
        }

    # I/O
    @staticmethod
    def load_package():
        return pickle.load(open("Package.p", 'rb'))

    def save_package(self):
        pickle.dump(self, open("Package.p", 'wb'))

    # Setters
    def set_name(self, name):
        self.name = name

    def set_uniqueID(self, uniqueID):
        self.uniqueID = uniqueID

    def set_relativePath(self, relativePath):
        self.relativePath = relativePath

    def set_fullPath(self, fullPath):
        self.fullPath = fullPath

    def set_creationDate(self, creationDate):
        self.creationDate = creationDate

    def set_sizeGB(self, sizeGB):
        self.sizeGB = sizeGB

    # Getters
    def get_name(self):
        return self.name

    def get_uniqueID(self):
        return self.uniqueID

    def get_relativePath(self):
        return self.relativePath

    def get_fullPath(self):
        return self.fullPath

    def get_creationDate(self):
        return self.creationDate

    def get_sizeGB(self):
        return self.sizeGB


class DataPackage(Package):

    analysisPackages = []

    def __init__(self, attrDict):
        super().__init__(attrDict)

    def __del__(self):
        super().__del__()

    @staticmethod
    def get_attr_dict():
        concatenatedDict = {}
        parentDict = Package.get_attr_dict()
        childDict = {

        }
        concatenatedDict.update(parentDict)
        concatenatedDict.update(childDict)
        return concatenatedDict


class AnalysisPackage(Package):

    def __init__(self, attrDict):
        super().__init__(attrDict)

    def __del__(self):
        super().__del__()

    @staticmethod
    def get_attr_dict():
        concatenatedDict = {}
        parentDict = Package.get_attr_dict()
        childDict = {

        }
        concatenatedDict.update(parentDict)
        concatenatedDict.update(childDict)
        return concatenatedDict





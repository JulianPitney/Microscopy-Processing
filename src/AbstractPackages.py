import pickle
from pickle import UnpicklingError, PicklingError
from pathlib import Path


class Package(object):

    name = None
    uniqueID = None
    relativePath = None
    creationDate = None
    sizeGB = None

    def __init__(self, attrDict):

        self.set_name(attrDict['name'])
        self.set_uniqueID(attrDict['uniqueID'])
        self.set_relativePath(attrDict['relativePath'])
        self.set_creationDate(attrDict['creationDate'])
        self.set_sizeGB(attrDict['sizeGB'])

    def __del__(self):
        pass

    @staticmethod
    def get_empty_attr_dict():
        return {
            'name': None,
            'uniqueID': None,
            'relativePath': None,
            'creationDate': None,
            'sizeGB': None
        }

    def get_filled_attr_dict(self):

        return {
            'name': self.get_name(),
            'uniqueID': self.get_uniqueID(),
            'relativePath': self.get_relativePath(),
            'creationDate': self.get_creationDate(),
            'sizeGB': self.get_sizeGB()
        }

    # I/O
    @staticmethod
    def load_package(path):

        try:
            inputFile = open(path, 'rb')
            unpickledObj = pickle.load(inputFile)
            inputFile.close()
        except UnpicklingError:
            raise UnpicklingError("Pickle has failed to load a Package object from disk.")
        else:
            return unpickledObj

        return unpickledObj

    def save_package(self, path):

        saveSuccess = True

        try:
            outfile = open(path, 'wb')
            pickle.dump(self, outfile)
            outfile.close()
        except PicklingError:
            raise PicklingError("Pickle has failed to save a Package object to disk.")
            saveSuccess = False
        else:
            return saveSuccess

        return saveSuccess

    # Setters
    def set_name(self, name):
        self.name = name

    def set_uniqueID(self, uniqueID):
        self.uniqueID = uniqueID

    def set_relativePath(self, relativePath):
        self.relativePath = relativePath

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

    def get_creationDate(self):
        return self.creationDate

    def get_sizeGB(self):
        return self.sizeGB


class DataPackage(Package):

    def __init__(self, attrDict):
        super().__init__(attrDict)

    def __del__(self):
        super().__del__()

    @staticmethod
    def get_empty_attr_dict():
        concatenatedDict = {}
        parentDict = Package.get_empty_attr_dict()
        childDict = {

        }
        concatenatedDict.update(parentDict)
        concatenatedDict.update(childDict)
        return concatenatedDict

    def get_filled_attr_dict(self):

        concatenatedDict = {}
        parentDict = super().get_filled_attr_dict()
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
    def get_empty_attr_dict():
        concatenatedDict = {}
        parentDict = Package.get_empty_attr_dict()
        childDict = {

        }
        concatenatedDict.update(parentDict)
        concatenatedDict.update(childDict)
        return concatenatedDict

    def get_filled_attr_dict(self):

        concatenatedDict = {}
        parentDict = super().get_filled_attr_dict()
        childDict = {

        }
        concatenatedDict.update(parentDict)
        concatenatedDict.update(childDict)
        return concatenatedDict


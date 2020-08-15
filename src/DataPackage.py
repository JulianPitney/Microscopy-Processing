import pickle


class DataPackage(object):

    name = None
    uniqueID = None
    relativePath = None
    fullPath = None
    creationDate = None
    sizeGB = None

    def __init__(self, name, uniqueID, relativePath, fullPath, creationDate, sizeGB):

        self.set_name(name)
        self.set_uniqueID(uniqueID)
        self.set_relativePath(relativePath)
        self.set_fullPath(fullPath)
        self.set_creationDate(creationDate)
        self.set_sizeGB(sizeGB)

    def __del__(self):
        pass

    # I/O
    @staticmethod
    def load_package():
        return pickle.load(open("DataPackage.p", 'rb'))

    def save_package(self):
        pickle.dump(self, open("DataPackage.p", 'wb'))

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
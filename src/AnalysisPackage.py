import pickle


class AnalysisPackage(object):

    name = None
    uniqueID = None
    relativePath = None
    fullPath = None
    sizeGB = None
    startDate = None
    completionDate = None

    def __init__(self, name, uniqueID, relativePath, fullPath, sizeGB, startDate, completionDate):

        self.set_name(name)
        self.set_uniqueID(uniqueID)
        self.set_relativePath(relativePath)
        self.set_fullPath(fullPath)
        self.set_sizeGB(sizeGB)
        self.set_startDate(startDate)
        self.set_completionDate(completionDate)

    def __del__(self):
        pass

    # I/O
    @staticmethod
    def load_package():
        pass

    def save_package(self):
        pass

    # Setters
    def set_name(self, name):
        self.name = name

    def set_uniqueID(self, uniqueID):
        self.uniqueID = uniqueID

    def set_relativePath(self, relativePath):
        self.relativePath = relativePath

    def set_fullPath(self, fullPath):
        self.fullPath = fullPath

    def set_sizeGB(self, sizeGB):
        self.sizeGB = sizeGB

    def set_startDate(self, startDate):
        self.startDate = startDate

    def set_completionDate(self, completionDate):
        self.completionDate = completionDate

    # Getters
    def get_name(self):
        return self.name

    def get_uniqueID(self):
        return self.uniqueID

    def get_relativePath(self):
        return self.relativePath

    def get_fullPath(self):
        return self.fullPath

    def get_sizeGB(self):
        return self.sizeGB

    def get_startDate(self):
        return self.startDate

    def get_completionDate(self):
        return self.completionDate
class PackageError(Exception):
    """Exception raised when problem is detected with a Package object.

    Attributes:
        errorMsg -- Message describing the particular circumstances (Default to generic explanation)
    """

    def __init__(self, errorMsg="A problem was detected within a Package object."):
        self.errorMsg = errorMsg
        super().__init__(self.errorMsg)


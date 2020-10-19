
class MLOpsException(Exception):
    """Base MLOps exception class.
    All MLOps specific exceptions should subclass this class.
    """


class ConfigDoesNotExistException(MLOpsException):
    """Exception for missing config file
    """

class InvalidConfigurationFieldException(MLOpsException):
    def __init__(self):
        pass

    def __str__(self):
        return ""
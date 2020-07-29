from jinja2 import Environment, FileSystemLoader, PackageLoader
import os
import logging

logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)

PATH = os.path.dirname(__file__)
logger.info(PATH)

class Jinja2Environment:
    class __Jinja2Environment:
        def __init__(self, *args):
            self.val = args
            self.__path = './templates'#os.path.join(PATH, 'templates')
            logger.info(self.__path)
            self.env = Environment(
                autoescape=False,
                loader=PackageLoader('mlops_generator', 'templates'),#FileSystemLoader("mlops_generator/templates"),
                trim_blocks=False
            )

        def __str__(self):
            return repr(self) + self.val

    instance = None

    def __new__(cls): # __new__ always a classmethod
        if not Jinja2Environment.instance: 
            Jinja2Environment.instance = Jinja2Environment.__Jinja2Environment()
        return Jinja2Environment.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)

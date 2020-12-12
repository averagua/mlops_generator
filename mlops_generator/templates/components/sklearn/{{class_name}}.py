"""[summary]"""

from sklearn.base import {{estimator_type}}
from pandas import DataFrame, DataFrame

import logging

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.ERROR)

class {{class_name}}Estimator({{estimator_type}}):
    def __init__(self):
        pass

    def fit(self, X:DataFrame, y:DataFrame, *args, **kwargs):
        # Change by you ouwn implementation
        return self

    def predict(self, X:DataFrame, y:DataFrame=None):
        return self.estimator.predict(X.values)


def main(verbose:int=40):
    logging.basicConfig(level=verbose)
    X = None
    y = None
    estimator = {{class_name}}Estimator().fit(X, y)
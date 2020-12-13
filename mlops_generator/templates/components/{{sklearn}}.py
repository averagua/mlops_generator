"""
{{component_name}} Accessor Module
version {{version}} - {{date}}
company: {{company}}
"""

from sklearn.base import {{component_type}}
from pandas import DataFrame, DataFrame

import logging

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.ERROR)

class {{component_name}}({{component_type}}):
    def __init__(self):
        pass

    def fit(self, X:DataFrame, y:DataFrame, *args, **kwargs):
        # Change by you ouwn implementation
        return self
    {% if component_type == 'TransformerMixin' %}
    def transform(self, X:DataFrame, y:DataFrame=None):
        return
    {% else %}
    def predict(self, X:DataFrame, y:DataFrame=None):
        return
    {% endif %}


def main(verbose:int=40):
    logging.basicConfig(level=verbose)
    X = None
    y = None
    estimator = {{component_name}}().fit(X, y)
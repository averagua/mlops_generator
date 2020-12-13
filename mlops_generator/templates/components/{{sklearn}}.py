"""
{{component_name}} sklearn base Module
version {{version}} - {{creation_date}}
company: {{company}}
"""

from sklearn.base import {{component_type}}
from pandas import DataFrame, DataFrame
{% if click %}from click.core import Option, Command{% endif %}

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

{% if click %}
class {{component_name}}Commands(Command):
    def __init__(self, *args, **kwargs):
        """Commands options for {{ component_name }}."""
        super().__init__(*args, **kwargs)
        self.params.extend([
            self.option
        ])

    @property
    def option(self) -> Option:
        return Option(("--option",), type=str, help="First option for {{component_name}}")
{% endif %}

def main(verbose:int=40):
    logging.basicConfig(level=verbose)
    X = None
    y = None
    estimator = {{component_name}}().fit(X, y)
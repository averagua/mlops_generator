"""
{{component_name}} Accessor Module
version {{version}} - {{creation_date}}
company: {{company}}
"""

import pandas as pd

@pd.api.extensions.register_dataframe_accessor('{{pandas}}_accessor')
class {{component_name}}Accessor:
    """
   {{component_name}} Accessor class for extend pandas
    See: https://pandas.pydata.org/pandas-docs/stable/development/extending.html
    """
    def __init__(self, __obj):
        """
        __init__ Constructor for pandas DataFrame extension like dependency injection.
        Args:
            __obj (DataFrame): Dataframe in context
        """
        self.__obj = __obj

    def foo(self):
        """
        Extend here your own implementations
        Usage:
            # Define a pandas DataFrame
            df = pd.DataFrame(data, columns, indexes)
            result = df.{{pandas}}_accessor.foo()
        Raises:
            NotImplementedError: [description]
        """
        raise NotImplementedError('Method not implemented.')
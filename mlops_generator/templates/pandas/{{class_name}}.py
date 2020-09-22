"""
{{class_name}} Accessor Module
version {{version}} - {{date}}
Author: <AUTHOR>
"""

import pandas as pd

@pd.api.extensions.register_dataframe_accessor('{{accessor_name}}_accessor')
class {{class_name}}Accessor:
    """
   {{class_name}} Accessor class for extend pandas
    See: https://pandas.pydata.org/pandas-docs/stable/development/extending.html
    """
    def __init__(self, __obj):
        """
        __init__ Constructor for pandas DataFrame extension like dependency injection.
        Usage:
            # Define a pandas DataFrame
            df = pd.DataFrame(data, columns, indexes)
            result = df.{{accessor_name}}_accessor.foo()
        Args:
            __obj (DataFrame): Dataframe in context
        """
        self.__obj = __obj

    def foo(self):
        """
        foo Extend here your implementations
        Raises:
            NotImplementedError: [description]
        """
        raise NotImplementedError('Method not implemented.')
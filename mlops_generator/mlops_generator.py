"""Main module."""
import logging
from .base import Generator, runner

logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)

class PandasExtension(Generator):
    """
    PandasExtension Generator of source code for pandas extensions.

    [extended_summary]

    Args:
        Generator ([type]): [description]
    """

    def __init__(self, module_name):
        """
        __init__ .

        [extended_summary]

        Args:
            module_name ([type]): [description]
        """
        super().__init__(
            'pandas/extension.py',
            context = {
                'module_name': module_name,
                'module_name_lower': module_name.lower()
            }
        )

def pandas_extension(module_name, out_filename):
    """
    pandas_extension Function that run the generation of a pandas extension.

    [extended_summary]

    Args:
        module_name ([type]): [description]
        out_filename ([type]): [description]
    """

    runner(
        'pandas_extension.py', 
        out_filename,
        context = {
            'module_name': module_name,
            'module_name_lower': module_name.lower()
        },
        
    )


if __name__=='__main__':
    # Define the model type
    MODULE_TYPE = 'pandas'
    # Define the model name
    MODULE_NAME = 'Example'
    # Verify if the paths exists
    # Destination path
    module_path = './examples/pandas/'
    test_path = './tests'
    out_filename = '{}{}_accessor.py'.format(module_path, MODULE_NAME.lower())
    # gen = PandasExtension(MODULE_NAME).run(out_filename)
    pandas_extension(MODULE_NAME, out_filename)
import logging
from .render import Jinja2Environment
from datetime import date
import io

logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)

TEMPLATE_ENVIRONMENT = Jinja2Environment() 

class Generator:
    """
    Base class template generator for inherit it and create custom modules bases in python templates.
    """
    def __init__(self, template_filename, context):
        """
        __init__ Initialize the class given the template filename and context

        Args:
            template_filename (str): The filename of template, in _template directory. 
            context (Dict): Context that will be used render the python template in usefull code.
        """
        self.__env = TEMPLATE_ENVIRONMENT.env
        self.__template_filename = template_filename
        self.__template = None
        self.__context = context
        self.__add_version_context()
        self.__add_date_context()
        self.__file_content = None

    @property
    def template(self):
        """
        template Jinja template

        Returns:
            Generator: Self
        """
        return self.__template

    @property
    def accessor_name(self):
        return self.__accessor_name

    @property
    def context(self):
        return self.__context

    def __add_version_context(self):
        self.__context['version'] = '0.1.0'
    
    def __add_date_context(self):
        self.__context['date'] = date.today().strftime("%B %d, %Y")

    def generate(self):
        """
        generate Generate source code, that its render the file
        using the given context.

        Returns:
            jinja2.environment.Template: Jinja2 Template
        """
        logger.info(self.__template)
        logger.info(self.__context)
        self.__template = self.__env.get_template(self.__template_filename)
        self.__file_content = self.__template.render(self.__context)
        return self

    def save(self, out_filename):
        """
        save Save the rendered file in the given directory.

        Args:
            out_filename (string): The destination filename path
        """
        with io.open(out_filename, 'w', encoding='utf-8') as f:
            logger.info('Saving in {}'.format(out_filename))
            f.write(self.__file_content)
        return self

    def run(self, output_filename):
        self.generate().save(output_filename)
        return self

def runner(template_filename, output_filename, context):
    
    from cookiecutter.generate import generate_file
    gen = Generator(template_filename, context).run(output_filename)
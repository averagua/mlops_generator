from .render import Jinja2Environment
from .exceptions import ConfigDoesNotExistException
from cookiecutter.main import cookiecutter
from collections import OrderedDict
import logging
from datetime import date
import io
import os
from jinja2 import Environment, FileSystemLoader, PackageLoader
from jsonschema import validate
import json
import pathlib

logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)

class TYPES:
    def __init__(self):
        self.__PY = '.py'
        self.__YAML = '.yaml'

    @property
    def PY(self):
        return self.__PY

    @property
    def YAML(self):
        return self.__YAML


class Project:
    def __init__(self, config_file):
        # Should be absolute because run into the generated project (singleton)
        self.__config_path = config_file
        self.__schema = {
            "type": "object",
            "properties": {
                "project_name": {"type": "string"},
                "root": {"type": "string"},
                "pipelines": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string"},
                        "registered": {"type": "array"}
                    }
                },
                "components": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string"},
                        "registered": {"type": "array"}
                    }
                }
            },
            "required": ["project_name", "root"]
        }
        self.__configs = None
    
    def load_config(self):
        with open(self.__config_path, 'r') as f:
            self.__configs = json.load(f)
            validate(self.__configs, self.__schema)
            print(self.__configs)
            return self

    @property
    def configs(self):
        return self.__configs

    @property
    def schema(self):
        return self.__schema


    @property
    def root(self):
        return self.__configs['root']

    @property
    def component_path(self):
        comp_path = os.path.join(
            pathlib.Path().absolute(),
            self.__configs['project_name'].strip(),
            self.__configs['components']['path'].strip()
        )
        print(comp_path)
        return comp_path

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
        self.__env = Environment(
            autoescape=False,
            # FileSystemLoader("mlops_generator/templates"),
            loader=PackageLoader('mlops_generator', 'templates'),
            trim_blocks=False
        )

        self.__project = Project('./mlops-config.json').load_config()
        logger.info(self.__project.configs)

        self.__template_filename = template_filename
        self.__template = None
        self.__context = OrderedDict(context)
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
    def context(self):
        return self.__context

    def __add_version_context(self):
        self.__context['version'] = '0.1.0'

    def __add_date_context(self):
        self.__context['date'] = date.today().strftime("%B %d, %Y")

    def render_output_path(self, out_dir):
        if '/' in self.__template_filename:
            filename = self.__template_filename.split('/')[-1]
        else:
            filename = self.__template_filename
        out_filename = self.__env.from_string(filename).render(self.__context)
        return os.path.join(out_dir, out_filename)

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

    def save(self, out_dir):
        """
        save Save the rendered file in the given directory.

        Args:
            out_filename (string): The destination filename path
        """
        out_path = self.render_output_path(out_dir)
        print("Saving module in path {}".format(out_path))
        with io.open(out_path, 'w', encoding='utf-8') as f:
            logger.info('Saving in {}'.format(out_path))
            f.write(self.__file_content)
        return self

    def component(self, output_filename=None):
        """Method for generate a module
        Args:
            output_filename (str, optional): Output path for the module. Defaults to None.

        Returns:
            [type]: [description]
        """
        if out_dir is None:
            out_dir = self.__project.component_path
        self.generate().save(output_filename)
        return self


def pandas_extension(module_name, output_filename):
    """
    pandas_extension Function that run the generation of a pandas extension.

    [extended_summary]

    Args:
        module_name ([type]): [description]
        out_filename ([type]): [description]
    """
    context = {
            'class_name': module_name,
            'module_name_lower': module_name.lower()
        }
    Generator('pandas/{{class_name}}.py', context).component(output_filename)

def initialize(project_template):
    cookiecutter(project_template)

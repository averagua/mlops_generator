"""Main module."""
import logging
from .generator import Generator
from cookiecutter.main import cookiecutter
# from cookiecutter.config import get_config, get_user_config
# from cookiecutter.prompt import prompt_for_config
# from cookiecutter.generate import generate_context, apply_overwrites_to_context, generate_file, generate_files, is_copy_only_path
# from cookiecutter.environment import StrictEnvironment
# from collections import OrderedDict
# from jinja2 import Environment, FileSystemLoader, PackageLoader
# from cookiecutter.exceptions import (
#     OutputDirExistsException
# )

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

def pandas_extension(module_name, output_filename):
    """
    pandas_extension Function that run the generation of a pandas extension.

    [extended_summary]

    Args:
        module_name ([type]): [description]
        out_filename ([type]): [description]
    """
    context = {
            'module_name': module_name,
            'module_name_lower': module_name.lower()
        }
    Generator('pandas/pandas_extension.py', context).module(output_filename)

def initialize():
    cookiecutter("https://github.com/averagua/mlops-kubeflow")

"""
from cookiecutter.generate import render_and_create_dir
import os
def test_cookiebad():
    # cookiecutter('./mlops_generator/templates')
    # get_config("./covid/mlops-config.json")
    root = "./mlops"
    template = "pandas/pandas_extension.py"
    extra_context = {
        "cookiecutter": {
            "module_name": "PDTest",
            "module_name_lower": "PDtest",
            "version": "1.0.0",
            "date": "today",
            "pandas": "PDTest"
            }
        }
    promt_conf = True

    context = OrderedDict(extra_context)
    context['cookiecutter'] = prompt_for_config(context, promt_conf)
    # context['cookiecutter']['_template'] = template
    env = StrictEnvironment(context=context, keep_trailing_newline=True)
    env.loader = PackageLoader('mlops_generator', 'templates') # FileSystemLoader('./')
    unrendered_dir = os.path.split(template)[0]
    infile = os.path.normpath(os.path.join(root, unrendered_dir))
    print(infile)
    try:
        project_dir, output_directory_created = render_and_create_dir(
            template, context, root, env, False
        )
        print(project_dir, output_directory_created)
    except OutputDirExistsException:
        logger.debug('Directory already exists, continue')
    generate_file(
        root,
        template,
        context['cookiecutter'],
        env
    )

    return True

"""
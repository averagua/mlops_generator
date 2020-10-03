from project import ProjectConfigsSchema, ArchitectureSchema, SetupSchema
from prompt_adapter import PromptAdapter
from persistence import PresentationLayer
from datetime import datetime
import logging
import importlib
import json 

logger = logging.getLogger(__package__)
logging.basicConfig(level=logging.INFO)

class Interface:
    """
    Implement functionalities for project administration.

    Supported:
        - initialize project
        - add pluging
        - generate
        - 
    """
    
    def __init__(self, config_file='mlops_configs.json', package='project'):
        self.__context = None
        self.__loader = importlib.import_module(package)
    
    def get_schema(self, schema_name):
        return getattr(self.__loader, schema_name, None)

    @property
    def loader(self):
        return self.__loader

    def initialize(self, cwd, tests=False, setup=True, *args, **kwargs):
        try:
            prompt = PromptAdapter(self.loader)
            project = prompt.prompt_schema('ProjectConfigsSchema', context={
                'name':  'covid2',
                'package_name': 'covid',
                'email': 'veragua.alb@gmail.com',
                'description': 'description',
                'license_type': 'MIT',
                'author': 'Alejandro Veragua',
                'version': '1.0.0',
                'creation_date': datetime.today().strftime('%Y-%m-%d %H:%M')
            }, serialize=True)
            presentation_layer = PresentationLayer(self.loader, root=project.name)
            presentation_layer.push_job('ProjectConfigsSchema')
            # Prompt setup schema, set the object in the project, change the current schema in presentation layer and push its templates.
            if setup:
                setup = prompt.prompt_schema('SetupSchema', context={'entrypoint': 'setup.py'}, serialize=True)
                presentation_layer.push_job('SetupSchema')
            presentation_layer.push_job('ArchitectureSchema')
            presentation_layer.push_job('ComponentSchema')
            presentation_layer.push_job('PipelineSchema')
            presentation_layer.schema = 'ProjectConfigsSchema'
            presentation_layer.render(project)
        except Exception as e:
            logger.exception(e)
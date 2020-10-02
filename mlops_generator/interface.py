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
    __PROJECT_SCHEMA = ProjectConfigsSchema()
    __ARCHITECTURE_SCHEMA = ArchitectureSchema()
    __SETUP_SCHEMA = SetupSchema()
    
    def __init__(self, config_file='mlops_configs.json', package='project'):
        self.__context = None
        self.__loader = importlib.import_module(package)

    @property
    def loader(self):
        return self.__loader

    def initialize(self, cwd, tests=False, setup=True, *args, **kwargs):
        try:
            creation_date = datetime.today()
            prompt = PromptAdapter(self.loader)
            project = prompt.prompt_schema('ProjectConfigsSchema', context={
                "name":  "covid2",
                "package_name": "covid",
                "email": "veragua.alb@gmail.com",
                "description": "description",
                "license_type": "MIT",
                "author": "Alejandro Veragua",
                "version": "1.0.0",
            }, serialize=True)
            presentation_layer = PresentationLayer(self.loader, root=project.name)
            presentation_layer.push_template('ProjectConfigsSchema')
            setup = prompt.prompt_schema('SetupSchema', serialize=True)
            if setup:
                project.setup = setup
                presentation_layer.push_template('SetupSchema')
            logger.info(presentation_layer.templates_queue.popleft())
            # logger.info(json.dumps(setup_dict))
            # Finally
            # project = cls.__PROJECT_SCHEMA.load(project_dict)
            # architecture = cls.__ARCHITECTURE_SCHEMA.load({})
            # logger.info(cls.__PROJECT_SCHEMA.dump(project))
        except Exception as e:
            logger.exception(e)
        # ComponentSchema.from_promt({'name': None})
        # Initialize from prompt user input
        # context = cls.__PROJECT_SCHEMA.from_promt(*args, **kwargs)
        # Set current directory
        # Project = cls.__PROJECT_SCHEMA.load(context)  # .render()
        # Enqueque creation of main project directories, an change current working directory (internal)
        # for define and persists paths
        # Enqueue project directory
        # Project.put_dir(Project.project)
        # BaseModel.chdir(Project.project)
        # Project.put_dir(Project.package_name)
        # Project.put_dir('deploy')
        # Project.put_dir('tests')
        # Project.put_dir('references')
        # Project.put_dir('notebooks')
        # Render the generated templates
        #Project.render()
        # Persists files
        # Project.persist()
from project import ProjectConfigsSchema
from prompt_adapter import PromptAdapter
from datetime import datetime
import logging


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
    
    def __init__(self, config_file='mlops_configs.json'):
        self.__context = None

    @classmethod
    def initialize(cls, cwd, tests=False, licence=False, setup=True, *args, **kwargs):
        try:
            creation_date = datetime.today()
            cls.__PROJECT_SCHEMA.cwd = cwd
            prompt_adapter = PromptAdapter(cls.__PROJECT_SCHEMA)
            project = prompt_adapter.gen_prompts(context={
                "project": "covid",
                "package_name": "covid",
                "author": "Alejandro Veragua",
                "email": "veragua.alb@gmail.com",
                "description": "Project generated from MLOPs cli"
            })
            logger.info(project)
        except Exception as e:
            logger.exception(e)
        # ComponentSchema.from_promt({'name': None})
        # Initialize from prompt user input
        """
        {
            "project":  "covid2",
            "package_name": "covid",
            "email": "veragua.alb@gmail.com",
            "description": "description",
            "license_type": "MIT",
            "creation_date": creation_date.strftime("%Y-%m-%d"),
            "author": "Alejandro Veragua",
            "version": "1.0.0",
        }
        """
        logger.info(args)
        logger.info(kwargs)

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
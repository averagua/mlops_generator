import json
from datetime import datetime
from pathlib import Path
from typing import NoReturn, Dict, List

from mlops_generator.prompt import PromptAdapter
from mlops_generator.persistence import PresentationLayer

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Interface:
    """Interface for project cli administration."""

    def __init__(
        self,
        config_file: str = "mlops_config.json",
        package: str = "mlops_generator.project",
    ):
        self.__context = None
        self.prompt = PromptAdapter()
        self.player = None
        self.PROJECT_SCHEMA = "ProjectSchema"

    def handler(self, option, project):
        if option == "deploy":
            project.architecture.deploy = self.prompt_and_push(
                "DeploySchema",
            )
        elif option == "docker":
            project.architecture.docker = self.prompt_and_push(
                "DockerfileSchema", serialize=True
            )
        elif option == "setup":
            project.setup = self.prompt_and_push(
                "SetupSchema",
                extra_context={"entry_point": project.project_name},
                serialize=True,
            )
        elif option == "tests":
            project.tests = self.prompt_and_push(
                "TestSChema",
                extra_context={},
                serialize=True,
            )
            logger.info(project.tests)
        else:
            logger.warning("Handler not implemented {}".format(option))
        return project

    def iter_options(self, kwargs: Dict, project):
        """Iter dictionary options throw handlers for update project object.

        Args:
            kwargs (dict):
            project (project.ProjectConfigs): Project config object

        Returns:
            [type]: [description]
        """
        # Filter true options
        options = self.filter_options(kwargs)
        for opt in options:
            project = self.handler(option=opt, project=project)
        return project

    def filter_options(self, kargs: Dict) -> List[str]:
        """Filter key arguments options if was given by user.

        Args:
            kargs (dict): [description]

        Returns:
            [type]: [description]
        """
        kargs = [k for k, v in kargs.items() if v]
        return kargs

    def prompt_and_push(
        self,
        schema_name: str,
        extra_context: dict = {},
        serialize: bool = False,
    ):
        """Routine for prompt schema and push the template jobs to layer.

        Args:
            schema_name (str): Schema name to promp
            extra_context (dict, optional): Extra context for not ask it to user. Defaults to {}.
            serialize (bool, optional): Serialize got context to object defined for schema. Defaults to False.

        Returns:
            base.BaseModel: Base model for schema
        """
        obj = self.prompt.prompt_schema(
            schema_name, context=extra_context, serialize=serialize
        )
        self.player.push_job(schema_name)
        return obj

    def load_project(self, cwd):
        self.player = PresentationLayer(cwd=cwd)
        # Load project objet from config file
        project = self.player.from_config(schema_name=self.PROJECT_SCHEMA)
        # Serialize project object to dictionart
        # context = project_schema.dump(project)
        return project

    def initialize(self, cwd: Path, *args, **kwargs) -> NoReturn:
        """Initialize project based on MLOps capabilities

        Args:
            cwd (Path): Current working directory

        Raises:
            FileExistsError: Project to initialize already exists
        """
        # Ask to user project definitions
        project = self.prompt.prompt_schema(
            self.PROJECT_SCHEMA, context={}, serialize=True
        )
        # Set cwd to choosed project
        cwd = cwd / project.project_name
        if cwd.exists():
            raise FileExistsError("Project already exists!")
        # Initialize presentation layer
        self.player = PresentationLayer(cwd=cwd)
        # Push project templates and directories to presentation layer
        project_schema = self.player.push_job(self.PROJECT_SCHEMA, return_schema=True)
        self.iter_options(kwargs, project)
        if project.click:
            self.player.push_job("ClickSchema")
        # Serialize project object to dictionary
        context = project_schema.dump(project)
        # Log ig
        logger.info(json.dumps(context, indent=2))
        # Renderize queued templates using got context from user
        self.player.render(context, persist=True)

    def add(self, cwd: Path, *args, **kwargs) -> NoReturn:
        """Add new component to project

        Args:
            cwd (Path): Current working directory
        """
        # Initialice presentation layer in current working directory
        self.player = PresentationLayer(cwd=cwd)
        # Load project objet from config file
        project = self.player.from_config(schema_name=self.PROJECT_SCHEMA)
        project_schema = self.player.create_schema(self.PROJECT_SCHEMA)
        project = self.iter_options(kwargs, project)
        # Serialize project object to dictionart
        context = project_schema.dump(project)
        # Log ig
        logger.info(json.dumps(context, indent=2))
        # Renderize queued templates using got context from user
        self.player.render(context, persist=True)

    @property
    def component_mapper(self):
        return {
            "sklearn": "SklearnSchema",
            "pandas": "PandasSchema",
            "kubeflow-component": "KFPContainerOpSchema",
            "kubeflow-pipeline": "PipelineSchema",
            "artifacts": "ArtifactsSchema",
            "jupyter-notebook": "NotebooksSchema"
        }

    def component(self, cwd: Path, module: str, *args, **kwargs):
        project = self.load_project(cwd)
        project_schema = self.player.create_schema(self.PROJECT_SCHEMA)
        try:
            schema_name = self.component_mapper[module]
            obj = self.prompt.prompt_schema(
                schema_name=schema_name, context={}, serialize=True
            )
            schema = self.player.push_job(schema_name, return_schema=True)
            context = schema.dump(obj)
            context.update(project_schema.dump(project))
            logger.info(json.dumps(context, indent=2))
            self.player.render(context, persist=False)
        except KeyError as e:
            logger.error(e)

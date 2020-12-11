import json
import importlib
from datetime import datetime
from pathlib import Path

from mlops_generator.project import (
    ProjectConfigsSchema,
    ArchitectureSchema,
    SetupSchema,
)
from mlops_generator.prompt_adapter import PromptAdapter
from mlops_generator.persistence import PresentationLayer

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

    def __init__(
        self,
        config_file: str = "mlops_config.json",
        package: str = "mlops_generator.project",
    ):
        self.__context = None

    def initialize(
        self,
        cwd: Path,
        setup: bool,
        tests: bool,
        dockerfile: bool,
        cloudbuild: bool,
        src: str = "src",
        *args,
        **kwargs
    ):
        try:
            prompt = PromptAdapter()
            context = {
                "project_name": "example_project",
                "package_name": "example_package",
                "email": "veragua.alb@gmail.com",
                "description": "description",
                "license_type": "MIT",
                "author": "Alejandro Veragua",
                "version": "1.0.0",
                "creation_date": datetime.today().strftime("%Y-%m-%d %H:%M"),
            }
            # context = {"creation_date": datetime.today().strftime("%Y-%m-%d %H:%M")}
            project = prompt.prompt_schema(
                "ProjectConfigsSchema", context=context, serialize=True
            )
            cwd = cwd / project.project_name
            presentation_layer = PresentationLayer(cwd=cwd)
            project_schema = presentation_layer.push_job(
                "ProjectConfigsSchema", return_schema=True
            )
            # # Prompt setup schema, set the object in the project, change the current schema in presentation layer and push its templates.
            if setup:
                # Prompt setup questions
                setup = prompt.prompt_schema(
                    "SetupSchema",
                    context={"entry_point": project.project_name},
                    serialize=True,
                )
                # Add setup to project definition
                project.setup = setup
                # Push templates and directories from stup schema
                presentation_layer.push_job("SetupSchema")
            if dockerfile:
                # prompt.prompt_schema(
                #    "DockerfileSchema", context={"project_name": project.project_name}
                # )
                presentation_layer.push_job("DockerfileSchema")

            if cloudbuild:
                prompt.prompt_schema(
                    "CloudbuildSchema", context={"project_name": project.project_name}
                )
                presentation_layer.push_job("CloudbuildSchema")
            logger.info(project)
            context = project_schema.dump(project)
            context = presentation_layer.render(context, persist=True)
            # logger.info(json.dumps(context))

        except Exception as e:
            logger.exception(e)

    def add(
        self, cwd: Path, setup: bool, tests: bool, dockerfile: bool, *args, **kwargs
    ):
        PresentationLayer.from_config(cwd)

    def prevent(self, path: Path):
        if path.exists():
            raise FileExistsError("File {} already exists".format(path))

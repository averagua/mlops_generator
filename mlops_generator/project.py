# -*- coding: utf-8 -*-
from pprint import pformat
import os
import sys

from marshmallow import fields, post_load, utils, missing, validate, post_dump, pre_load

import logging

from datetime import datetime

from mlops_generator.base import BaseModel, BaseSchema

logger = logging.getLogger(__package__)
logging.basicConfig(level=logging.INFO)


class PipelineModel(BaseModel):
    def __init__(self, name):
        self.name = name


class PipelineSchema(BaseSchema):
    __model__ = PipelineModel
    name = fields.Str(description="Pipeline's name")

    class Meta:
        templates = ["__init__.py"]
        path = "src/{{package_name}}/pipelines"


class ComponentModel(BaseModel):
    def __init__(self, component_name:str):
        self.component_name = component_name
        self.component_classname = component_name[0].upper()


class ComponentSchema(BaseSchema):
    __model__ = ComponentModel
    # name = fields.Str(description="Component's name", required=True)

    class Meta:
        templates = ["__init__.py", "components/simple.py"]
        path = "src/{{package_name}}"


class Notebooks(BaseModel):
    pass


class NotebooksSchema(BaseSchema):
    __model__ = Notebooks


class SetupConfig(BaseModel):
    def __init__(self, entry_point, install):
        self.install = install
        self.entry_point = entry_point


class SetupSchema(BaseSchema):
    install = fields.Str(
        required=True, description="Install filename", default="setup.py"
    )
    entry_point = fields.Str(
        required=True, description="Entrypoint command line interface"
    )

    __model__ = SetupConfig

    class Meta:
        templates = ["setup.py"]


class TestsModel(BaseModel):
    def __init__(self, framework):
        self.framework = framework


class TestSChema(BaseSchema):
    __model__ = TestsModel
    framework = fields.Str(
        required=True,
        description="Framework for run test, ML/AI tests included",
        default="pytest",
    )


class DockerfileModel(BaseModel):
    def __init__(self, project_name, registry):
        self.project_name = project_name
        self.registry = registry


class DockerfileSchema(BaseSchema):
    project_name = fields.Str(required=True, description="Project Name")
    registry = fields.Str(
        required=True, description="Docker registry url", default="gcr.io"
    )
    __model__ = DockerfileModel

    class Meta:
        templates = ["Dockerfile", ".dockerignore"]


class CloudbuildModel(BaseModel):
    def __init__(self, project_name, platform):
        self.project_name = project_name
        self.framework = 'gcp'


class CloudbuildSchema(BaseSchema):
    project_name = fields.Str(required=True, description="Project Name")
    __model__ = CloudbuildModel

    class Meta:
        templates = ["cloudbuild.yaml"]


class Architecture(BaseSchema):
    def __init__(
        self,
        components: list = [],
        pipelines: list = [],
        docker: dict = {},
        cloudbuild: dict = {},
    ):
        self.components = components
        self.pipelines = pipelines
        self.docker = docker
        self.cloudbuild = cloudbuild


class ArchitectureSchema(BaseSchema):
    __model__ = Architecture
    components = fields.Nested(ComponentSchema, many=True, missing=[])
    pipelines = fields.Nested(PipelineSchema, many=True, missing=[])
    docker = fields.Nested(DockerfileSchema, missing={})
    cloudbuild = fields.Nested(CloudbuildSchema, missing={})

    class Meta:
        path = "src/{{package_name}}"
        templates = ["__init__.py"]


class ProjectConfigs(BaseModel):
    def __init__(
        self,
        project_name,
        author,
        email,
        description,
        package_name,
        creation_date,
        license_type,
        version,
        architecture,
        python_interpreter,
        setup=None,
        deploy=None,
        tests=None,
    ):
        # Serializable data
        self.project_name = project_name
        self.author = author
        self.email = email
        self.package_name = package_name
        self.python_interpreter = python_interpreter
        self.description = description
        self.license_type = license_type
        self.deploy = deploy
        self.creation_date = creation_date
        self.version = version
        self.setup = setup
        self.tests = tests
        self.architecture = architecture


class ProjectConfigsSchema(BaseSchema):
    # 1.- Config declaration
    project_name = fields.Str(required=True, description="Project Name")
    package_name = fields.Str(required=True, description="Pypi Package name")
    author = fields.Str(required=True, description="Author name")
    email = fields.Email(required=True, description="Contact email")
    description = fields.Str(
        required=True,
        description="Project description",
        validate=validate.Length(max=280),
    )
    creation_date = fields.DateTime(
        format=BaseSchema.format_date, default=BaseSchema.today()
    )
    version = fields.Str(default="1.0.0", required=True, description="Package version")
    # default="No license file",
    license_type = fields.Str(
        validate=validate.OneOf(["MIT", "BSD-3-Clause", "No license file"]),
        required=True,
        default="No license file",
        description="Licence type",
    )

    architecture = fields.Nested(
        ArchitectureSchema,
        description="MLOps architecture project definition",
        missing=Architecture(),
    )
    setup = fields.Nested(SetupSchema, default=None, description="Setup configurations")
    deploy = fields.Nested(
        CloudbuildSchema, default=None, description="CI pipeline configurations"
    )
    tests = fields.Nested(TestSChema, default=None, description="Testing framework")
    python_interpreter = fields.Str(
        description="Python interpreter", missing="python3", default="python3"
    )
    # 2.- Define the object to deserialize

    __model__ = ProjectConfigs
    # 3.- Define custom templates and directories
    class Meta:
        templates = [
            "LICENSE",
            ".gitignore",
            "requirements.txt",
            "Readme.md",
        ]
        default_dirs = [
            "src/{{package_name}}",
            "tests/src",
            "notebooks",
            "references",
        ]

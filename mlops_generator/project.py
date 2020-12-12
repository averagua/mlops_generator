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


class SklearnModel(BaseModel):
    def __init__(self, class_name, estimator_type):
        self.class_name = class_name
        self.estimator_type = estimator_type


class SklearnSchema(BaseSchema):
    __model__ = SklearnModel
    class_name = fields.Str(description="Component class name", required=True)
    estimator_type = fields.Str(
        description="Sklearn base type",
        required=True,
        validate=validate.OneOf(
            [
                "BaseEstimator",
                "RegressorMixin",
                "TransformerMixin",
                "ClassifierMixin",
                "ClusterMixin",
                "DensityMixin"
            ]
        ),
    )

    class Meta:
        templates = ["components/sklearn/{{class_name}}.py"]
        path = "src/{{package_name}}"


class ComponentModel(BaseModel):
    def __init__(self, component_name: str):
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
        templates = ["setup.py", "setup.cfg"]


class TestsModel(BaseModel):
    def __init__(self, framework):
        self.framework = framework


class TestSChema(BaseSchema):
    __model__ = TestsModel
    framework = fields.Str(
        description="Framework for run test",
        missing=None,
    )


class DockerfileModel(BaseModel):
    def __init__(self, registry):
        self.registry = registry


class DockerfileSchema(BaseSchema):
    registry = fields.Str(
        required=True,
        description="Docker registry url",
        validate=validate.OneOf(["gcr.io"]),
    )
    __model__ = DockerfileModel

    class Meta:
        templates = ["Dockerfile", ".dockerignore"]


class DeployModel(BaseModel):
    def __init__(self, platform):
        self.platform = platform


class DeploySchema(BaseSchema):
    platform = fields.Str(
        required=True,
        description="CI pipeline platform",
        validate=validate.OneOf(["GCP"]),
    )

    __model__ = DeployModel

    class Meta:
        templates = ["cloudbuild.yaml"]


class Architecture(BaseSchema):
    def __init__(
        self,
        docker: dict = None,
        deploy: dict = None,
        components: list = None,
        pipelines: list = None,
    ):
        self.components = components
        self.pipelines = pipelines
        self.docker = docker
        self.deploy = deploy


class ArchitectureSchema(BaseSchema):
    __model__ = Architecture
    components = fields.Nested(ComponentSchema, many=True, missing=None)
    pipelines = fields.Nested(PipelineSchema, many=True, missing=None)
    docker = fields.Nested(DockerfileSchema, missing=None, many=False, default=None)
    deploy = fields.Nested(DeploySchema, many=False, default=None, missing=None)

    class Meta:
        path = "src/{{package_name}}"
        templates = ["__init__.py"]


class ProjectConfigs(BaseModel):
    def __init__(
        self,
        project_name,
        company,
        email,
        description,
        package_name,
        creation_date,
        license_type,
        version,
        architecture,
        python_interpreter,
        setup,
        tests,
    ):
        # Serializable data
        self.project_name = project_name
        self.company = company
        self.email = email
        self.package_name = package_name
        self.python_interpreter = python_interpreter
        self.description = description
        self.license_type = license_type
        self.creation_date = creation_date
        self.version = version
        self.setup = setup
        self.tests = tests
        self.architecture = architecture


class ProjectSchema(BaseSchema):
    # 1.- Config declaration
    project_name = fields.Str(
        required=True, description="Project Name", default="example_project"
    )
    package_name = fields.Str(
        required=True, description="Pypi Package name", default="package_name"
    )
    company = fields.Str(required=True, description="Company name", default="company")
    email = fields.Email(
        required=True, description="Contact email", default="contact@company.org"
    )
    description = fields.Str(
        required=True,
        description="Project description, max. 200",
        validate=validate.Length(max=280),
        default="Project description",
    )
    creation_date = fields.DateTime(
        format=BaseSchema.format_date,
        missing=BaseSchema.today(),
        default=BaseSchema.today(),
    )
    version = fields.Str(default="1.0.0", required=True, description="Package version")
    # default="No license file",
    license_type = fields.Str(
        validate=validate.OneOf(["MIT", "BSD-3-Clause", "No license file"]),
        required=True,
        default="No license file",
        description="Licence type",
    )
    python_interpreter = fields.Str(
        required=True,
        description="Python interpreter",
        default="python3",
        validate=validate.OneOf(["python3"]),
    )
    setup = fields.Nested(SetupSchema, description="Setup configurations", missing=None)

    architecture = fields.Nested(
        ArchitectureSchema,
        description="MLOps architecture project definition",
        default=None,
        missing=Architecture(),
    )
    tests = fields.Nested(
        TestSChema, missing=None, default=None, description="Testing framework"
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
            "Makefile",
        ]
        default_dirs = [
            "src/{{package_name}}",
            "tests/src",
            "notebooks",
            "references",
        ]

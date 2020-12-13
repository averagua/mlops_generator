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
    def __init__(self, pipeline_name: str, experiment_name: str):
        self.pipeline_name = pipeline_name
        self.experiment_name = experiment_name
        self.pipeline = pipeline_name.lower()


class PipelineSchema(BaseSchema):
    __model__ = PipelineModel
    pipeline_name = fields.Str(
        description="Pipeline name",
        required=True,
        default="pipeline",
    )
    experiment_name = fields.Str(
        description="Experiment name",
        required=True,
        default="pipeline_experiment",
    )

    pipeline = fields.Str()

    class Meta:
        templates = ["components/{{pipeline}}.py"]
        path = "src/{{project_name}}"


class ComponentModel(BaseModel):
    def __init__(self, component_name: str, component_type: str):
        self.component_name = "".join(
            map(lambda s: s.strip().capitalize(), component_name.split("_"))
        )

        self.component_type = component_type


class PandasModel(ComponentModel):
    def __init__(self, component_name, component_type):
        super(PandasModel, self).__init__(
            component_name=component_name, component_type=component_type
        )
        self.pandas = component_name.lower()


class PandasSchema(BaseSchema):
    __model__ = PandasModel
    component_name = fields.Str(
        description="Component class name. Ex. Extension result in extension.py.",
        required=True,
    )
    component_type = fields.Str(default="pandas_extension", missing="pandas_extension")
    pandas = fields.Str()

    class Meta:
        templates = ["components/{{pandas}}.py"]
        path = "src/{{project_name}}"


class SklearnModel(ComponentModel):
    def __init__(self, component_name, component_type, *args, **kwargs):
        super(SklearnModel, self).__init__(
            component_name=component_name,
            component_type=component_type,
            *args,
            **kwargs
        )
        self.sklearn = component_name.lower()


class SklearnSchema(BaseSchema):
    __model__ = SklearnModel
    component_name = fields.Str(
        description="Component class name. Ex. Trainner.", required=True
    )
    sklearn = fields.Str()
    component_type = fields.Str(
        description="Sklearn base type",
        required=True,
        validate=validate.OneOf(
            [
                "BaseEstimator",
                "RegressorMixin",
                "TransformerMixin",
                "ClassifierMixin",
                "ClusterMixin",
                "DensityMixin",
            ]
        ),
    )

    class Meta:
        templates = ["components/{{sklearn}}.py"]
        path = "src/{{project_name}}"


class KFPContainerOpModel(ComponentModel):
    def __init__(
        self,
        component_name: str,
        component_type: str,
        ui_metadata: bool,
        tmp_data: bool,
    ):
        super(KFPContainerOpModel, self).__init__(
            component_name=component_name, component_type=component_type
        )
        self.kfp_cop = component_name.lower()
        self.ui_metadata = ui_metadata
        self.tmp_data = tmp_data


class KFPContainerOpSchema(BaseSchema):
    __model__ = KFPContainerOpModel
    component_name = fields.Str(
        description="Kubeflow Component filename. Ex. trainner_component result in TrainnerComponent",
        required=True,
    )
    component_type = fields.Str(
        default="kfp.dsl.ContainerOp", missing="kfp.dsl.ContainerOp"
    )
    ui_metadata = fields.Bool(
        default=True,
        description="Add UI metadata to component definition.",
        required=True,
    )
    tmp_data = fields.Str(
        default="/tmp_data.json",
        description="Add temporal data to component definition.",
        required=True,
    )
    kfp_cop = fields.Str()

    class Meta:
        templates = ["components/{{kfp_cop}}.py"]
        path = "src/{{project_name}}"


class ComponentSchema(BaseSchema):
    __model__ = ComponentModel
    # name = fields.Str(description="Component's name", required=True)

    class Meta:
        templates = ["__init__.py", "components/simple.py"]
        path = "src/{{project_name}}"


class Notebooks(BaseModel):
    def __init__(self, jupyter: str):
        self.jupyter = jupyter.lower()


class NotebooksSchema(BaseSchema):
    __model__ = Notebooks
    jupyter = fields.Str(description="jupyter notebook to add", required=True)

    class Meta:
        templates = ["components/{{jupyter}}.ipynb"]
        path = "notebooks"


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
        templates = [
            "setup.py",
            "setup.cfg",
            "requirements.txt",
            "Makefile",
        ]


class TestsModel(BaseModel):
    def __init__(self, framework: str):
        self.framework = framework


class TestSChema(BaseSchema):
    __model__ = TestsModel
    framework = fields.Str(
        description="Framework for run test",
        validate=validate.OneOf(["pytest"]),
        default="pytest",
        required=True,
    )

    class Meta:
        templates = ["test_hello.py"]
        path = "tests/src"
        default_dirs = [
            "tests/src",
        ]


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


class ArtifactsModel(BaseModel):
    def __init__(self):
        pass


class ArtifactsSchema(BaseSchema):
    __model__ = ArtifactsModel

    class Meta:
        path = "src/{{project_name}}"
        templates = [
            "components/base.py",
            "components/temporal.py",
            "components/visualization.py",
        ]


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
        path = "src/{{project_name}}"


class ClickModel(BaseModel):
    def __init__(self):
        pass


class ClickSchema(BaseSchema):
    __model__ = ClickModel

    class Meta:
        path = "src/{{project_name}}"
        templates = ["__init__.py", "cli.py"]


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
        click,
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
        self.click = click
        self.tests = tests
        self.architecture = architecture


class ProjectSchema(BaseSchema):
    # 1.- Config declaration
    project_name = fields.Str(
        required=True,
        description="Project Name",
        default="example_project",
    )
    package_name = fields.Str(
        required=True, description="Pypi Package name", default="package_name"
    )
    company = fields.Str(
        required=True,
        description="Company name",
        default="company",
    )
    email = fields.Email(
        required=True,
        description="Contact email",
        default="contact@company.org",
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
    version = fields.Str(
        default="1.0.0",
        required=True,
        description="Package version",
    )
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
    setup = fields.Nested(
        SetupSchema,
        description="Setup configurations",
        missing=None,
    )
    click = fields.Bool(
        description="Add click to project",
        default=True,
        required=True,
    )
    architecture = fields.Nested(
        ArchitectureSchema,
        description="MLOps architecture project definition",
        default=None,
        missing=Architecture(),
    )
    tests = fields.Nested(
        TestSChema,
        description="Testing framework",
        missing=None,
    )
    # 2.- Define the object to deserialize

    __model__ = ProjectConfigs
    # 3.- Define custom templates and directories
    class Meta:
        templates = [
            "LICENSE",
            ".gitignore",
            "Readme.md",
        ]
        default_dirs = [
            "src/{{project_name}}",
            "notebooks",
            "references",
        ]

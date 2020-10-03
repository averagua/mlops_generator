# -*- coding: utf-8 -*-
from pprint import pformat
import os
import sys

from marshmallow import (
    fields,
    post_load,
    utils,
    missing,
    validate,
    post_dump,
    pre_load
)

import logging

from datetime import datetime

from base import BaseModel, BaseSchema
from trigger import ChangeTrigger

logger = logging.getLogger(__package__)
logging.basicConfig(level=logging.INFO)


class PipelineModel(BaseModel):
    def __init__(self, name):
        self.name = name

class PipelineSchema(BaseSchema):
    __model__ = PipelineModel
    name = fields.Str(description="Pipeline's name")

    class Meta:
        templates = ['__init__.py']
        parent_dir = '{{package_name}}/pipelines'


class ComponentModel(BaseModel):
    def __init__(self):
        # self.name = name
        pass

class ComponentSchema(BaseSchema):
    __model__ = ComponentModel
    # name = fields.Str(description="Component's name", required=True)

    class Meta:
        templates = ['__init__.py']
        parent_dir = '{{package_name}}/components'


class Architecture(ComponentModel, PipelineModel):
    def __init__(self, components=[], pipelines=[]):
        self.components = components
        self.pipelines = pipelines

class ArchitectureSchema(BaseSchema):
    __model__ = Architecture
    components = fields.Nested(ComponentSchema, many=True, missing=[])
    pipelines = fields.Nested(PipelineSchema, many=True, missing=[])
    class Meta:
        parent_dir = '{{package_name}}'
        templates = ['__init__.py']
        default_dirs = ['components', 'pipelines']



class DeployConfig:
    def __init__(self, framework):
        self.framework = framework


class DeploySchema(BaseSchema):
    __model__ = DeployConfig
    framework = fields.Str(
        required=True, description="Framework for CI/CD", default="GCB")

class Notebooks(BaseModel):
    pass


class NotebooksSchema(BaseSchema):
    __model__ = Notebooks

class SetupConfig(BaseModel):
    def __init__(self, entrypoint):
        self.entrypoint = entrypoint

class TestsModel(BaseModel):
    def __init__(self, framework):
        self.framework = framework


class TestSChema(BaseSchema):
    __model__ = TestsModel
    framework = fields.Str(
        required=True, description="Framework for run test, ML/AI tests included", default="pytest")

class SetupSchema(BaseSchema):
    entrypoint = fields.Str(
        required=True, description="Entrypoint for setup", default="setup.py")

    __model__ = SetupConfig
    class Meta:
        templates = ['setup.py']

class ProjectConfigs(BaseModel):
    def __init__(self, name, author, email, description, package_name, creation_date, license_type, version, architecture, setup=None, deploy=None, tests=None):
        # Serializable data
        self.name = name
        self.author = author
        self.email = email
        self.package_name = package_name
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
    name = fields.Str(required=True, description="Project Name")
    package_name = fields.Str(required=True, description="Pypi Package name")
    author = fields.Str(required=True, description="Author name")
    email = fields.Email(required=True, description="Contact email")
    description = fields.Str(required=True, description="Project description", validate=validate.Length(max=280))
    creation_date = fields.DateTime(format=BaseSchema.format_date, default=BaseSchema.today())
    version = fields.Str(default="1.0.0", required=True, description="Package version")
    # default="No license file",
    license_type = fields.Str(validate=validate.OneOf(
        ["MIT", "BSD-3-Clause", "No license file"]), required=True, default='No license file', description="Licence type")

    architecture = fields.Nested(ArchitectureSchema, description="MLOps architecture project definition", missing=Architecture())
    setup = fields.Nested(SetupSchema, default=None, description="Setup configurations")
    deploy = fields.Nested(DeploySchema, default=None, description="CI/CD deployment configurations")
    tests = fields.Nested(TestSChema, default=None, description="Testing framework")
    # 2.- Define the object to deserialize
    
    __model__ = ProjectConfigs
    # 3.- Define custom templates and directories
    class Meta:
        templates = ['LICENSE', '.gitignore']
        default_dirs = ['deploy', 'docs', 'notebooks', 'references', 'tests', '{{package_name}}']

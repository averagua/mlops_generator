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

logger = logging.getLogger(__package__)
logging.basicConfig(level=logging.INFO)


class PipelineModel(BaseModel):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return """-name: {}""".format(self.name)

class PipelineSchema(BaseSchema):
    __model__ = PipelineModel
    name = fields.Str(description="Pipeline's name")


class ComponentModel(BaseModel):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return """-name: {}""".format(self.name)

class ComponentSchema(BaseSchema):
    __model__ = ComponentModel
    name = fields.Str(description="Component's name", required=True)


class Architecture(ComponentModel, PipelineModel):
    def __init__(self, components, pipelines):
        self.components = components
        self.pipelines = pipelines

    def __repr__(self):
        return """
            Components {}
            Pipelines {}""".format(self.components, self.pipelines)


class ArchitectureSchema(BaseSchema):
    __model__ = Architecture
    components = fields.Nested(ComponentSchema, many=True, default=[])
    pipelines = fields.Nested(PipelineSchema, many=True, default=[])

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

    def __repr__(self):
        return """entrypoint: {}""".format(self.entrypoint)

class TestsModel(BaseModel):
    def __init__(self, framework):
        self.framework = framework


class TestSChema(BaseSchema):
    __model__ = TestsModel
    framework = fields.Str(
        required=True, description="Framework for run test, ML/AI tests included", default="pytest")

class SetupSchema(BaseSchema):
    __model__ = SetupConfig
    entrypoint = fields.Str(
        required=True, description="Entrypoint for setup", default="setup.py")

    class Meta:
        templates = ['setup.py']

class ProjectConfigs(Architecture):
    def __init__(self, project, author, email, description, package_name, license_type, creation_date=None, architecture=None, version="1.0.0", setup=None, deploy=None, tests=None):
        # Serializable data
        self.project = project
        self.author = author
        self.email = email
        self.package_name = package_name
        self.description = description
        if creation_date is None:
            creation_date = datetime.today().strftime("%Y-%m-%d")
        if architecture is None:
            self.architecture = Architecture(components=[], pipelines=[])
        self.license_type = license_type
        self.deploy = deploy
        self.creation_date = creation_date
        self.version = version
        self.setup = setup
        self.tests = tests

    def add_tests(self, data):
        self.tests = None
        TestSChema().load(data)
        return self


class ProjectConfigsSchema(BaseSchema):
    __model__ = ProjectConfigs
    project = fields.Str(required=True, description="Project Name")
    author = fields.Str(required=True, description="Author name")
    email = fields.Email(required=True, description="Contact email")
    description = fields.Str(required=True, description="Project description", validate=validate.Length(max=280))
    package_name = fields.Str(required=True, description="Pypi Package name")
    creation_date = fields.DateTime(format='%Y-%m-%d')
    version = fields.Str(default="1.0.0", required=True, description="Package version")
    license_type = fields.Str(default="No license file", validate=validate.OneOf(
        ["MIT", "BSD-3-Clause", "No license file"]))

    architecture = fields.Nested(ArchitectureSchema, description="MLOps architecture project definition")
    setup = fields.Nested(SetupSchema, default=None,description="Setup configurations")
    deploy = fields.Nested(DeploySchema, default=None,description="CI/CD deployment configurations")
    tests = fields.Nested(TestSChema, default=None,description="Testing framework")

    class Meta:
        templates = ['LICENSE', 'setup.py']


class Generator:
    __PROJECT_SCHEMA = ProjectConfigsSchema()
    __CONFIG_FILE = 'mlops_configs.json'

    @classmethod
    def initialize(cls, cwd, tests=False, licence=False, setup=True):
        creation_date = datetime.today()
        # ComponentSchema.from_promt({'name': None})
        # Initialize from prompt user input
        BaseModel.cwd = cwd
        context = cls.__PROJECT_SCHEMA.from_promt({
            "project":  "covid2",
            "package_name": "covid",
            "email": "veragua.alb@gmail.com",
            "description": "description",
            "license_type": "MIT",
            "creation_date": creation_date.strftime("%Y-%m-%d"),
            "author": "Alejandro Veragua",
            "version": "1.0.0",
        })
        # Set current directory
        Project = cls.__PROJECT_SCHEMA.load(context)  # .render()
        # Enqueque creation of main project directories, an change current working directory (internal)
        # for define and persists paths
        # Enqueue project directory
        Project.put_dir(Project.project)
        BaseModel.chdir(Project.project)
        Project.put_dir(Project.package_name)
        Project.put_dir('deploy')
        Project.put_dir('tests')
        Project.put_dir('references')
        Project.put_dir('notebooks')
        # Render the generated templates
        Project.render()
        # Persists files
        Project.persist()

def main():
    try:
        logging.info('Welcome to mlops refactoring')
        command = "initialize"
        cwd = os.getcwd()
        if command == "initialize":
            Generator.initialize(cwd, tests=True, licence=True)
        else:
            raise NotImplementedError("{} not implemented".format(command))
    except Exception as e:
        logger.exception(e)
if __name__ == "__main__": main()
from jsonschema import validate, Draft7Validator, RefResolver, ErrorTree
from jsonschema.exceptions import ValidationError, best_match
from jsonschema._utils import format_as_index
from jsonschema import _types
import logging
from os import path
from sys import exit
import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, PackageLoader
from collections import deque
import click
logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.DEBUG)


class ProjectInstanceAlreadyExists(AssertionError):
    """Raise when the project instance already exists, so you can load it from same package"""
    status_code = 1001
    message = "Project instance already exists, prefer load it"


class EmptyContextError(AttributeError):
    """ Raise when the given context is empty"""
    status_code = 1001
    message = "Empty context"

from marshmallow import Schema, fields, post_load, exceptions, utils, missing
from marshmallow.fields import Field
from functools import reduce
from operator import getitem


class ContextManager:
    def __init__(self, schema, context=None, from_promt=False):
        if context is None:
            raise EmptyContextError()

        self.__context = context
        try:
            logger.info('Initializing context manager')
            self.__validator = Draft7Validator(schema)
            self.__validator.validate(self.__context)
            # logger.info(validate(context, self.__schema))
        except ValidationError as error:
            logger.info(error.message)
            # logger.info((dir(error)))
            # required = self.schema[schema_path]
            # logger.info(json.dumps(error.__dict__, indent=2))
            logger.info(self.missing_keys())

    @classmethod
    def from_jsonschema_file(cls, abs_path):
        raise NotImplementedError()

    @property
    def schema(self):
        return self.__validator.schema

    @property
    def context(self):
        return self.__context

    def __resolve_field(self, absoulte_path, sub_context):
        try:
            logger.info(absoulte_path)
            logger.info(sub_context)
            if absoulte_path is None:
                return self.context
            else:
                abs_p = absoulte_path
                logger.info(self.context[abs_p])
                logger.info(absoulte_path)
                return self.__resolve_field(absoulte_path, self.context[abs_p])
        except IndexError:
            return sub_context

    def missing_keys(self):
        _ask_for = deque()
        tree = self.__validator.iter_errors(self.__context)
        for i in tree:
            field = i.message.split("'")[1]
            failed_paths = list(i.relative_schema_path)[:-1]
            failed_paths.extend(["properties", field])
            logger.info(failed_paths)
            r = reduce(getitem, failed_paths, self.schema)
            logger.info(json.dumps(r["type"]))
            _ask_for.append(r)
            click.prompt(field) #, type=r["type"]
        logger.info(list(_ask_for))
        return ()


class MetaProject(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

import sys

def promt(cls, field_name):
    try:
        logger.info(cls)
        logger.info(dir(cls))
        return click.prompt(
                field_name,
                type = cls.resolve_primitive_type(),
                default = cls.resolve_default()
            )
    except click.exceptions.Abort as error:
        logger.info("Closed by user {}".format(error))
    else:
        return sys.exit(0)

def resolve_primitive_type(cls):
    if isinstance(cls, fields.Str):
        return str
    elif isinstance(cls, fields.Dict):
        return AssertionError("{} type is not supported for click")
    else:
        raise NotImplementedError("{} not supported".format(type(fields)))

def resolve_default(cls):
    if isinstance(cls.default, utils._Missing):
        return None
    else:
        return cls.default

# TRICKY!!

setattr(Field, promt.__name__, promt)
setattr(Field, resolve_primitive_type.__name__, resolve_primitive_type)
setattr(Field, resolve_default.__name__, resolve_default)


class DefaultConfigs:
    def __init__(self, project_name, author):
        self.project_name = project_name
        self.author = author
    
class DefaultConfigsSchema(Schema):
    project_name = fields.Str(required=True, description="Project Name")
    author = fields.Str(required=True, description="Author name")

    # logger.info(getattr(DefaultConfigs, list(error.messages.keys()).pop()))

    @classmethod
    def from_promt(cls, data):
        context = {}
        errors = cls().validate(data)
        for field in errors.keys():
            to_ask = cls._declared_fields[field]
            logger.info(to_ask)
            context[field] = to_ask.promt(field)
        return cls.from_dict(context)

    @post_load
    def default_load(self, data, **kwargs):
        return DefaultConfigs(**data)

class Component:
    def __init__(self, name):
        self.__name = name

class ComponentSchema(Schema):
    name = fields.Str(description="Component's name")


class PipelinesProject:
    def __init__(self, name):
        self.__name = name

class PipelineSchema(Schema):
    name = fields.Str(description="Pipeline's name")


class ProjectSchema(Schema):
    version = fields.Str(description="Project Version", default="1.0.0")
    default_configs = fields.Nested(DefaultConfigsSchema)
    components = fields.Nested(ComponentSchema, many=True, default=[])
    pipelines = fields.Nested(PipelineSchema, many=True, default=[])
    
    @post_load
    def project_load(self, data, **kwargs):
        return Project(**data)

class Project:
    _SCHEMA = ProjectSchema()
    def __init__(self, version, default_configs):
        self.version = version
        self.default_configs = default_configs

    @classmethod
    def initialize(cls):
        pass


class MLOpsProject(MetaProject):
    def __init__(self, ContextManager=None):
        self.__ContextManager = ContextManager

    @property
    def ContextManager(self):
        return self.__ContextManager

    @property
    def context(self):
        return self.__ContextManager.context

    @classmethod
    def init(cls):
        _SCHEMA = ProjectSchema()
        #confs = DefaultConfigsSchema.from_promt({})
        
        confs = DefaultConfigsSchema.from_dict({
            "project_name": "Project",
            "author": "alejandro"
        })
        
        project = Project(version="2.0.0", default_configs=confs)
        logger.info(dir(ComponentSchema()))
        logger.info((ComponentSchema()._declared_fields['name']))
        fields.prompt(ComponentSchema()._declared_fields['name'], 'name')
        logger.info(_SCHEMA.dump(project))
        return None

    def __repr__(self):
        return json.dumps(self.context, indent=2)


class MetaTemplate:
    def __init__(self):
        pass

class ComponentTemplate(MetaTemplate):
    def __init__(self):
        pass

class PipelineTemplate(MetaTemplate):
    def __init__(self):
        pass

class MetaBuilder:
    def __init__(self):
        pass

class ComponentDirector(MetaBuilder):
    def __init__(self):
        pass

def main():
    try:
        logging.info('Welcome to mlops refactoring')
        Project = MLOpsProject.init()
        logger.info(Project)
        # logger.info(Path("templates/schema.json").absolute())
        # logger.info(Path("templates/schema.json").resolve())
        # Project.init(Path("templates/schema.json").absolute())
    except Exception as e:
        logger.exception(e)
    finally:
        pass

if __name__ == "__main__":
    main()

import logging
from collections import OrderedDict
from importlib import import_module

from pathlib import Path
from marshmallow import (
    Schema,
    SchemaOpts,
    fields,
    exceptions,
    utils,
    missing,
    validate,
    pre_load,
    post_load,
    pre_dump,
    post_dump,
)
from marshmallow.exceptions import ValidationError
from marshmallow.schema import SchemaMeta
from types import GeneratorType
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
import click
import sys
import json

class BaseLayer(object):
    def __init__(self, package:str):
        self.__schema = None
        self.loader = import_module(package)

    @property
    def schema(self):
        if self.__schema is None: raise AttributeError('Schema not setted')
        return self.__schema
    
    @schema.setter
    def schema(self, schema_name):
        """Set echema for future purpose

        Args:
            schema (marshmallow.Schema): Schema to prompt

        Raises:
            TypeError: Is not valid schema
        """
        schema = self.get_schema(schema_name)
        if not (isinstance(schema, SchemaMeta) or isinstance(schema, Schema)):
            raise TypeError('Schema to prompt must be {} or {}'.format(Schema.__class__, SchemaMeta.__class__))
        self.__schema = schema()

    def get_schema(self, schema_name):
        schema = getattr(self.loader, schema_name, None)
        if schema is None: raise ModuleNotFoundError('{} not found'.format(schema_name))
        return schema
    
    def create_schema(self, schema_name):
        return self.get_schema(schema_name)()

class BaseModel(object):

    def __init__(self):
        pass

    # def __repr__(self):
    #     attributes = '\t'+'\t'.join([attr+'='+ str(getattr(self, attr, None))+',\n' for attr in self.__dict__ ])
    #     return """\n{}(\n{})""".format(self.__class__.__name__, attributes)

class BaseOptSchema(SchemaOpts):

    def __init__(self, meta, **kwargs):
        SchemaOpts.__init__(self, meta, **kwargs)
        self.templates = getattr(meta, 'templates', None)
        self.path = getattr(meta, 'path', '')
        self.default_dirs = getattr(meta, 'default_dirs', [])

class BaseSchema(Schema):
    """Base schema for define serializable and promptable methods"""
    # Build in model
    __model__ = BaseModel 
    OPTIONS_CLASS = BaseOptSchema

    format_date ='%B %d %X %Y'

    class Meta:
        ordered = True

    @post_load
    def make_object(self, context, **kwargs):
        """Resolve declared model after serialization"""
        logger.info('Serializing object {}'.format(self))
        made_obj = self.__model__(**context)
        # made_obj.render()
        return made_obj

    @classmethod
    def today(cls):
        """Standar today date."""
        return datetime.today()#.strftime(cls.format_date)


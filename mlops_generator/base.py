import logging
from collections import OrderedDict
from collections import deque
import os
from jinja2 import Environment, PackageLoader, FileSystemLoader, exceptions as Jinja2Exceptions
from marshmallow import (
    Schema,
    SchemaOpts,
    fields,
    post_load,
    exceptions,
    utils,
    missing,
    validate,
    post_dump,
    pre_load,
    pre_dump
)
from marshmallow.exceptions import ValidationError
from types import GeneratorType
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
import click
import sys

class BaseModel(object):
    __global_dirs_queue = deque()
    __global_files_queue = deque()


    cwd = None

    def __init__(self):
        self.__templates__ = None
        self.renderized = False

    @property
    def templates(self):
        return self.__templates__
    
    @templates.setter
    def templates(self, template):
        # if not isinstance(template, GeneratorType): raise TypeError('Must be {}'.format(GeneratorType))
        self.__templates__ = template

    @classmethod
    def global_dirs_queue(self):
        return self.__global_dirs_queue

    @classmethod
    def global_files_queue(self):
        return self.__global_files_queue 


    def render(self, enqueue=True):
        # Issue, you can renderize multiple times
        if not self.templates is None:
            # Unpack
            self.templates = OrderedDict(self.templates)
            for temp in self.__templates__: self.put_file(temp, self.get_content(temp))
        # files = [{'path': temp, 'content': content} for temp, content in self.__templates__]
        # logger.info(files)
        # self.__global_files_queue.extend(files)
        # for template, body in self.templates:
        #     templates[template] = body['content']
        # self.templates = templates
        return self

    def get_content(self, template_key):
        try:
            template = self.templates[template_key]
            return template
        except KeyError as e:
            raise e

    """def __str__(self):
        print(self.__dict__)
        result = self.__class__.__name__
        return result"""

    def join_path(self, path):
        return os.path.join(self.cwd, path)


    def put_dir(self, new_dir):
        if self.cwd is None:
            raise AttributeError('Current directory is not setted')
        to_put = self.join_path(new_dir)
        if os.path.exists(to_put):
            error = FileExistsError(
                'Directory {} already exists'.format(to_put))
            logger.error(error)
        self.__global_dirs_queue.append(to_put)
        logger.debug("Path queued ({}): {}".format(len(self.__global_dirs_queue), to_put))

    def put_file(self, filename, content):
        path = self.join_path(filename)
        self.__global_files_queue.append({
            'path': path,
            "content": content
        })
        logger.debug("File queued ({}): {}".format(len(self.__global_files_queue), path))
        return self

    """
    @property
    def cwd(self):
        # logger.info("Local current working directory {}".format(self.__cwd))
        if self.__cwd is None:
            raise AttributeError('Current directory not found')
        return self.__cwd

    @cwd.setter
    def cwd(self, cwd):
        self.__cwd = cwd
    """
    @classmethod
    def chdir(cls, path):
        cls.cwd = os.path.join(cls.cwd, path)
        logger.debug(
            "Internal current working directory changed to {}".format(cls.cwd))
            
    def persist_dirs(self):
        try:
            new_dir = self.__global_dirs_queue.popleft()
            logger.info('Directory created {}'.format(new_dir))
            os.mkdir(new_dir)
            self.persist_dirs()
        except IndexError:
            logger.info('Directories pesisted!')
            return self
        except Exception as error:
            logger.error(error)
            # In generic exception continue iteration
            self.persist_dirs()
    
    def persist_files(self):
        try:
            new_file = self.__global_files_queue.popleft()
            logger.info('File created {}'.format(new_file['path']))
            with open(new_file['path'], 'w') as f: f.write(new_file['content'])
            self.persist_files()

        except IndexError:
            logger.info('Files pesisted!')
            return self
        except Exception as error:
            logger.error(error)
            self.persist_files()

    def persist(self):
        self.persist_dirs()
        self.persist_files()
        return self

class BaseOptSchema(SchemaOpts):

    def __init__(self, meta, **kwargs):
        SchemaOpts.__init__(self, meta, **kwargs)
        self.templates = getattr(meta, "templates", None)

class BaseSchema(Schema):
    """Base schema for define serializable and promptable methods"""
    # Build in model
    __model__ = BaseModel 
    OPTIONS_CLASS = BaseOptSchema
    try:
        loader = PackageLoader('mlops_generator', 'templates')
        logger.debug('Package loader')
    except ImportError as error:
        logger.debug('Filesystem loader')
        loader = FileSystemLoader("mlops_generator/mlops_generator/templates")
    except Exception as error:
        raise error

    __TEMPLATE_ENGINE = Environment(
        loader=loader,
        trim_blocks=False,
    )

    format_date ='%Y-%m-%d %H:%M'

    class Meta:
        ordered = True

    @post_load
    def make_object(self, context, **kwargs):
        """Resolve declared model after serialization"""
        logger.info('Serializing object {}'.format(self))
        made_obj = self.__model__(**context)
        # made_obj.templates = self._gen_templates(context)
        # made_obj.render()
        return made_obj

    @classmethod
    def today(cls):
        """Standar today date."""
        return datetime.today().strftime(cls.format_date)

    def _gen_templates(self, context):
        try:
            for template in self.opts.templates:
                gtemplate = self.__TEMPLATE_ENGINE.get_template(template)
                yield template, gtemplate.render(context)
        except Jinja2Exceptions.TemplateNotFound as error:
            logger.error(
                'Error getting template {} - {}'.format(error.message, type(error)))
        except Jinja2Exceptions.TemplateSyntaxError as error:
            message = "{} in line {} - {}".format(
                error.message, error.lineno, error.source.split('\n')[error.lineno - 1])
            logger.error(message)
        except Exception as error:
            logger.exception(error)

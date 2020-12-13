from typing import Union, Optional, Dict
from pathlib import Path

from collections import deque
import json
from jinja2 import (
    Environment,
    PackageLoader,
    FileSystemLoader,
    exceptions as Jinja2Exceptions,
    Template,
)

from mlops_generator.base import BaseLayer, BaseSchema
from collections import OrderedDict

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

try:
    loader = PackageLoader("mlops_generator", "templates")
    logger.info("Package loader")
except ImportError as error:
    logger.info("Filesystem loader")
    loader = FileSystemLoader("mlops_generator/mlops_generator/templates")
except Exception as error:
    logger.error(error)
    raise error

TEMPLATE_ENGINE = Environment(
    loader=loader,
    trim_blocks=False,
)


class PresentationLayer(BaseLayer):

    RENDER = "render"
    NEW_DIR = "new_dir"
    ENCODING = "utf-8"

    def __init__(self, cwd: Path, config_file="mlops-configs.json"):
        super().__init__(package="mlops_generator.project")
        self.__cwd = cwd
        self.__events_queue = deque()
        self.config_file = config_file
        logger.info(
            "Persistence layer initialized in current working directory {}".format(
                self.__cwd
            )
        )

    @property
    def handler(self):
        return {
            self.RENDER: self.template_handler,
            self.NEW_DIR: self.directory_handler,
        }

    def handle(self, event, *args, **kwargs):
        try:
            self.handler.get(event["type"], lambda: AssertionError("Event not found"))(
                event, *args, **kwargs
            )
        except Exception as error:
            logger.error(error)

    def render_string(self, string: str, context: OrderedDict) -> str:
        return TEMPLATE_ENGINE.from_string(string).render(context)

    def template_handler(self, event: dict, context: OrderedDict, *args, **kwargs):
        file_content = event["value"].render(context)
        path = self.render_string(string=str(event["path"]), context=context)
        path = Path(path)
        if path.exists():
            logger.error("{} already exists".format(path.name))
        else:
            logger.info("Saving {}".format(path))
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(file_content, encoding=self.ENCODING)

    def directory_handler(self, event: dict, context: OrderedDict, *args, **kwargs):
        path = self.render_string(str(event["value"]), context)
        path = Path(path)
        path.mkdir(parents=True, exist_ok=False)
        logger.info("Path created {}".format(path))

    def get_template(self, template_name):
        try:
            return TEMPLATE_ENGINE.get_template(template_name)
        except Jinja2Exceptions.TemplateNotFound as error:
            logger.error(
                "Error getting template {} - {}".format(error.message, type(error))
            )
            raise error
        except Jinja2Exceptions.TemplateSyntaxError as error:
            message = "{} in line {} - {}".format(
                error.message, error.lineno, error.source.split("\n")[error.lineno - 1]
            )
            logger.error(message)
        except Exception as error:
            logger.exception(error)

    def get_template_events(self, schema):
        templates = schema.opts.templates
        templates = [
            {
                "type": self.RENDER,
                "value": self.get_template(template),
                "path": Path(self.cwd, schema.opts.path) / Path(template).name,
            }
            for template in templates
        ]
        return [template for template in templates if templates]

    def get_directory_events(self, schema):
        return [
            {"type": self.NEW_DIR, "value": self.cwd / directory}
            for directory in schema.opts.default_dirs
        ]

    @property
    def cwd(self):
        return self.__cwd

    @property
    def events_queue(self) -> deque:
        """Queued events"""
        return self.__events_queue

    def push_event(self, data):
        if isinstance(data, list):
            self.__events_queue.extend(data)
        else:
            self.__events_queue.append(data)

    def push_job(self, schema_name, return_schema: bool = False):
        logger.debug("Pushing {} schema job".format(schema_name))
        schema = self.get_schema(schema_name)
        template_events = self.get_template_events(schema)
        directory_events = self.get_directory_events(schema)
        self.push_event(template_events)
        self.push_event(directory_events)
        if return_schema:
            return schema()
        return self

    def render(self, context, persist=True):
        logger.debug("Trying to renderize source code in {}".format(self.cwd))
        self.cwd.mkdir(parents=True, exist_ok=True)
        while True:
            try:
                event = self.__events_queue.popleft()
                self.handle(event, context)
            except IndexError:
                logger.info("Renderization finished")
                if persist:
                    config_path = self.cwd / self.config_file
                    config_path.write_text(json.dumps(context, indent=2))
                return context

    def from_config(self, schema_name:str, config_file:str="mlops-configs.json"):
        config_path = self.cwd / config_file
        with config_path.open('r') as jn:
            context = json.load(jn)
        return self.create_schema(schema_name).load(context)
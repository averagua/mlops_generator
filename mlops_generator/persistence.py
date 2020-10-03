import os
import logging
from collections import deque
from base import BaseLayer
import json
from jinja2 import Environment, PackageLoader, FileSystemLoader, exceptions as Jinja2Exceptions

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class PresentationLayer(BaseLayer):
    __root_key = 'root'
    def __init__(self, loader, root):
        super().__init__(loader)
        self.__cwd = os.getcwd()
        self.__events_queue = deque()
        self.__root = os.path.join(self.__cwd, root)
        if not os.path.exists(self.__root): self.__push_event({ 'type': 'new_dir', 'data': {'dir': self.__root}})
        logger.info('Persistence layer initialized in current root directory {}'.format(self.__root))
        try:
            loader = PackageLoader('mlops_generator', 'templates')
            logger.debug('Package loader')
        except ImportError as error:
            logger.debug('Filesystem loader')
            loader = FileSystemLoader("mlops_generator/mlops_generator/templates")
        except Exception as error:
            raise error

        self.__TEMPLATE_ENGINE = Environment(
            loader=loader,
            trim_blocks=False,
        )

    @property
    def root(self):
        return self.__root
    
    @property
    def events_queue(self):
        return self.__events_queue


    def push_job(self):
        pass

    def __push_event(self, data):
        if isinstance(data, list): self.__events_queue.extend(data)
        else: self.__events_queue.append(data)

    def resolve_path(self, path):
        # logger.info('Where im resolving? {}'.format(self.root))
        if not self.parent_dir is self.__root_key:
            path = os.path.join(self.parent_dir, path)
        resolved_path = os.path.join(self.root, path)
        return resolved_path

    def push_directories(self):
        default_dirs = self.default_dirs
        event_type = 'new_dir'
        default_dirs = [self.resolve_path(default_dir) for default_dir in default_dirs ]
        [ self.__push_event({
            'type': event_type,
            'data': {
                'dir': directory
            }
        }) for directory in default_dirs ]

    def push_templates(self):
        if not self.parent_dir is self.__root_key: logger.info(self.parent_dir)
        if not self.templates is None:
            for template in self.templates:
                events = {
                        'type': 'render',
                        'data': {
                            'template': self.get_template(template),
                            'dir': self.resolve_path(template)
                        }
                    }
                self.__push_event(events)
        else: logger.warning('No templates to push in this schema')

    def push_job(self, schema_name):
        self.schema = schema_name
        self.push_directories()
        self.push_templates()
        return self

    def get_template(self, template_name):
        try:
            return self.__TEMPLATE_ENGINE.get_template(template_name)
        except Jinja2Exceptions.TemplateNotFound as error:
            logger.error(
                'Error getting template {} - {}'.format(error.message, type(error)))
        except Jinja2Exceptions.TemplateSyntaxError as error:
            message = "{} in line {} - {}".format(
                error.message, error.lineno, error.source.split('\n')[error.lineno - 1])
            logger.error(message)
        except Exception as error:
            logger.exception(error)


    def render(self, obj):
        context = self.schema.dump(obj)
        logger.info(json.dumps(context))
        while True:
            try:
                event = self.__events_queue.popleft()
                output_path = self.__TEMPLATE_ENGINE.from_string(event['data']['dir']).render(context)
                logger.info(output_path)
                if os.path.exists(output_path): logger.warning('File already exists')
                elif event['type'] is 'new_dir':
                    os.mkdir(output_path)
                elif event['type'] is 'render':
                    file_content = event['data']['template'].render(context)
                    with open(output_path, 'w') as f: f.write(file_content)
                else:
                    pass
            except IndexError:
                return 
    def persist(self):
        pass

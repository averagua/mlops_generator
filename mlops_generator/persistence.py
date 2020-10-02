import os
import logging
from collections import deque
from base import BaseLayer
import json

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class PresentationLayer(BaseLayer):
    __root_key = 'root'
    def __init__(self, loader, root):
        super().__init__(loader)
        self.__cwd = os.getcwd()
        self.__templates_queue = deque()
        self.__root = os.path.join(self.__cwd, root)
        if not os.path.exists(self.__root): self.push_event({ 'type': 'new_dir', 'data': {'dir': self.__root}})
        logger.info(self.__root)
        logger.info('Persistence layer initialized in current root directory {}'.format(self.__root))

    @property
    def root(self):
        return self.__root
    
    @property
    def templates_queue(self):
        return self.__templates_queue

    def resolve_path(self, path):
        # logger.info('Where im resolving? {}'.format(self.root))
        return os.path.join(self.root, path)

    def queue_path(self, directory):
        event = { 'type': 'new_dir', 'data': {'dir': self.resolve_path(directory)}}
        self.push_event(event)

    def push_event(self, data):
        if isinstance(data, list): self.__templates_queue.extend(data)
        else: self.__templates_queue.append(data)


    def push_template(self, schema_name):
        self.schema = schema_name
        # if self.parent_dir is self.__root_key: event['data']['dir'] = self.
        logger.info(self.resolve_path(self.templates[0]))
        events = {
                'type': 'render',
                'data': [{
                    'template': template,
                    'dir': self.resolve_path(template)
                }
                for template in self.templates
                ]
            }
        self.push_event(events)
        logger.info(json.dumps(list(self.__templates_queue), indent=2))


    def render(self, context):
        pass

    def persist(self):
        pass

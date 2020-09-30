import logging
from collections import OrderedDict, deque
from marshmallow.schema import Schema, SchemaMeta
from marshmallow import validate, utils
from marshmallow.exceptions import ValidationError
import sys
import click

logger = logging.getLogger(__package__)
logging.basicConfig(level=logging.INFO)

class PromptAdapter:
    """
    Prompt Adapter for serialize (load) an schema using click prompt
    Raises:
        TypeError: [description]

    Returns:
        [type]: [description]
    """
    __TYPES = {
        'String':   str,
        'Dict':     dict,
        'List':     list,
        'Tuple':    tuple,
        'Number':   float,
        'Integer':  int,
        'Decimal':  float,
        'Boolean':  bool,
        'Float':    float,
        'Str':      str,
        'Bool':     bool,
        'Int':      int,
        'Email':    str,
        'DateTime': str
    } 

    def __init__(self, schema):
        self.__schema = schema

    @property
    def schema(self):
        return self.__schema
    
    @schema.setter
    def schema(self, schema):
        """Set echema for future purpose

        Args:
            schema (marshmallow.Schema): Schema to prompt

        Raises:
            TypeError: Is not valid schema
        """
        if not (isinstance(schema, SchemaMeta) or isinstance(schema, Schema)):
            raise TypeError('Schema to prompt must be {} or {}'.format(Schema.__class__, SchemaMeta.__class__))

    def mlw_py(self, field):
        """Adapt the marshmallow field types to python primitives.
        
        Args:
            schema (marshmallow.field): Marshmallow field type
        """
        try:
            marshmallow_type = field.__class__.__name__
            return self.__TYPES[marshmallow_type]
        except KeyError:
            logger.error("Marsmallow type {} not supported in prompt".format(field.__class__))

    def ask_for(self, field_name):
        """
        Transform the Schema definition for user input.

        Transform to click.prompt keyword for all datatypes defined in self.__TYPES

        - text [SUPPORTED] the text to show for the prompt.
        - default [SUPPORTED] the default value to use if no input happens. If this is not given it will prompt until it’s aborted
        - type [SUPPORTED] the type to use to check the value against.
        - show_choices [SUPPORTED] - Show or hide choices if the passed type is a click.Choice
        Args:
            field_name (str): field name to map

        Returns:
            value (str): User input value
        """
        try:
            prompt_args = {}
            prompt_args['text'] = field_name
            field = self.schema._declared_fields[field_name]
            ptype = self.mlw_py(field)
            prompt_args['type'] = ptype
            # Support marshmallow validation.
            if self._not_missing(field.validate):
                # One is like choices
                if isinstance(field.validate, validate.OneOf):
                    prompt_args['type'] = click.Choice(field.validate.choices)
            # Support text from metadata description
            if 'description' in field.metadata.keys(): prompt_args['text'] = field.metadata['description']
            # Support defaults If default is not missing map to default prompt
            if self._not_missing(field.default): prompt_args['default'] = field.default
            value = click.prompt(**prompt_args)
            return value
        except KeyboardInterrupt as e:
            logger.info('\nClosed by user')
            sys.exit()
        except click.exceptions.Abort as e:
            logger.info('\nClosed by user')
            sys.exit()

    def _not_missing(self, field):
        """
        Validate if not missing

        [extended_summary]

        Args:
            field (marshmallow.field): Field to valida if missing 

        Returns:
            bool: True if is not missing
        """
        return not isinstance(field, utils._Missing)

    def gen_prompts(self, context=None):
        """
        Generate __model__ class from prompt user input.
        This implementation only support click for define the interface.

        Only resolve the validations errors for keys in the context

        Args:
            context (OrderedDict, optional): Current context to iterate with the prompt using. Defaults to None.
            If context is `None`, an empty ordered dict is initialized

        Raises:
            TypeError: When the context is not a `dict` or `OrderedDitct`

        Returns:
            __model__.__class__: Built class instance
        """
        try:
            if context is None: context = OrderedDict({})
            if isinstance(context, dict): context = OrderedDict(context)
            obj = self.schema.load(context)
            # for field_name in errors:
            return obj
        except ValidationError as e:
            field_name = list(e.messages.keys()).pop(0)
            context[field_name] = self.ask_for(field_name)
            # Retry until the user input value is valid over field definition
            return self.gen_prompts(context)
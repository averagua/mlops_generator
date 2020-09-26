from marshmallow import Schema, fields, post_load, exceptions, utils, missing, validate
import logging
import click

logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.DEBUG)

class PipelinesProject:
    def __init__(self, name):
        self.__name = name

class PipelineSchema(Schema):
    name = fields.Str(description="Pipeline's name")

class Component:
    def __init__(self, name):
        self.__name = name

class ComponentSchema(Schema):
    name = fields.Str(description="Component's name", required=True)


class ProjectConfigs:
    def __init__(self, project_name, author, email, description, package_name):
        self.project_name = project_name
        self.author = author
        self.email = email
        self.description = description
        self.package_name = package_name
        components = fields.Nested(ComponentSchema, many=True, default=[])
        pipelines = fields.Nested(PipelineSchema, many=True, default=[])
    
    
class ProjectConfigsSchema(Schema):
    project_name = fields.Str(required=True, description="Project Name")
    author = fields.Str(required=True, description="Author name")
    email = fields.Email(required=True, description="Contact email")
    description = fields.Str(required=True, description="Project description", validate=validate.Length(max=280) )
    package_name = fields.Str(required=True, description="Pypi Package name")
    components = fields.Nested(ComponentSchema, many=True, default=[])
    pipelines = fields.Nested(PipelineSchema, many=True, default=[])
    
    @post_load
    def default_load(self, data, **kwargs):
        return ProjectConfigs(**data)

def main():
    try:
        logging.info('Welcome to mlops refactoring')
        data = {
            "version": "1.0.0",
            "default_configs":{
                "project_name": "Covid-19",
                "author": "Alejandro Veragua",
                "package_name": "covid_19",
                "email": "veragua.alb@gmail.com",
                "description": "Covid 19 project example for MLOps proove of concept"
            }
        }
        schema = ProjectConfigsSchema()
        result = schema.load(data["default_configs"])
        logger.info(schema.dumps(result, indent=2))
        # project = DefaultConfigsSchema.from_dict(data["default_configs"])
        # logger.info(project)
        # logger.info(DefaultConfigsSchema.loads(data["default_configs"]))
        # logger.info(Path("templates/schema.json").absolute())
        # logger.info(Path("templates/schema.json").resolve())
        # Project.init(Path("templates/schema.json").absolute())
    except Exception as e:
        logger.exception(e)
    finally:
        pass

if __name__ == "__main__":
    main()



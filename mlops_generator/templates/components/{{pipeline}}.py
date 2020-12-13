from kfp import dsl
from kfp.compiler import Compiler, VersionedDependency

@dsl.pipeline(
    name="{{ pipeline.name }}",
    description= "{{ pipeline.description }}"
)

def {{pipeline.name}}(a: int = 1, b: str = "default value"):
    pass

Compiler().compile(my_pipeline, '{{pipeline.path}}/{{pipeline.name}}.yaml')
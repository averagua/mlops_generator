"""
{{component_name}} kubeflow container op
version {{version}} - {{creation_date}}
company: {{company}}
"""
from kfp.dsl import ContainerOp
from kfp.dsl.types import Integer, Float, Dict, String, List

_BASE_IMAGE = "{{architecture.docker.registry}}/{{project_name}}/{{project_name}}:latest"

class {{component_name}}(ContainerOp):
    """Define kubeflow pipeline component."""

    def __init__(self,
        sparam: String(),
        fparam: Float(),
        dparam: Dict(),
        lparam: List()
        ):
        super({{component_name}}, self).__init__(
            name="{{ component_name }}",
            image=_BASE_IMAGE,
            command=["{{ setup.entry_point }}", "{{ component_name }}"],
            arguments=[
                "--sparam", sparam,
                "--fparam", fparam,
                "--dparam", dparam,
                "--lparam", lparam
            ],
            file_outputs={
                {% if ui_metadata %}"mlpipeline-ui-metadata": "/mlpipeline-ui-metadata.json",{% endif %}
                {% if tmp_data %}"tmp-data": "{{tmp_data}}",{% endif %}
            },
        )
from kfp.dsl import ContainerOp
from kfp.dsl.types import Integer, Float, Dict, String, List

_BASE_IMAGE = "{{docker.registry}}.io/{{project_name}}/{{project_package}}:latest"

class {{component_classname}}ContainerOp(ContainerOp):
    """Define kubeflow pipeline component."""

    def __init__(self,
        sparam: String(),
        fparam: Float(),
        dparam: Dict(),
        lparam: List()
        ):
        super(PreprocessingContainerOp, self).__init__(
            name="{{ component_name }}",
            image=_BASE_IMAGE,
            command=["{{ setup["entry_point"]}}", "{{ component_name }}"],
            arguments=[
                "--sparam", sparam,
                "--fparam", fparam,
                "--dparam", dparam,
                "--lparam", lparam
            ],
            file_outputs={
                {% if add_ui %}
                "mlpipeline-ui-metadata": "/mlpipeline-ui-metadata.json",
                {% endif %}
                {% if tmp %}
                "tmp-data": "/tmp_data.json",
                {% endif %}
            },
        )
from kfp import compiler, gcp, components, Client
import kfp.dsl as dsl
from pathlib import Path
from click.core import Option, Command

# Import your components
from {{project_name}}.MODULE import ContainerOp

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

INTERNAL_KF_SA = "user-gcp-sa"
PIPELINE_DIR = "pipelines"

HOST_URL = "https://<KUBEFLOW_HOST>/pipeline"
PIPELINE_NAME = "{{pipeline_name}}"
CLIENT_ID = "<CLIENT_ID>"
NAMESPACE = "default-profile"
EXPERIMENT_NAME = "{{experiment_name}}"
_BASE_IMAGE = "{{architecture.docker.registry}}/{{project_name}}/{{project_name}}:latest"

@dsl.pipeline(
    name=PIPELINE_NAME,
    description="Pipeline {{project_name}} - {{pipeline_name}}",
)
def pipeline():
    # Declare your step
    op = ContainerOp().apply(gcp.use_gcp_secret(INTERNAL_KF_SA))
    # Set diplay name
    op.set_display_name("{{pipeline}}")
    # No cache step
    op.execution_options.caching_strategy.max_cache_staleness = "P0D"


class PipelinesCommands(Command):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.params.extend([
            self.compile,
            self.version,
            self.upload,
            ])

    @property
    def compile(self):
        """Compile pipeline version"""
        return Option(
            ("--kfp-compile",),
            type=str,
            help="Compile pipeline.yaml using kubeflow compiler.",
            is_flag=True,
        )

    @property
    def version(self):
        return Option(("--version",), type=str, help="Upload a new pipeline version.")

    @property
    def upload(self):
        return Option(("--upload",), type=bool, help="Upload pipeline to kubeflow.")


def main(kfp_compile: bool = False, version: str = None, upload: bool = False):
    cwd = Path().cwd()
    # Declare pipeline funcion
    pipeline_func = pipeline
    # Create pipeline filename
    pipeline_filename = pipeline_func.__name__ + version + ".yaml"
    cwd = cwd / PIPELINE_DIR
    cwd.mkdir(parents=True, exist_ok=True)
    pipeline_filename = cwd / pipeline_filename
    logger.info("Working on {}".format(pipeline_filename))
    # Compile pipeline
    if kfp_compile:
        logger.info("Compiling pipeline to filename {}".format(pipeline_filename))
        compiler.Compiler().compile(pipeline_func, str(pipeline_filename))
    logger.info("Connecting to client")
    # Create client with some additional functionalities
    client = Clien(host=HOST_URL, client_id=CLIENT_ID)
    # Get pipeline ID for check if exists
    pipeline_id = client.get_pipeline_id(PIPELINE_NAME)
    logger.info("Pipeline ID {}".format(pipeline_id))
    # Upload pipeline first time
    if upload or pipeline_id is None:
        logger.info("Uploading pipeline {}".format(pipeline_filename))
        client.upload_pipeline(
            pipeline_package_path=pipeline_filename, pipeline_name=PIPELINE_NAME
        )
    # Versioned the pipeline, only if exists and upload is not setted
    elif version:
        version = "{}-{}".format(PIPELINE_NAME, version)
        logger.info("Updating version {}".format(version))
        client.upload_pipeline_version(
            pipeline_package_path=pipeline_filename,
            pipeline_name=PIPELINE_NAME,
            pipeline_version_name=version,
        )
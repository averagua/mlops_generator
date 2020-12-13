"""Console script for mlops_generator."""
import sys
from os import getcwd
import click
from click import option, command
from click.core import Option, Command
from pathlib import Path

from mlops_generator.interface import Interface

import logging

logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)


class InitCommand(Command):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.params.extend([self.setup, self.tests, self.dockerfile, self.deploy,])

    @property
    def tests(self):
        """Initialize with tests"""
        return Option(
            ("--tests",),
            type=bool,
            help="Add pytest suite",
            is_flag=True,
            default=False,
        )

    @property
    def setup(self):
        """Initialize with setup.py"""
        return Option(
            ("--setup",),
            type=bool,
            help="Add setup",
            is_flag=True,
            default=False,
        )

    @property
    def dockerfile(self):
        """Initialice dockerfile"""
        return Option(
            ("--docker",),
            type=bool,
            help="Add docker",
            is_flag=True,
            default=False,
        )

    @property
    def deploy(self):
        """Initialice pipeline CI"""
        return Option(
            ("--deploy",),
            type=bool,
            help="Add pipeline CI",
            is_flag=True,
            default=False,
        )

class ComponentCommmand(Command):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.params.extend([
            self.project_dir,
            self.pandas,
            self.sklearn,
            self.kubeflow_component,
            self.kubeflow_pipeline,
            self.jupyter_notebook,
            self.artifacts
        ])

    @property
    def pandas(self):
        """Pandas extension"""
        return Option(
            ("--pandas",),
            type=bool,
            help="Add pandas extension",
            is_flag=True,
            default=False,
        )

    @property
    def project_dir(self):
        """Project directory"""
        return Option(
            ("--project-dir",),
            type=str,
            help="Project directory, by default is current working directory",
            default="",
        )      

    @property
    def sklearn(self):
        """Sklearn base class"""
        return Option(
            ("--sklearn",),
            type=bool,
            help="Add sklearn base class",
            is_flag=True,
            default=False,
        )

    @property
    def kubeflow_component(self):
        """Kubeflow component container op class"""
        return Option(
            ("--kubeflow-component",),
            type=bool,
            help="Add kubeflow component container op",
            is_flag=True,
            default=False,
        )

    @property
    def kubeflow_pipeline(self):
        """Pipeline implementation"""
        return Option(
            ("--kubeflow-pipeline",),
            type=bool,
            help="Add kubeflow-pipeline",
            is_flag=True,
            default=False,
        )

    @property
    def jupyter_notebook(self):
        """Jupyter notebook document"""
        return Option(
            ("--jupyter-notebook",),
            type=bool,
            help="Add kubeflow-pipeline",
            is_flag=True,
            default=False,
        )

    @property
    def artifacts(self):
        """Temporal data and visualization artifacts"""
        return Option(
            ("--artifacts",),
            type=bool,
            help="Add temporal data and visualization artifacts",
            is_flag=True,
            default=False,
        )

@click.group()
def main():
    """Commmand Line Interface for MLOps lifecycle."""
    pass


@main.command("init", help="Initialize mlops project", cls=InitCommand)
def init(*args, **kwargs):
    """
    Initialize a project in the current working directory.

    Args:
        project_template ([type]): [description]
    """
    try:
        cwd = Path().cwd()
        Interface().initialize(cwd, *args, **kwargs)
        click.echo("Initialize mlops project")
    except Exception as error:
        logger.error(error)
        sys.exit(0)


@main.command("add", help="Add configuration to project", cls=InitCommand)
@click.option("--project-dir", help="Give project name if you want", default="")
def add(project_dir, *args, **kwargs):
    """Add a configuration to the current project."""
    try:
        cwd = Path().cwd() / project_dir
        Interface().add(cwd, *args, **kwargs)
    except Exception as error:
        logger.exception(error)
        sys.exit(0)


@main.command(
    "component",
    help="Generate a component",
    context_settings=dict(ignore_unknown_options=True),
    cls=ComponentCommmand
)
def component(project_dir, *args, **kwargs):
    """CLI for generate MLOps archetypes."""
    try:
        cwd = Path().cwd() / project_dir
        Interface().component(cwd, *args, **kwargs)
    except Exception as error:
        logger.exception(error)
        sys.exit(0)


# @main.command(
#     "pipeline",
#     help="Generate a kubeflow pipeline",
#     context_settings=dict(ignore_unknown_options=True),
# )
# def pipeline():
#     """Generate a pipeline."""
#     pass


if __name__ == "__main__":
    main()

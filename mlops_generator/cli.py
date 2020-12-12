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
        self.params.extend([
            self.setup,
            self.tests,
            self.dockerfile,
            self.deploy
        ])

    @property
    def tests(self):
        """Initialize with tests"""
        return Option(("--tests",), type=bool, help="Add pytest suite", is_flag=True)

    @property
    def setup(self):
        """Initialize with setup.py"""
        return Option(
            ("--setup",),
            type=bool,
            help="Add setup entrypoint",
            is_flag=True,
            default=False,
        )

    @property
    def dockerfile(self):
        """Initialice dockerfile"""
        return Option(
            ("--docker",),
            type=bool,
            help="Add setup entrypoint",
            is_flag=True,
            default=False,
        )

    @property
    def deploy(self):
        """Initialice pipeline CI"""
        return Option(
            ("--deploy",),
            type=bool,
            help="Add setup entrypoint",
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
)
@click.option("--project-dir", help="Give project name if you want", default="")
@click.option(
    "--module",
    help="Module type to generate",
    prompt="What component do you want to create?",
    type=click.Choice(["pandas", "sklearn", "tensorflow", "kubeflow"]),
    default="pandas",
    show_default=True,
)

def component(project_dir, module, *args, **kwargs):
    """CLI for generate MLOps archetypes."""
    try:
        cwd = Path().cwd() / project_dir
        Interface().component(cwd, module, *args, **kwargs)
    except Exception as error:
        logger.exception(error)
        sys.exit(0)

@main.command(
    "pipeline",
    help="Generate a kubeflow pipeline",
    context_settings=dict(ignore_unknown_options=True),
)
def pipeline():
    """Generate a pipeline."""
    pass

if __name__ == "__main__":
    main()

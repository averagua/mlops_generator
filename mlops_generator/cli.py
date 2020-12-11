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
            self.cloudbuild
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
            default=True,
        )

    @property
    def dockerfile(self):
        """Initialice dockerfile"""
        return Option(
            ("--dockerfile",),
            type=bool,
            help="Add setup entrypoint",
            is_flag=True,
            default=True,
        )

    @property
    def cloudbuild(self):
        """Initialice dockerfile"""
        return Option(
            ("--cloudbuild",),
            type=bool,
            help="Add setup entrypoint",
            is_flag=True,
            default=True,
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
    cwd = Path().cwd()
    Interface().initialize(cwd, *args, **kwargs)
    click.echo("Initialize mlops project")


@main.command("add", help="Add configuration to project", cls=InitCommand)
def add(*args, **kwargs):
    """Add a configuration to the current project."""
    cwd = Path().cwd()
    Interface().add(cwd, *args, **kwargs)


@main.command(
    "component",
    help="Generate a component",
    context_settings=dict(ignore_unknown_options=True),
)
@click.option(
    "--name",
    help="Module name",
    prompt="Type a name for your component",
    show_default=True,
)
@click.option(
    "--module",
    help="Module type to generate",
    prompt="What component do you want to create?",
    type=click.Choice(["pandas", "sklearn", "tensorflow", "kubeflow"]),
    default="pandas",
    show_default=True,
)
@click.option("--out-filename", type=str, help="Output path for the filename")
def component(name, module, out_filename):
    """CLI for generate MLOps archetypes."""
    click.echo("Adding component... {} ".format(module))
    print(out_filename)
    # if module == 'pandas':
    #    pandas_extension(name, out_filename)


@main.command(
    "pipeline",
    help="Generate a kubeflow pipeline",
    context_settings=dict(ignore_unknown_options=True),
)
def pipeline():
    """Generate a pipeline."""
    pass


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

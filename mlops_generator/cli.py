"""Console script for mlops_generator."""
import sys
import click
import logging
from interface import Interface
from os import getcwd

logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)


@click.group()
def main():
    """Commmand Line Interface for MLOps lifecycle."""
    pass

@main.command('init', help='Initialize mlops project')
@click.option('--tests', help='Add test suite', default=True, type = bool)
@click.option('--licence', help='Add licence type', default=True, type = bool)
def init(*args, **kwargs):
    """
    Initialize a project in the current working directory.

    Args:
        project_template ([type]): [description]
    """
    cwd = getcwd()
    Interface.initialize(cwd, *args, **kwargs)
    click.echo('Initialize mlops project')

@main.command('add', help='Add configuration to project')
def add():
    """Add a configuration to the current project."""
    pass

@main.command('component', help='Generate a component', context_settings=dict(ignore_unknown_options=True))
@click.option(
    '--name',
    help='Module name',
    prompt='Type a name for your component',
    show_default=True
)
@click.option(
    '--module',
    help='Module type to generate',
    prompt="What component do you want to create?",
    type=click.Choice(['pandas', 'sklearn', 'tensorflow', 'kubeflow']),
    default='pandas',
    show_default=True
)
@click.option(
    '--out-filename',
    type=str,
    help='Output path for the filename'
)
def component(name, module, out_filename):
    """CLI for generate MLOps archetypes."""
    click.echo('Adding component... {} '.format(module))
    print(out_filename)
    # if module == 'pandas':
    #    pandas_extension(name, out_filename)


@main.command('pipeline', help='Generate a kubeflow pipeline', context_settings=dict(ignore_unknown_options=True))
def pipeline():
    """Generate a pipeline."""
    pass


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

"""Console script for mlops_generator."""
import sys
import click
from .generator import pandas_extension, initialize
import logging
logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)


@click.group()
def main():
    """Commmand Line Interface for MLOps lifecycle."""
    pass


@main.command('init', help='Initialize mlops project')
@click.option(
    '--project-template',
    help="Project template from initialize project",
    default="https://github.com/averagua/mlops-kubeflow"
)
def init(project_template):
    click.echo('Initialize mlops project')
    initialize(project_template)

@main.command('add', help='Add configuration to project')
def add():
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
    if module == 'pandas':
        pandas_extension(name, out_filename)


@main.command('pipeline', help='Generate a kubeflow pipeline', context_settings=dict(ignore_unknown_options=True))
def pipeline():
    pass


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

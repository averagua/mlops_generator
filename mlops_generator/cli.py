"""Console script for mlops_generator."""
import sys
import click
from .mlops_generator import pandas_extension

@click.group()
def main():
    """Commmand Line Interface for MLOps lifecycle."""
    pass

@main.command(
    'generate',
    help='Generate a component from template',
    context_settings=dict(ignore_unknown_options=True)
)
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
    type=click.Choice(['pandas', 'sklearn', 'tensorflow']),
    default='pandas',
    show_default=True
)
@click.option(
    '--unit',
    is_flag=True,
    prompt="Do you want add unit pytest?", 
    help='Generate a unit test for the module',
    show_default=True
)
@click.option(
    '--out-filename',
    prompt='Where do you want to save output module?',
    type=str,
    help='Output filename and directory',
    default='./'
    )
def generate(name, module, unit, out_filename):
    """CLI for generate MLOps archetypes."""
    click.echo('Adding component... {} '.format(module))
    click.echo('Add unit test  {} '.format(unit))
    if module == 'pandas':
        pandas_extension(name, out_filename)

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

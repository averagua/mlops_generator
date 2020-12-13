import click
from {{project_name}}.MODULE import YourCommandClass, main as module_main_routine

@click.group()
def main():
    """Command line interface for {{project_name}}"""
    pass

@main.command("command", help="First command", cls=YourCommandClass)
def command(*args, **kwargs):
    raise NotImplementedError("Please import YourCommandClass and run module_main_routine")


if __name__ == "__main__":
    main()
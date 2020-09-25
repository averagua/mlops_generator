import click
from collections import OrderedDict

context = OrderedDict({
    "variable 1": "a",
    "variable 2": "b"
})
for i in context:
    click.prompt(i, type=str)
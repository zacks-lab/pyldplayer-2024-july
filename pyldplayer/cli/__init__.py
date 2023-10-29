
import click

from pyldplayer.cli.app import app
from pyldplayer._internal.cliProcess import _attempt_to_find_default

@click.group()
def ldplayer():
    pass

@ldplayer.command()
def init():
    _attempt_to_find_default()
    print("done")

ldplayer.add_command(app)


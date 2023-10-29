
import click
from pyldplayer.core.app import LDPlayerApp


_app = LDPlayerApp()

@click.group()
def app():
    pass

@app.command()
def multi():
    _app.multiplayer()
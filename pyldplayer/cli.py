
import click
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from pyldplayer.utils import find_ldconsole
import json
from pyldplayer.core.console import LDConsole

mod_path = os.path.dirname(os.path.realpath(__file__))
cfg_path = os.path.join(mod_path, "config.json")


def dump(path):
    with open(cfg_path, "w") as f:
        json.dump({"path": path}, f)

@click.group(invoke_without_command=True)
@click.option("--path", "-p", type=click.Path(exists=True), help="path to ldconsole.exe")
@click.pass_context
def cli(ctx: click.Context, path):
    ctx.ensure_object(dict)
    if path is not None:
        ctx.obj["path"] = path
        dump(path)
    elif os.path.exists(cfg_path):
        with open(cfg_path, "r") as f:
            config = json.load(f)
        ctx.obj.update(config)
    else:
        path = find_ldconsole()
        if path is None:
            print("Could not find ldconsole.exe")
            sys.exit(1)
        
        ctx.obj["path"] = path
        dump(path)

    ctx.obj["console"] = LDConsole(ctx.obj["path"])


@cli.command(name="action")
@click.argument("id")
@click.argument("key")
@click.argument("value")

@click.pass_context
def action(ctx, id, key, value):

    if id.isnumeric():
        id = int(id)

    res =  ctx.obj["console"].action(id, key, value)
    if not res:
        return
    click.echo(res)


@cli.command(name="adb")
@click.argument("id")
@click.argument("command")

@click.pass_context
def adb(ctx, id, command):

    if id.isnumeric():
        id = int(id)

    res =  ctx.obj["console"].adb(id, command)
    if not res:
        return
    click.echo(res)


@cli.command(name="add")
@click.argument("name")

@click.pass_context
def add(ctx, name):

    res =  ctx.obj["console"].add(name)
    if not res:
        return
    click.echo(res)


@cli.command(name="backup")
@click.argument("id")
@click.argument("filepath")

@click.pass_context
def backup(ctx, id, filepath):

    if id.isnumeric():
        id = int(id)

    res =  ctx.obj["console"].backup(id, filepath)
    if not res:
        return
    click.echo(res)


@cli.command(name="backupapp")
@click.argument("id")
@click.argument("filepath")

@click.pass_context
def backupapp(ctx, id, filepath):

    if id.isnumeric():
        id = int(id)

    res =  ctx.obj["console"].backupapp(id, filepath)
    if not res:
        return
    click.echo(res)


@cli.command(name="copy")
@click.argument("id")
@click.argument("name")

@click.pass_context
def copy(ctx, id, name):

    if id.isnumeric():
        id = int(id)

    res =  ctx.obj["console"].copy(id, name)
    if not res:
        return
    click.echo(res)


@cli.command(name="downcpu")
@click.argument("id")

@click.pass_context
def downcpu(ctx, id):

    if id.isnumeric():
        id = int(id)

    res =  ctx.obj["console"].downcpu(id)
    if not res:
        return
    click.echo(res)


@cli.command(name="getprop")
@click.argument("id")
@click.argument("key")

@click.pass_context
def getprop(ctx, id, key):

    if id.isnumeric():
        id = int(id)

    res =  ctx.obj["console"].getprop(id, key)
    if not res:
        return
    click.echo(res)


@cli.command(name="globalsetting")

@click.pass_context
def globalsetting(ctx, ):

    res =  ctx.obj["console"].globalsetting()
    if not res:
        return
    click.echo(res)


@cli.command(name="installapp")
@click.argument("id")
@click.argument("filename")
@click.argument("packagename")

@click.pass_context
def installapp(ctx, id, filename, packagename):

    if id.isnumeric():
        id = int(id)

    res =  ctx.obj["console"].installapp(id, filename, packagename)
    if not res:
        return
    click.echo(res)


@cli.command(name="isrunning")
@click.argument("id")

@click.pass_context
def isrunning(ctx, id):

    if id.isnumeric():
        id = int(id)

    res =  ctx.obj["console"].isrunning(id)
    if not res:
        return
    click.echo(res)


@cli.command(name="killapp")
@click.argument("id")
@click.argument("packagename")

@click.pass_context
def killapp(ctx, id, packagename):

    if id.isnumeric():
        id = int(id)

    res =  ctx.obj["console"].killapp(id, packagename)
    if not res:
        return
    click.echo(res)


@cli.command(name="launch")
@click.argument("id")

@click.pass_context
def launch(ctx, id):

    if id.isnumeric():
        id = int(id)

    res =  ctx.obj["console"].launch(id)
    if not res:
        return
    click.echo(res)


@cli.command(name="launchex")
@click.argument("id")
@click.argument("packagename")

@click.pass_context
def launchex(ctx, id, packagename):

    if id.isnumeric():
        id = int(id)

    res =  ctx.obj["console"].launchex(id, packagename)
    if not res:
        return
    click.echo(res)


@cli.command(name="list")

@click.pass_context
def list(ctx, ):

    res =  ctx.obj["console"].list()
    if not res:
        return
    click.echo(res)


@cli.command(name="list2")

@click.pass_context
def list2(ctx, ):

    res =  ctx.obj["console"].list2()
    if not res:
        return
    click.echo(res)


@cli.command(name="locate")
@click.argument("id")
@click.argument("lng")
@click.argument("lat")

@click.pass_context
def locate(ctx, id, lng, lat):

    if id.isnumeric():
        id = int(id)

    res =  ctx.obj["console"].locate(id, lng, lat)
    if not res:
        return
    click.echo(res)


@cli.command(name="modify")
@click.argument("id")

@click.pass_context
def modify(ctx, id):

    if id.isnumeric():
        id = int(id)

    res =  ctx.obj["console"].modify(id)
    if not res:
        return
    click.echo(res)


@cli.command(name="operateinfo")
@click.argument("id")
@click.argument("file")

@click.pass_context
def operateinfo(ctx, id, file):

    if id.isnumeric():
        id = int(id)

    res =  ctx.obj["console"].operateinfo(id, file)
    if not res:
        return
    click.echo(res)


@cli.command(name="operatelist")
@click.argument("id")

@click.pass_context
def operatelist(ctx, id):

    if id.isnumeric():
        id = int(id)

    res =  ctx.obj["console"].operatelist(id)
    if not res:
        return
    click.echo(res)


@cli.command(name="operaterecord")
@click.argument("id")
@click.argument("content")

@click.pass_context
def operaterecord(ctx, id, content):

    if id.isnumeric():
        id = int(id)

    res =  ctx.obj["console"].operaterecord(id, content)
    if not res:
        return
    click.echo(res)


@cli.command(name="pull")
@click.argument("id")
@click.argument("remote")
@click.argument("local")

@click.pass_context
def pull(ctx, id, remote, local):

    if id.isnumeric():
        id = int(id)

    res =  ctx.obj["console"].pull(id, remote, local)
    if not res:
        return
    click.echo(res)


@cli.command(name="push")
@click.argument("id")
@click.argument("local")
@click.argument("remote")

@click.pass_context
def push(ctx, id, local, remote):

    if id.isnumeric():
        id = int(id)

    res =  ctx.obj["console"].push(id, local, remote)
    if not res:
        return
    click.echo(res)


@cli.command(name="quit")
@click.argument("id")

@click.pass_context
def quit(ctx, id):

    if id.isnumeric():
        id = int(id)

    res =  ctx.obj["console"].quit(id)
    if not res:
        return
    click.echo(res)


@cli.command(name="quitall")

@click.pass_context
def quitall(ctx, ):

    res =  ctx.obj["console"].quitall()
    if not res:
        return
    click.echo(res)


@cli.command(name="reboot")
@click.argument("id")

@click.pass_context
def reboot(ctx, id):

    if id.isnumeric():
        id = int(id)

    res =  ctx.obj["console"].reboot(id)
    if not res:
        return
    click.echo(res)


@cli.command(name="remove")
@click.argument("id")

@click.pass_context
def remove(ctx, id):

    if id.isnumeric():
        id = int(id)

    res =  ctx.obj["console"].remove(id)
    if not res:
        return
    click.echo(res)


@cli.command(name="rename")
@click.argument("id")
@click.argument("name")

@click.pass_context
def rename(ctx, id, name):

    if id.isnumeric():
        id = int(id)

    res =  ctx.obj["console"].rename(id, name)
    if not res:
        return
    click.echo(res)


@cli.command(name="restore")
@click.argument("id")
@click.argument("filepath")

@click.pass_context
def restore(ctx, id, filepath):

    if id.isnumeric():
        id = int(id)

    res =  ctx.obj["console"].restore(id, filepath)
    if not res:
        return
    click.echo(res)


@cli.command(name="restoreapp")
@click.argument("id")
@click.argument("filepath")

@click.pass_context
def restoreapp(ctx, id, filepath):

    if id.isnumeric():
        id = int(id)

    res =  ctx.obj["console"].restoreapp(id, filepath)
    if not res:
        return
    click.echo(res)


@cli.command(name="runapp")
@click.argument("id")
@click.argument("packagename")

@click.pass_context
def runapp(ctx, id, packagename):

    if id.isnumeric():
        id = int(id)

    res =  ctx.obj["console"].runapp(id, packagename)
    if not res:
        return
    click.echo(res)


@cli.command(name="runninglist")

@click.pass_context
def runninglist(ctx, ):

    res =  ctx.obj["console"].runninglist()
    if not res:
        return
    click.echo(res)


@cli.command(name="scan")
@click.argument("id")
@click.argument("filepath")

@click.pass_context
def scan(ctx, id, filepath):

    if id.isnumeric():
        id = int(id)

    res =  ctx.obj["console"].scan(id, filepath)
    if not res:
        return
    click.echo(res)


@cli.command(name="setprop")
@click.argument("id")
@click.argument("key")
@click.argument("value")

@click.pass_context
def setprop(ctx, id, key, value):

    if id.isnumeric():
        id = int(id)

    res =  ctx.obj["console"].setprop(id, key, value)
    if not res:
        return
    click.echo(res)


@cli.command(name="sortwnd")

@click.pass_context
def sortwnd(ctx, ):

    res =  ctx.obj["console"].sortwnd()
    if not res:
        return
    click.echo(res)


@cli.command(name="uninstallapp")
@click.argument("id")
@click.argument("packagename")

@click.pass_context
def uninstallapp(ctx, id, packagename):

    if id.isnumeric():
        id = int(id)

    res =  ctx.obj["console"].uninstallapp(id, packagename)
    if not res:
        return
    click.echo(res)


@cli.command(name="zoomin")

@click.pass_context
def zoomin(ctx, ):

    res =  ctx.obj["console"].zoomin()
    if not res:
        return
    click.echo(res)


@cli.command(name="zoomout")

@click.pass_context
def zoomout(ctx, ):

    res =  ctx.obj["console"].zoomout()
    if not res:
        return
    click.echo(res)


def LdCli():
    cli()
    
def LdShell():
    import click_shell

    # make shell from cli
    ctx = cli.make_context("",[])
    shell = click_shell.make_click_shell(
        ctx
    )
    shell.cmdloop()

if __name__ == "__main__":
    cli()

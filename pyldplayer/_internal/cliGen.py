cli_header = """
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
"""
cmd_template_1 = """

@cli.command(name="{name}")
"""

cmd_template_2 = """
@click.pass_context
def {name}(ctx, {vars}):
"""

cmd_parser = """
    if id.isnumeric():
        id = int(id)
"""

cmd_template_3 = """
    res =  ctx.obj["console"].{name}({vars})
    if not res:
        return
    click.echo(res)
"""

main = """
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
"""

import inspect
import os
import typing
from pyldplayer._internal.consoleInterfaces.base import ConsoleInterface

currentMod = os.path.dirname(os.path.realpath(__file__))
baseMod = os.path.dirname(currentMod)
cliFile = os.path.join(baseMod, "cli.py")

def gen():
    f = open(cliFile, "w")
    f.write(cli_header)
    
    for name, method in inspect.getmembers(ConsoleInterface):
        if name.startswith("_"):
            continue
        
        if not callable(method):
            continue
        
        f.write(cmd_template_1.format(name=name))

        params = inspect.signature(method).parameters
    
        vars = []
        for pname, param in params.items():
            param : inspect.Parameter
            if pname == "self":
                continue
            
            annotation = param.annotation
            if annotation not in [typing.Union[str, int], str]:
                continue

            f.write("@click.argument(\"{pname}\")\n".format(pname=pname))
            vars.append(pname)
        
        f.write(cmd_template_2.format(name=name, vars=", ".join(vars)))
        if "id" in vars:
            f.write(cmd_parser)
            
        f.write(cmd_template_3.format(name=name, vars=", ".join(vars)))

        
    f.write("\n")
    
    f.write(main)
    f.close()
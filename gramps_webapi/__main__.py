"""Command line interface for the Gramps web API."""


import os

import click

from .app import create_app
from .auth import SQLAuth
from .const import ENV_CONFIG_FILE


@click.group("cli")
@click.option("--config", help="Set the path to the config file", required=True)
@click.pass_context
def cli(ctx, config):
    """Gramps web API command line interface."""
    os.environ[ENV_CONFIG_FILE] = os.path.abspath(config)
    ctx.obj = create_app()


@cli.command("run")
@click.option("-p", "--port", help="Port to use (default: 5000)", default=5000)
@click.pass_context
def run(ctx, port):
    """Run the app."""
    app = ctx.obj
    # threading is disabled to avoid problems with locked databases
    app.run(port=port, threaded=False)


@cli.group("user")
@click.pass_context
def user(ctx):
    app = ctx.obj
    ctx.obj = SQLAuth(db_uri=app.config["USER_DB_URI"])


@user.command("add")
@click.argument("name")
@click.argument("password")
@click.option("--fullname", help="Full name", default="")
@click.option("--email", help="E-mail address", default=None)
@click.pass_context
def user_add(ctx, name, password, fullname, email):
    auth = ctx.obj
    auth.create_table()
    auth.add_user(name, password, fullname, email)


@user.command("delete")
@click.argument("name")
@click.pass_context
def user_del(ctx, name):
    auth = ctx.obj
    auth.delete_user(name)


if __name__ == "__main__":
    cli(
        prog_name="python3 -m gramps_webapi"
    )  # pylint:disable=no-value-for-parameter,unexpected-keyword-arg

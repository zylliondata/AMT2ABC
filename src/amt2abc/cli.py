import click

from amt2abc import __version__


@click.group()
@click.version_option(version=__version__, prog_name="amt2abc")
def main():
    """AMT2ABC: Atomic Mechanism Triplets to Atomic Business Capabilities."""


@main.command()
def list():
    """List available AMTs and ABCs."""
    click.echo("AMT2ABC Compiler v" + __version__)
    click.echo("AMTs: 0 available")
    click.echo("ABCs: 0 available")

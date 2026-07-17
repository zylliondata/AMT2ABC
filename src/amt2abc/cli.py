import json

import click

from amt2abc import __version__


@click.group()
@click.version_option(version=__version__, prog_name="amt2abc")
def main():
    """AMT2ABC: Atomic Mechanism Triplets to Atomic Business Capabilities."""


@main.command()
def list():
    """List available AMTs and ABCs."""
    from amt2abc.parser.abc_parser import ABCParser
    from amt2abc.parser.amt_parser import AMTParser

    amts = AMTParser().load_all()
    abcs = ABCParser().load_all()
    click.echo(f"AMT2ABC Compiler v{__version__}")
    click.echo(f"AMTs: {len(amts)} available")
    for amt in amts:
        click.echo(f"  - {amt.id}: {amt.name}")
    click.echo(f"ABCs: {len(abcs)} available")
    for abc in abcs:
        click.echo(f"  - {abc.id}: {abc.name}")


@main.command()
@click.argument("goal")
@click.option("--format", "-f", "output_format", default="text")
def compile(goal, output_format):
    """Compile a goal statement into recommended ABCs."""
    from amt2abc.compiler.pipeline import CompilerPipeline

    pipeline = CompilerPipeline()
    result = pipeline.compile(goal)

    if output_format == "json":
        click.echo(json.dumps(result, ensure_ascii=False, indent=2))
        return

    click.echo(f"Goal: {result['goal']}")
    click.echo(f"Matched AMTs: {len(result['matched_amts'])}")
    for amt in result["matched_amts"]:
        click.echo(f"  {amt['id']:<30} score={amt['score']}")
    click.echo(f"Recommended ABCs: {len(result['recommended_abcs'])}")

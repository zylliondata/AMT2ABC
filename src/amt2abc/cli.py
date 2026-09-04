import json
from typing import Any, Dict

import click

from amt2abc import __version__


@click.group()
@click.version_option(version=__version__, prog_name="amt2abc")
def main() -> None:
    """AMT2ABC: Atomic Mechanism Triplets to Atomic Business Capabilities."""


@main.command()
def list() -> None:  # noqa: A001
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
@click.argument("amt_id")
@click.option("--format", "-f", "output_format", default="text")
def info(amt_id: str, output_format: str) -> None:
    """Show details of an AMT by ID."""
    from amt2abc.parser.amt_parser import AMTParser

    amt = next(
        (a for a in AMTParser().load_all() if a.id == amt_id),
        None,
    )
    if amt is None:
        raise click.ClickException(f"AMT not found: {amt_id}")

    data: Dict[str, Any] = {
        "id": amt.id,
        "name": amt.name,
        "domain": amt.domain,
        "triplets": [
            {
                "cause": t.cause,
                "effect": t.effect,
                "relation": t.relation,
                "mechanism": t.mechanism,
                "weight": t.weight,
                "confidence": t.confidence,
            }
            for t in amt.triplets
        ],
        "layer": amt.layer,
        "evidence_source": amt.evidence_source,
        "mcl_engine": amt.mcl_engine,
    }

    if output_format == "json":
        click.echo(json.dumps(data, ensure_ascii=False, indent=2))
        return

    click.echo(f"AMT: {amt.id}  ({amt.name})")
    click.echo(f"Domain: {amt.domain}")
    click.echo(f"Layer: {amt.layer or '-'}  Evidence: {amt.evidence_source or '-'}")
    click.echo(f"Triplets: {len(amt.triplets)}")
    for t in amt.triplets:
        click.echo(
            f"  {t.cause} --{t.relation}--> {t.effect} "
            f"(w={t.weight}, c={t.confidence})"
        )
    if amt.secp is not None:
        click.echo(f"SECP subject: {amt.secp.S.subject}")
        click.echo(f"SECP process: {', '.join(amt.secp.P)}")


@main.command()
@click.argument("source")
@click.argument("target")
def graph(source: str, target: str) -> None:
    """Find a causal path between two variables in the AMT graph."""
    from amt2abc.compiler.graph import AMTGraph
    from amt2abc.parser.amt_parser import AMTParser

    amts = AMTParser().load_all()
    amt_graph = AMTGraph()
    amt_graph.build(amts)
    path = amt_graph.find_path(source, target)

    if not path:
        click.echo(f"No path found from '{source}' to '{target}'.")
        return

    click.echo(f"Path: {' -> '.join(path)}")


@main.command()
@click.argument("goal")
@click.option("--format", "-f", "output_format", default="text")
def compile(goal: str, output_format: str) -> None:  # noqa: A001
    """Compile a goal statement into recommended ABCs."""
    from amt2abc.compiler.pipeline import CompilerPipeline

    pipeline = CompilerPipeline()
    result: Dict[str, Any] = pipeline.compile(goal)

    if output_format == "json":
        click.echo(json.dumps(result, ensure_ascii=False, indent=2))
        return

    click.echo(f"Goal: {result['goal']}")
    click.echo(f"Matched AMTs: {len(result['matched_amts'])}")
    for amt in result["matched_amts"]:
        click.echo(f"  {amt['id']:<30} score={amt['score']}")
    click.echo(f"Recommended ABCs: {len(result['recommended_abcs'])}")

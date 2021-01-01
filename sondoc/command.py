import shutil
from pathlib import Path

import click

from .bind import bind as run_bind
from .prepare import prepare as run_prepare


@click.group(help="Create self-contained cross-refernced documents based on markdown.")
def cli():
    pass


@cli.command(help="Prepare the input for binding it to a document")
@click.argument(
    "input",
    nargs=1,
    type=click.Path(exists=True, file_okay=False, resolve_path=True),
)
@click.argument(
    "output",
    nargs=1,
    type=click.Path(file_okay=False, resolve_path=True),
)
@click.option(
    "--rm/--no-rm", default=False, help="Remove output folder before preparing"
)
def prepare(input, output, rm):
    if rm:
        shutil.rmtree(output, ignore_errors=True)
    run_prepare(Path(input), Path(output))


@cli.command(
    help="Bind the output of prepare to a document, can point to a subfolder of the prepare output."
)
@click.argument(
    "input",
    nargs=1,
    type=click.Path(exists=True, file_okay=False, resolve_path=True),
)
@click.option(
    "--output",
    default="output.html",
    type=click.Path(file_okay=True, dir_okay=False, writable=True),
    help="Output file",
)
@click.option("--follow/--no-follow", default=False, help="Follow symlinks")
def bind(input, output, follow):
    run_bind(Path(input), Path(output), follow)


if __name__ == "__main__":
    cli()

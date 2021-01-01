import click


@click.group(help="Create self-contained cross-refernced documents based on markdown.")
def cli():
    pass


@cli.command(help="Prepare the input for binding it to a document")
@click.argument("source", nargs=1)
@click.argument("output", nargs=1)
def prepare():
    click.echo("Initialized the database")


@cli.command(help="Bind the output of prepare to a document.")
def bind():
    click.echo("Dropped the database")


if __name__ == "__main__":
    cli()

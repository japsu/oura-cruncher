import click

from .cli.run_experiments import run_experiments
from .cli.update_data import update_data


@click.group
def cli():
    pass


cli.add_command(run_experiments)
cli.add_command(update_data)


if __name__ == "__main__":
    cli()

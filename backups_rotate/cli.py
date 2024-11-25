from pathlib import Path

import click
from ruamel.yaml import YAML, scanner

from backups_rotate.area import Area

DEFAULT_CONFIG_FILE = "/etc/backups-rotate.yaml"

@click.command()
@click.option(
    "--config",
    "-c",
    default=DEFAULT_CONFIG_FILE,
    help="Configuration file",
)
@click.option(
    "--list",
    "-l",
    is_flag=True,
    help="List areas",
)
@click.option(
    "--list-deleted",
    "-d",
    is_flag=True,
    help="list only files to be deleted",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Verbose mode",
)
@click.option(
    "--dry-run",
    "-n",
    is_flag=True,
    help="Dry run",
)
@click.argument('area_names', nargs=-1)
def cli(config, list, list_deleted, verbose, dry_run, area_names):
    """
    backups_rotate: a tool to manage backups
    """

    # read the configuration
    yaml = YAML(typ='safe')
    candidates = [ Path(config), Path(".") / Path(config).name ]
    for candidate in candidates:
        if verbose:
            click.echo(f"Trying to reading configuration from {candidate}")
        if candidate.exists():
            try:
                with open(candidate) as f:
                    config = yaml.load(f)
                    areas_by_name = {area["name"]: area for area in config}
                if verbose:
                    click.echo(f"Configuration read from {candidate}")
                break
            except scanner.ScannerError as e:
                click.echo(f"Error reading configuration from {candidate}: {e}")
    else:
        click.echo(f"Config file not found - exiting - have tried:")
        for candidate in candidates:
            click.echo(f"  {candidate.absolute()}")
        return 1

    if not area_names:
        area_dicts = config
    else:
        try:
            area_dicts = [areas_by_name[name] for name in area_names]
        except KeyError as e:
            click.echo(f"Area {e} not found in configuration")
            return 1
    try:
        areas = [Area(area_dict) for area_dict in area_dicts]
    except ValueError as e:
        click.echo(f"Error creating area: {e}")
        return 1

    for area in areas:
        area.read()
        if verbose:
            click.echo(f"area={area}")
        if list:
            kept = not list_deleted
            area.list(verbose=verbose, kept=kept)
        else:
            area.delete(dry_run=dry_run, verbose=verbose)


if __name__ == "__main__":
    cli()

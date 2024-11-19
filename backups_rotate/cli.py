import click
from ruamel.yaml import YAML

from backups_rotate.area import Area

DEFAULT_CONFIG_FILE = "/etc/backups_rotate.yaml"

@click.command()
@click.option(
    "--config",
    "-c",
    default=DEFAULT_CONFIG_FILE,
    help="Configuration file",
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
def cli(config, verbose, dry_run, area_names):
    """
    backups_rotate: a tool to manage backups
    """

    # read the configuration
    yaml = YAML(typ='safe')
    with open(config) as f:
        config = yaml.load(f)
        areas_by_name = {area["name"]: area for area in config}

    if not area_names:
        area_dicts = config
    else:
        try:
            area_dicts = [areas_by_name[name] for name in area_names]
        except KeyError as e:
            click.echo(f"Area {e} not found in configuration")
            return 1

    areas = [Area(area_dict) for area_dict in area_dicts]

    if verbose:
        for area in areas:
            area.read()
            if verbose:
                click.echo(f"area={area}")
            area.delete(dry_run=dry_run, verbose=verbose)


if __name__ == "__main__":
    cli()

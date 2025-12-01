"""Database management CLI commands."""

from pathlib import Path

from alembic import command
from alembic.config import Config
from rich.console import Console

import blanket.io.click as click

console = Console()


def get_alembic_config() -> Config:
    """Get Alembic configuration."""
    # alembic.ini is in the backend/ directory
    backend_dir = Path(__file__).parent.parent.parent
    ini_path = backend_dir / "alembic.ini"

    alembic_cfg = Config(str(ini_path))
    # Set script_location to absolute path
    script_location = backend_dir / "blanket" / "db" / "migrations"
    alembic_cfg.set_main_option("script_location", str(script_location))

    return alembic_cfg


@click.group()
def db():
    """Database management utilities."""
    pass


@db.command()
@click.option(
    "--revision",
    "-r",
    default="head",
    help="Revision to upgrade to",
)
def upgrade(revision: str):
    """Upgrade database to a later version."""
    console.print(f"[cyan]Upgrading database to {revision}...[/cyan]")
    alembic_cfg = get_alembic_config()
    command.upgrade(alembic_cfg, revision)
    console.print(f"[green]Database upgraded to {revision}[/green]")


@db.command()
@click.option(
    "--revision",
    "-r",
    required=True,
    help="Revision to downgrade to",
)
def downgrade(revision: str):
    """Downgrade database to a previous version."""
    console.print(f"[cyan]Downgrading database to {revision}...[/cyan]")
    alembic_cfg = get_alembic_config()
    command.downgrade(alembic_cfg, revision)
    console.print(f"[green]Database downgraded to {revision}[/green]")


@db.command()
def current():
    """Show current database revision."""
    alembic_cfg = get_alembic_config()
    command.current(alembic_cfg)


@db.command()
def history():
    """Show migration history."""
    alembic_cfg = get_alembic_config()
    command.history(alembic_cfg)


@db.command()
@click.option(
    "--revision",
    "-r",
    default="head",
    help="Revision to show (defaults to head)",
)
def show(revision: str):
    """Show information about a revision."""
    alembic_cfg = get_alembic_config()
    command.show(alembic_cfg, revision)


@db.command()
@click.option(
    "--revision",
    "-r",
    help="Revision to stamp to (use 'head' for latest)",
)
def stamp(revision: str | None):
    """Stamp the database with a given revision without running migrations."""
    if not revision:
        console.print("[red]Error: --revision is required[/red]")
        return

    console.print(f"[yellow]Stamping database to {revision}...[/yellow]")
    alembic_cfg = get_alembic_config()
    command.stamp(alembic_cfg, revision)
    console.print(f"[green]Database stamped to {revision}[/green]")

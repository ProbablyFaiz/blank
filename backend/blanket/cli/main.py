import blanket.db.commands as db_commands
import blanket.io.click as click


@click.group()
def cli():
    pass


cli.add_command(db_commands.db)


if __name__ == "__main__":
    cli()

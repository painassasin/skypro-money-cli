import typer

from skypro.cli.commands import calculate_command

app = typer.Typer()

app.command(name='calculate')(calculate_command)

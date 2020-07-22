import click
import os
from commands import user, file
from constant import SECRET_PATH, RECIPIENTS_FILE_NAME


@click.group()
def cli():
    pass


@cli.command()
def init():
    """Initializes xenolith in the current directory"""
    if os.path.exists(SECRET_PATH):
        return click.echo('Xenolith has already been initialized')
    try:
        os.mkdir(SECRET_PATH)
        recipients = open(SECRET_PATH + RECIPIENTS_FILE_NAME, 'w')
        recipients.close()
    except OSError as e:
        return click.echo('There was an error creating the secret folder.\n{}'.format(e))

    click.echo('.secret folder created in current directory')


command_collection = click.CommandCollection(
    sources=[cli, user.user, file.file])

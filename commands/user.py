import click
import os
import utils
import constant
from constant import SECRET_PATH, RECIPIENTS_FILE_NAME


@click.group()
def user():
    pass


@user.command()
@utils.secret_folder_exists
@click.argument('recipient')
def add(recipient):
    """Adds a recipient that can unencrypt files.

    - recpient - Public key of the recipient"""
    # TODO: Allow multiple recipients
    with open(SECRET_PATH + RECIPIENTS_FILE_NAME, 'a') as recipients_file:
        recipients_file.write(recipient + '\n')
        click.echo('Recipient has been added')


@user.command()
@click.argument('id')
def remove(id):
    if not os.path.exists(SECRET_PATH):
        return click.echo(
            'Cannot detect a .secret folder. Run "xenolith init" to initialize xenolith')
